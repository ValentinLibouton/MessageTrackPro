import sqlite3
import os
from models import Message
from dotenv import load_dotenv

# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")
YOURPHONENUMBER = os.getenv("YOURPHONENUMBER")


def get_tag_id_with_tag(tag):
    """
    Retrieve the tag ID associated with a specific tag.

    Args:
        tag (str): The tag for which to retrieve the associated tag ID.

    Returns:
        int or None: The tag ID if found, or None if the tag doesn't exist.
    """
    query = f"""
                SELECT tag_id
                FROM Tags
                WHERE tag = '{tag}'
                """
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(query)
        tag_id = cursor.fetchone()

        if tag_id:
            tag_id = tag_id[0]
        return tag_id
    except Exception as e:
        print(f"\033[93mUne erreur s'est produite lors de la requête get_tag_id_with_tag : {e} \033[0m")


def get_message_ids_with_tag_id(tag_id):
    """
    Retrieve message IDs associated with a specific tag ID.

    Args:
        tag_id (int): The ID of the tag for which to retrieve associated message IDs.

    Returns:
        tuple: A tuple containing message IDs (message_id, sms_id, mms_id) associated with the given tag ID.
    """
    list_message_ids = []
    query = f"""SELECT
                        message_id AS [message_id],
                        sms_id AS [sms_id],
                        mms_id AS [mms_id]
                        FROM MTM_Tags
                        WHERE tag_id = {tag_id}
                    """
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            if result[0]:
                list_message_ids.append(result[0])
            elif result[1]:
                list_message_ids.append(result[1])
            elif result[2]:
                list_message_ids.append(result[2])

        return tuple(list_message_ids)
    except Exception as e:
        print(f"\033[93mUne erreur s'est produite lors de la requête get_message_ids_with_tag_id : {e} \033[0m")


def get_headers():
    return ['Sender name', 'Sender address', 'Recipient type', 'Recipient name', 'Recipient address', "Date", "Time",
            "Subject", "Original filename", "Content", "Attachments", "Tags", "Message id"]


def get_contact_id(first_name, last_name):
    """
    Retrieve the contact ID for a contact with the given first name and last name from the database.

    Args:
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.

    Returns:
        int or None: The contact ID if the contact exists, or None if the contact is not found.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""SELECT contact_id
                FROM Contacts
                WHERE first_name = ? AND last_name = ?"""
    cursor.execute(query, (first_name, last_name))
    contact_id = cursor.fetchone()
    connection.close()
    if contact_id:
        contact_id = contact_id[0]
    return contact_id


def get_your_contact_id():
    """
    Retrieve your contact ID based on your phone number.

    Returns:
        int: Your contact ID if found, None otherwise.
    """
    print(f"Retrieve your contact_id with phone: {YOURPHONENUMBER}")
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query_your_contact_id = """SELECT contact_id
                               FROM ContactPhoneNumbers
                               WHERE phone = ?"""
    cursor.execute(query_your_contact_id, (YOURPHONENUMBER,))
    your_contact_id = cursor.fetchone()
    connection.close()
    if your_contact_id:
        return your_contact_id[0]
    return None


def get_email_id(email):
    """
    Retrieve the email ID associated with the given email address from the ContactEmails table.

    Args:
        email (str): The email address to search for in the database.

    Returns:
        int or None: The email ID if found, or None if not found or an error occurs.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""SELECT email_id
                FROM ContactEmails
                WHERE email = ?"""
    cursor.execute(query, (email,))
    email_id = cursor.fetchone()
    connection.close()
    if email_id:
        email_id = email_id[0]
    return email_id


def get_emails_addresses_linked_to_contact_id(contact_id):
    """
    Retrieve a list of email addresses linked to a specific contact ID from the ContactEmails table.

    Args:
        contact_id (int): The unique identifier of the contact for which email addresses are to be retrieved.

    Returns:
        list of str: A list of email addresses associated with the specified contact ID.
                     An empty list is returned if no email addresses are found or if an error occurs.
    """
    emails_list = []
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""SELECT email
                FROM ContactEmails
                WHERE contact_id = ?"""
    cursor.execute(query, (contact_id,))
    emails = cursor.fetchall()
    if emails:
        for email in emails:
            emails_list.append(email[0])
    return emails_list


def find_messages_with_tag(tag):
    """
    Find messages containing a specific tag linked to a contact ID.

    Args:
        contact_id (int): The ID of the contact to retrieve linked messages for.
        tag (str): The tag to search for in message tags.

    Returns:
        tuple: A tuple containing headers and a list of message objects.
    """
    tag_id = get_tag_id_with_tag(tag=tag)
    tuple_message_ids = get_message_ids_with_tag_id(tag_id=tag_id)
    headers = get_headers()

    your_contact_id = get_your_contact_id()
    if not your_contact_id:
        print("\033[93mError getting your contact ID\033[0m")
        return [], []

    query_1_sms_with = f"""WITH MeContact AS (
                                    SELECT *
                                FROM Contacts
                                WHERE contact_id = {your_contact_id}),
                            MeAddress AS (
                                SELECT *
                                FROM ContactPhoneNumbers
                                WHERE contact_id = {your_contact_id})"""

    query_2_emails = f"""
                                SELECT
                                    C.first_name || ' ' || C.last_name AS [Sender name],
                                    CE.email AS [Sender address],
                                    CASE
                                        WHEN RE.is_cc = 0 AND RE.is_bcc = 0 THEN 'Destinataire direct'
                                        WHEN RE.is_cc = 1 AND RE.is_bcc = 0 THEN 'Destinataire en copie'
                                        WHEN RE.is_cc = 0 AND RE.is_bcc = 1 THEN 'Destinataire caché'
                                        ELSE 'Autre' -- Gérer d'autres cas si nécessaire
                                    END AS "Recipient type",
                                    C2.first_name || ' ' || C2.last_name AS [Recipient name],
                                    CE2.email [Recipient address],
                                    E.date AS [Date],
                                    E.time AS [Time],
                                    E.subject AS [Subject],
                                    E.original_filename AS [Original filename],
                                    E.content AS [Content],
                                    (
                                        SELECT GROUP_CONCAT(filename, ', ')
                                        FROM Attachments AS A
                                        WHERE A.message_id = E.message_id
                                    ) AS [Attachments],
                                    (
                                        SELECT GROUP_CONCAT(T.tag, ', ')
                                        FROM Tags AS T
                                        LEFT JOIN MTM_Tags AS MTM_T
                                        ON MTM_T.tag_id = T.tag_id
                                        WHERE MTM_T.message_id = E.message_id
                                    ) AS [Tags],
                                    E.message_id AS [Message id]
                                FROM Emails AS E
                                JOIN ContactEmails AS CE
                                ON E.sender_email_id = CE.email_id
                                JOIN Contacts AS C
                                ON CE.contact_id = C.contact_id
                                JOIN RecipientEmails AS RE
                                ON E.message_id = RE.message_id
                                JOIN ContactEmails AS CE2
                                ON RE.email_id = CE2.email_id
                                JOIN Contacts AS C2
                                ON CE2.contact_id = C2.contact_id
                                LEFT JOIN Attachments AS A
                                ON A.message_id = E.message_id
                                WHERE E.message_id IN {tuple_message_ids}
                                GROUP BY E.message_id """

    query_3_union = f"""
                        UNION
                        """

    query_4_sms = f"""  SELECT
                                CASE
                                    WHEN S.type = '1' THEN C_SMS.first_name || ' ' || C_SMS.last_name
                                    WHEN S.type = '2' THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                                    ELSE 'ERROR !'
                                END AS [Sender name],
                                CASE
                                    WHEN S.type = '1' THEN CPN.phone
                                    WHEN S.type = '2' THEN (SELECT phone FROM MeAddress)
                                    ELSE 'ERROR !'
                                END AS [Sender address],
                                'Destinataire direct' AS [Recipient type],
                                CASE
                                    WHEN S.type = '1' THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                                    WHEN S.type = '2' THEN C_SMS.first_name || ' ' || C_SMS.last_name
                                    ELSE 'ERROR !'
                                END AS [Recipient name],
                                CASE
                                    WHEN S.type = '1' THEN (SELECT phone FROM MeAddress)
                                    WHEN S.type = '2' THEN CPN.phone
                                    ELSE 'ERROR !'
                                END AS [Recipient address],
                                S.date AS [Date],
                                S.time AS [Time],
                                'No subject' AS [Subject],
                                S.original_filename AS [Original filename],
                                S.body AS [Content],
                                'None' AS [Attachments],
                                (
                                    SELECT GROUP_CONCAT(T.tag, ', ')
                                    FROM Tags AS T
                                    LEFT JOIN MTM_Tags AS MTM_T
                                    ON MTM_T.tag_id = T.tag_id
                                    WHERE MTM_T.sms_id = S.sms_id
                                ) AS [Tags],
                                S.sms_id AS [Message id]
                            FROM Sms AS S
                            JOIN Sms_ContactPhoneNumber AS SCPN
                            ON SCPN.sms_id = S.sms_id
                            JOIN ContactPhoneNumbers AS CPN
                            ON CPN.phone_id = SCPN.phone_id
                            JOIN Contacts AS C_SMS
                            ON C_SMS.contact_id = CPN.contact_id
                            WHERE S.sms_id IN {tuple_message_ids}
                            GROUP BY S.sms_id
                            """

    query_5_union = f""" UNION """

    query_6_mms = f"""
                        SELECT
                            CASE
                                WHEN M.msg_box = '1' THEN C_MMS.first_name || ' ' || C_MMS.last_name
                                WHEN M.msg_box = '2' THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                                ELSE 'ERROR !'
                            END AS [Sender name],
                            CASE
                                WHEN M.msg_box = '1' THEN CPN2.phone
                                WHEN M.msg_box = '2' THEN (SELECT phone FROM MeAddress)
                                ELSE 'ERROR !'
                            END AS [Sender address],
                            'Destinataire direct' AS [Recipient type],
                            CASE
                                WHEN M.msg_box = '1' THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                                WHEN M.msg_box = '2' THEN C_MMS.first_name || ' ' || C_MMS.last_name
                                ELSE 'ERROR !'
                            END AS [Recipient name],
                            CASE
                                WHEN M.msg_box = '1' THEN (SELECT phone FROM MeAddress)
                                WHEN M.msg_box = '2' THEN CPN2.phone
                                ELSE 'ERROR !'
                            END AS [Recipient address],
                            M.date AS [Date],
                            M.time AS [Time],
                            'No subject' AS [Subject],
                            'None' AS [Original filename],
                            (
                                SELECT text
                                FROM MmsPart AS MP_sub
                                JOIN Mms_MmsPart MMP_sub
                                ON MP_sub.part_id = MMP_sub.part_id
                                JOIN Mms As M_sub
                                ON M_sub.mms_id = MMP_sub.mms_id
                                WHERE MP_sub.seq = '0' and MP_sub.ct = 'text/plain' AND MP_sub.text != '' AND M_sub.mms_id = M.mms_id
                                LIMIT 1
                            ) AS [Content],
                            (
                            SELECT GROUP_CONCAT(cl, ', ')
                            FROM (
                                SELECT DISTINCT cl
                                FROM MmsPart AS MP_sub
                                JOIN Mms_MmsPart MMP_sub
                                ON MP_sub.part_id = MMP_sub.part_id
                                JOIN Mms As M_sub
                                ON M_sub.mms_id = MMP_sub.mms_id
                                WHERE MP_sub.seq = '0' and MP_sub.ct != 'text/plain' AND M_sub.mms_id = M.mms_id
                                )
                            ) AS [Attachments],
                            (
                                SELECT GROUP_CONCAT(T.tag, ', ')
                                FROM Tags AS T
                                LEFT JOIN MTM_Tags AS MTM_T
                                ON MTM_T.tag_id = T.tag_id
                                WHERE MTM_T.mms_id = M.mms_id
                            ) AS [Tags],
                            M.mms_id AS [Message id]
                        FROM Mms As M
                        JOIN Mms_ContactPhoneNumber AS MCPN
                        ON MCPN.mms_id = M.mms_id
                        JOIN ContactPhoneNumbers AS CPN2
                        ON CPN2.phone_id = MCPN.phone_id
                        JOIN Contacts AS C_MMS
                        ON C_MMS.contact_id = CPN2.contact_id
                        JOIN Mms_MmsPart AS MMP
                        ON MMP.mms_id = M.mms_id
                        JOIN MmsPart AS MP
                        ON MP.part_id = MMP.part_id
                        WHERE M.mms_id IN {tuple_message_ids}
                        GROUP BY M.mms_id 
                    """
    query_end_order = f"""
                            ORDER BY Date, Time"""

    query = query_1_sms_with + query_2_emails + query_3_union + query_4_sms + query_5_union + query_6_mms + query_end_order
    results = None
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print(f"\033[93mUne erreur s'est produite lors de la requête find_messages_with_tag : {e} \033[0m")

    messages = []
    if results:
        for result in results:
            message_obj = Message.Message(*result)
            messages.append(message_obj)
    return headers, messages


def get_messages(contact_id, word=None, start_date=None, end_date=None):
    """
    Retrieve messages for a specific contact within a specified date range and optionally containing a specific word.

    Args:
        contact_id (int): The ID of the contact for whom to retrieve messages.
        word (str, optional): A specific word to search for within message content (default is None).
        start_date (str, optional): The start date of the date range in "YYYY-MM-DD" format (default is "1950-01-01").
        end_date (str, optional): The end date of the date range in "YYYY-MM-DD" format (default is "3000-12-31").

    Returns:
        tuple: A tuple containing headers and a list of message objects.
    """
    headers = get_headers()

    your_contact_id = get_your_contact_id()
    if not your_contact_id:
        print("\033[93mError getting your contact ID\033[0m")
        return [], []
    if not start_date:
        start_date = "1950-01-01"
    if not end_date:
        end_date = "3000-12-31"
    if not word:
        concat_where_email = f"""
            GROUP BY E.message_id
            """
        concat_where_sms = f""" 
            GROUP BY S.sms_id
            """
        concat_where_mms = f""" 
            GROUP BY M.mms_id
            """
    else:
        concat_where_email = f"""
                AND Content LIKE '%{word}%'
            GROUP BY E.message_id
            """
        concat_where_sms = f"""
                AND Content LIKE '%{word}%'
            GROUP BY S.sms_id
            """
        concat_where_mms = f"""
                AND Content LIKE '%{word}%'
            GROUP BY M.mms_id
            """
    union = f"""
        UNION
        """

    order = f"""
        ORDER BY Date, Time
        """

    query_1_sms_with = f"""
        WITH    MeContact AS (
                    SELECT *
                    FROM Contacts
                    WHERE contact_id = {your_contact_id}),
                MeAddress AS (
                    SELECT *
                    FROM ContactPhoneNumbers
                    WHERE contact_id = {your_contact_id})
                    """

    query_2_emails = f"""
        SELECT
            C.first_name || ' ' || C.last_name AS [Sender name],
            CE.email AS [Sender address],
            CASE
                WHEN RE.is_cc = 0 AND RE.is_bcc = 0 THEN 'Destinataire direct'
                WHEN RE.is_cc = 1 AND RE.is_bcc = 0 THEN 'Destinataire en copie'
                WHEN RE.is_cc = 0 AND RE.is_bcc = 1 THEN 'Destinataire caché'
                ELSE 'Autre' -- Gérer d'autres cas si nécessaire
            END AS "Recipient type",
            C2.first_name || ' ' || C2.last_name AS [Recipient name],
            CE2.email [Recipient address],
            E.date AS [Date],
            E.time AS [Time],
            E.subject AS [Subject],
            E.original_filename AS [Original filename],
            E.content AS [Content],
            (
                SELECT GROUP_CONCAT(filename, ', ')
                FROM Attachments AS A
                WHERE A.message_id = E.message_id
            ) AS [Attachments],
            (
                SELECT GROUP_CONCAT(T.tag, ', ')
                FROM Tags AS T
                LEFT JOIN MTM_Tags AS MTM_T
                ON MTM_T.tag_id = T.tag_id
                WHERE MTM_T.message_id = E.message_id
            ) AS [Tags],
            E.message_id AS [Message id]
        FROM Emails AS E
        JOIN ContactEmails AS CE
        ON E.sender_email_id = CE.email_id
        JOIN Contacts AS C
        ON CE.contact_id = C.contact_id
        JOIN RecipientEmails AS RE
        ON E.message_id = RE.message_id
        JOIN ContactEmails AS CE2
        ON RE.email_id = CE2.email_id
        JOIN Contacts AS C2
        ON CE2.contact_id = C2.contact_id
        LEFT JOIN Attachments AS A
        ON A.message_id = E.message_id
        WHERE (C.contact_id = {contact_id} OR C2.contact_id = {contact_id}) AND (Date BETWEEN '{start_date}' AND '{end_date}')"""

    query_4_sms = f"""
        SELECT
        CASE
            WHEN S.type = '1' THEN C_SMS.first_name || ' ' || C_SMS.last_name
            WHEN S.type = '2' THEN (SELECT first_name || ' ' || last_name FROM MeContact)
            ELSE 'ERROR !'
        END AS [Sender name],
        CASE
            WHEN S.type = '1' THEN CPN.phone
            WHEN S.type = '2' THEN (SELECT phone FROM MeAddress)
            ELSE 'ERROR !'
        END AS [Sender address],
        'Destinataire direct' AS [Recipient type],
        CASE
            WHEN S.type = '1' THEN (SELECT first_name || ' ' || last_name FROM MeContact)
            WHEN S.type = '2' THEN C_SMS.first_name || ' ' || C_SMS.last_name
            ELSE 'ERROR !'
        END AS [Recipient name],
        CASE
            WHEN S.type = '1' THEN (SELECT phone FROM MeAddress)
            WHEN S.type = '2' THEN CPN.phone
            ELSE 'ERROR !'
        END AS [Recipient address],
        S.date AS [Date],
        S.time AS [Time],
        'No subject' AS [Subject],
        S.original_filename AS [Original filename],
        S.body AS [Content],
        'None' AS [Attachments],
        (
            SELECT GROUP_CONCAT(T.tag, ', ')
            FROM Tags AS T
            LEFT JOIN MTM_Tags AS MTM_T
            ON MTM_T.tag_id = T.tag_id
            WHERE MTM_T.sms_id = S.sms_id
        ) AS [Tags],
        S.sms_id AS [Message id]
        FROM Sms AS S
        JOIN Sms_ContactPhoneNumber AS SCPN
        ON SCPN.sms_id = S.sms_id
        JOIN ContactPhoneNumbers AS CPN
        ON CPN.phone_id = SCPN.phone_id
        JOIN Contacts AS C_SMS
        ON C_SMS.contact_id = CPN.contact_id
        WHERE (C_SMS.contact_id = {contact_id} OR C_SMS.contact_id = {your_contact_id}) AND (Date BETWEEN '{start_date}' AND '{end_date}')"""

    query_5_mms = f"""
        SELECT
        CASE
            WHEN M.msg_box = '1' THEN C_MMS.first_name || ' ' || C_MMS.last_name
            WHEN M.msg_box = '2' THEN (SELECT first_name || ' ' || last_name FROM MeContact)
            ELSE 'ERROR !'
        END AS [Sender name],
        CASE
            WHEN M.msg_box = '1' THEN CPN2.phone
            WHEN M.msg_box = '2' THEN (SELECT phone FROM MeAddress)
            ELSE 'ERROR !'
        END AS [Sender address],
        'Destinataire direct' AS [Recipient type],
        CASE
            WHEN M.msg_box = '1' THEN (SELECT first_name || ' ' || last_name FROM MeContact)
            WHEN M.msg_box = '2' THEN C_MMS.first_name || ' ' || C_MMS.last_name
            ELSE 'ERROR !'
        END AS [Recipient name],
        CASE
            WHEN M.msg_box = '1' THEN (SELECT phone FROM MeAddress)
            WHEN M.msg_box = '2' THEN CPN2.phone
            ELSE 'ERROR !'
        END AS [Recipient address],
        M.date AS [Date],
        M.time AS [Time],
        'No subject' AS [Subject],
        'None' AS [Original filename],
        (
            SELECT text
            FROM MmsPart AS MP_sub
            JOIN Mms_MmsPart MMP_sub
            ON MP_sub.part_id = MMP_sub.part_id
            JOIN Mms As M_sub
            ON M_sub.mms_id = MMP_sub.mms_id
            WHERE MP_sub.seq = '0' and MP_sub.ct = 'text/plain' AND MP_sub.text != '' AND M_sub.mms_id = M.mms_id
            LIMIT 1
        ) AS [Content],
        (
        SELECT GROUP_CONCAT(cl, ', ')
        FROM (
            SELECT DISTINCT cl
            FROM MmsPart AS MP_sub
            JOIN Mms_MmsPart MMP_sub
            ON MP_sub.part_id = MMP_sub.part_id
            JOIN Mms As M_sub
            ON M_sub.mms_id = MMP_sub.mms_id
            WHERE MP_sub.seq = '0' and MP_sub.ct != 'text/plain' AND M_sub.mms_id = M.mms_id
            )
        ) AS [Attachments],
        (
            SELECT GROUP_CONCAT(T.tag, ', ')
            FROM Tags AS T
            LEFT JOIN MTM_Tags AS MTM_T
            ON MTM_T.tag_id = T.tag_id
            WHERE MTM_T.mms_id = M.mms_id
        ) AS [Tags],
        M.mms_id AS [Message id]
        FROM Mms As M
        JOIN Mms_ContactPhoneNumber AS MCPN
        ON MCPN.mms_id = M.mms_id
        JOIN ContactPhoneNumbers AS CPN2
        ON CPN2.phone_id = MCPN.phone_id
        JOIN Contacts AS C_MMS
        ON C_MMS.contact_id = CPN2.contact_id
        JOIN Mms_MmsPart AS MMP
        ON MMP.mms_id = M.mms_id
        JOIN MmsPart AS MP
        ON MP.part_id = MMP.part_id
        WHERE (C_MMS.contact_id = {contact_id} OR C_MMS.contact_id = {your_contact_id}) AND (Date BETWEEN '{start_date}' AND '{end_date}')"""

    #ToDo: "query_6_messenger" doit très probablement disparaître
    query_6_messenger = f"""
        SELECT
        C_M.first_name || ' ' || C_M.last_name AS [Sender name],
        C_MSNGR.surname AS [Sender address],
        G_M.group_name AS [Recipient type]
    FROM Messenger AS MSNGR
    JOIN ContactMessenger AS C_MSNGR
    ON C_MSNGR.surname_id = MSNGR.surname_id
    JOIN Contacts AS C_M
    ON C_M.contact_id = C_MSNGR.contact_id
    JOIN GroupMessenger AS G_M
    ON G_M.group_id = MSNGR.group_id
        """

    query = query_1_sms_with + query_2_emails + concat_where_email + union + query_4_sms + concat_where_sms + union + query_5_mms + concat_where_mms + order
    results = None
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print(f"\033[93mUne erreur s'est produite lors de la requête get_messages_between_dates : {e} \033[0m")

    messages = []
    if results:
        for result in results:
            message_obj = Message.Message(*result)
            messages.append(message_obj)
    return headers, messages

def get_contact_messenger(contact_id):
    query = f"""
    SELECT surname_id, surname FROM ContactMessenger WHERE contact_id = ?
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(query,(contact_id,))
    result = cursor.fetchone()
    return result

def get_groups_messenger_for_contact_messenger(surname_id):
    query_group_id = f"""
    SELECT group_id FROM MTM_GroupMessenger_ContactMessenger WHERE surname_id = ?
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(query_group_id, (surname_id,))
    g_ids = cursor.fetchall()
    group_ids = tuple([elem[0] for elem in g_ids])
    query_group = f"""
    SELECT * FROM GroupMessenger WHERE group_id IN {group_ids}
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(query_group)
    result = cursor.fetchall()
    return result

def get_messenger_for_group_ids(group_ids):

    query_messenger = f"""
    SELECT * FROM Messenger WHERE group_id IN {group_ids}
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(query_messenger)
    result = cursor.fetchall()
    return result



if __name__ == "__main__":
    surname_id, surname = get_contact_messenger(2)
    print(surname_id)
    ids__names = get_groups_messenger_for_contact_messenger(surname_id)
    group_ids = tuple([element[0] for element in ids__names])
    res = get_messenger_for_group_ids(group_ids)
    for r in res:
        print(r)



