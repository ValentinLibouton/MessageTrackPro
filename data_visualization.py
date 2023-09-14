import sqlite3
import os
import Message
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")
YOURPHONENUMBER = os.getenv("YOURPHONENUMBER")


def get_contact_id(first_name, last_name):
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

def get_email_id(email):
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
    emails_list= []
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

def get_messages_linked_to_contact_id(contact_id):
    """
    

    :param contact_id:
    :return:
    """

    headers = ['Sender name', 'Sender address', 'Recipient type', 'Recipient name', 'Recipient address', "Date", "Time",
               "Original filename", "Content", "Attachments"]
    messages_list = []
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    query_your_contact_id = f"""SELECT contact_id
                                FROM ContactPhoneNumbers
                                WHERE phone = ?"""
    cursor.execute(query_your_contact_id, (YOURPHONENUMBER,))
    your_contact_id = cursor.fetchone()
    if your_contact_id:
        your_contact_id = your_contact_id[0]


    query_1_sms_with = f"""WITH MeContact AS (
                                SELECT *
                            FROM Contacts
                            WHERE contact_id = {your_contact_id}),
                        MeAddress AS (
                            SELECT *
                            FROM ContactPhoneNumbers
                            WHERE contact_id = {your_contact_id})"""

    query_2_emails = f""" SELECT   C.first_name || ' ' || C.last_name AS [Sender Name],
                            CE.email [Sender Address],
                            CASE
                                WHEN RE.is_cc = 0 AND RE.is_bcc = 0 THEN 'Destinataire direct'
                                WHEN RE.is_cc = 1 AND RE.is_bcc = 0 THEN 'Destinataire en copie'
                                WHEN RE.is_cc = 0 AND RE.is_bcc = 1 THEN 'Destinataire caché'
                                ELSE 'Autre' -- Gérer d'autres cas si nécessaire
                            END AS "Recipient Type",
                            C_RE.first_name || ' ' || C_RE.last_name AS [Recipient name],
                            CE_RE.email [Recipient Email],
                            E.date AS [Date],
                            E.time AS [Time],
                            E.original_filename AS [Original filename],
                            E.content AS [Content],
                            (
                                SELECT GROUP_CONCAT(filename, ', ')
                                FROM Attachments AS A
                                WHERE A.message_id = E.message_id
                            )
                    FROM Contacts AS C
                    JOIN ContactEmails AS CE
                    ON CE.contact_id = C.contact_id
                    JOIN Emails AS E
                    ON E.sender_email_id = CE.email_id
                    JOIN RecipientEmails AS RE
                    ON RE.message_id = E.message_id
                    JOIN ContactEmails AS CE_RE
                    ON CE_RE.email_id = RE.email_id
                    JOIN Contacts AS C_RE
                    ON C_RE.contact_id = CE_RE.contact_id
                    JOIN Attachments AS A
                    ON A.message_id = E.message_id
                    WHERE C.contact_id = {contact_id}
                    
                    UNION
                    
                    SELECT  C2.first_name || ' ' || C2.last_name AS [Sender Name],
                            CE2.email [Sender Address],
                            CASE
                                WHEN RE2.is_cc = 0 AND RE2.is_bcc = 0 THEN 'Destinataire direct'
                                WHEN RE2.is_cc = 1 AND RE2.is_bcc = 0 THEN 'Destinataire en copie'
                                WHEN RE2.is_cc = 0 AND RE2.is_bcc = 1 THEN 'Destinataire caché'
                                ELSE 'Autre' -- Gérer d'autres cas si nécessaire
                            END AS "Recipient Type",
                            C_RE2.first_name || ' ' || C_RE2.last_name AS [Recipient name],
                            CE_RE2.email [Recipient Email],
                            E2.date AS [Date],
                            E2.time AS [Time],
                            E2.original_filename AS [Original filename],
                            E2.content AS [Content],
                            (
                                SELECT GROUP_CONCAT(filename, ', ')
                                FROM Attachments AS A2
                                WHERE A2.message_id = E2.message_id
                            )
                            
                    FROM Contacts AS C_RE2
                    JOIN ContactEmails AS CE_RE2
                    ON CE_RE2.contact_id = C_RE2.contact_id
                    JOIN RecipientEmails AS RE2
                    ON RE2.email_id = CE_RE2.email_id
                    JOIN Emails AS E2
                    ON E2.message_id = RE2.message_id
                    JOIN ContactEmails AS CE2
                    ON CE2.email_id = E2.sender_email_id
                    JOIN Contacts AS C2
                    ON C2.contact_id = CE2.contact_id
                    JOIN Attachments AS A2
                    ON A2.message_id = E2.message_id
                    
                    WHERE C_RE2.contact_id = {contact_id} """

    query_3_union = f"""
                        UNION
                        """

    query_4_sms = f"""  SELECT
                            CASE
                                WHEN S.type = "1" THEN C_SMS.first_name || ' ' || C_SMS.last_name
                                WHEN S.type = "2" THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                                ELSE 'ERROR !'
                            END AS [Sender Name],
                            CASE
                                WHEN S.type = "1" THEN CPN.phone
                                WHEN S.type = "2" THEN (SELECT phone FROM MeAddress)
                                ELSE 'ERROR !'
                            END AS [Sender Address],
                            'Destinataire direct' AS [Recipient Type],
                            CASE
                                WHEN S.type = "1" THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                                WHEN S.type = "2" THEN C_SMS.first_name || ' ' || C_SMS.last_name
                                ELSE 'ERROR !'
                            END AS [Recipient Name],
                            CASE
                                WHEN S.type = "1" THEN (SELECT phone FROM MeAddress)
                                WHEN S.type = "2" THEN CPN.phone
                                ELSE 'ERROR !'
                            END AS [Recipient Address],
                            S.date AS [Date],
                            S.time AS [Time],
                            S.original_filename AS [Original filename],
                            S.body AS [Content],
                            '' AS [Attachments]
                            
                            
                        FROM Sms AS S
                        JOIN Sms_ContactPhoneNumber AS SCPN
                        ON SCPN.sms_id = S.sms_id
                        JOIN ContactPhoneNumbers AS CPN
                        ON CPN.phone_id = SCPN.phone_id
                        JOIN Contacts AS C_SMS
                        ON C_SMS.contact_id = CPN.contact_id
                        WHERE C_SMS.contact_id = {contact_id} """

    query_5_union = f"""
                        UNION
                        """

    query_6_mms = f"""
                        SELECT
                        CASE
                            WHEN M.msg_box = "1" THEN C_MMS.first_name || ' ' || C_MMS.last_name
                            WHEN M.msg_box = "2" THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                            ELSE 'ERROR !'
                        END AS [Sender Name],
                        CASE
                            WHEN M.msg_box = "1" THEN CPN2.phone
                            WHEN M.msg_box = "2" THEN (SELECT phone FROM MeAddress)
                            ELSE 'ERROR !'
                        END AS [Sender Address],
                        'Destinataire direct' AS [Recipient Type],
                        CASE
                            WHEN M.msg_box = "1" THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                            WHEN M.msg_box = "2" THEN C_MMS.first_name || ' ' || C_MMS.last_name
                            ELSE 'ERROR !'
                        END AS [Recipient Name],
                        CASE
                            WHEN M.msg_box = "1" THEN (SELECT phone FROM MeAddress)
                            WHEN M.msg_box = "2" THEN CPN2.phone
                            ELSE 'ERROR !'
                        END AS [Recipient Address],
                        M.date AS [Date],
                        M.time AS [Time],
                        '' AS [Original filename],
                        (
                            SELECT text
                            FROM MmsPart AS MP_sub
                            JOIN Mms_MmsPart MMP_sub
                            ON MP_sub.part_id = MMP_sub.part_id
                            JOIN Mms As M_sub
                            ON M_sub.mms_id = MMP_sub.mms_id
                            WHERE MP_sub.seq = "0" and MP_sub.ct = "text/plain" AND MP_sub.text != '' AND M_sub.mms_id = M.mms_id
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
                            WHERE MP_sub.seq = "0" and MP_sub.ct != "text/plain" AND M_sub.mms_id = M.mms_id
                        )
                    ) AS [Attachments]
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
                    WHERE C_MMS.contact_id = {contact_id}
                    GROUP BY M.mms_id
                """

    query_end_order = f"""
                        ORDER BY Date, Time
                        """

    query = query_1_sms_with + query_2_emails + query_3_union + query_4_sms + query_5_union + query_6_mms + query_end_order

    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        for result in results:
            messages_list.append(result)

    return headers, messages_list


def find_messages_with_word(contact_id, word):
    """

    :param contact_id: type(int)
    :param word: type(str)
    :return: headers type(list), messages_list type(list)
    """

    headers = ['Sender name', 'Sender address', 'Recipient type', 'Recipient name', 'Recipient address', "Date", "Time",
               "Original filename", "Content", "Attachments"]
    messages_list = []
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    query_your_contact_id = f"""SELECT contact_id
                                FROM ContactPhoneNumbers
                                WHERE phone = ?"""
    cursor.execute(query_your_contact_id, (YOURPHONENUMBER,))
    your_contact_id = cursor.fetchone()
    if your_contact_id:
        your_contact_id = your_contact_id[0]

    query_1_sms_with = f"""WITH MeContact AS (
                                SELECT *
                            FROM Contacts
                            WHERE contact_id = {your_contact_id}),
                        MeAddress AS (
                            SELECT *
                            FROM ContactPhoneNumbers
                            WHERE contact_id = {your_contact_id})"""

    query_2_emails = f""" SELECT   C.first_name || ' ' || C.last_name AS [Sender Name],
                            CE.email [Sender Address],
                            CASE
                                WHEN RE.is_cc = 0 AND RE.is_bcc = 0 THEN 'Destinataire direct'
                                WHEN RE.is_cc = 1 AND RE.is_bcc = 0 THEN 'Destinataire en copie'
                                WHEN RE.is_cc = 0 AND RE.is_bcc = 1 THEN 'Destinataire caché'
                                ELSE 'Autre' -- Gérer d'autres cas si nécessaire
                            END AS "Recipient Type",
                            C_RE.first_name || ' ' || C_RE.last_name AS [Recipient name],
                            CE_RE.email [Recipient Email],
                            E.date AS [Date],
                            E.time AS [Time],
                            E.original_filename AS [Original filename],
                            E.content AS [Content],
                            (
                                SELECT GROUP_CONCAT(filename, ', ')
                                FROM Attachments AS A
                                WHERE A.message_id = E.message_id
                            )
                    FROM Contacts AS C
                    JOIN ContactEmails AS CE
                    ON CE.contact_id = C.contact_id
                    JOIN Emails AS E
                    ON E.sender_email_id = CE.email_id
                    JOIN RecipientEmails AS RE
                    ON RE.message_id = E.message_id
                    JOIN ContactEmails AS CE_RE
                    ON CE_RE.email_id = RE.email_id
                    JOIN Contacts AS C_RE
                    ON C_RE.contact_id = CE_RE.contact_id
                    JOIN Attachments AS A
                    ON A.message_id = E.message_id
                    WHERE C.contact_id = {contact_id} AND E.content LIKE '%{word}%'

                    UNION

                    SELECT  C2.first_name || ' ' || C2.last_name AS [Sender Name],
                            CE2.email [Sender Address],
                            CASE
                                WHEN RE2.is_cc = 0 AND RE2.is_bcc = 0 THEN 'Destinataire direct'
                                WHEN RE2.is_cc = 1 AND RE2.is_bcc = 0 THEN 'Destinataire en copie'
                                WHEN RE2.is_cc = 0 AND RE2.is_bcc = 1 THEN 'Destinataire caché'
                                ELSE 'Autre' -- Gérer d'autres cas si nécessaire
                            END AS "Recipient Type",
                            C_RE2.first_name || ' ' || C_RE2.last_name AS [Recipient name],
                            CE_RE2.email [Recipient Email],
                            E2.date AS [Date],
                            E2.time AS [Time],
                            E2.original_filename AS [Original filename],
                            E2.content AS [Content],
                            (
                                SELECT GROUP_CONCAT(filename, ', ')
                                FROM Attachments AS A2
                                WHERE A2.message_id = E2.message_id
                            )

                    FROM Contacts AS C_RE2
                    JOIN ContactEmails AS CE_RE2
                    ON CE_RE2.contact_id = C_RE2.contact_id
                    JOIN RecipientEmails AS RE2
                    ON RE2.email_id = CE_RE2.email_id
                    JOIN Emails AS E2
                    ON E2.message_id = RE2.message_id
                    JOIN ContactEmails AS CE2
                    ON CE2.email_id = E2.sender_email_id
                    JOIN Contacts AS C2
                    ON C2.contact_id = CE2.contact_id
                    JOIN Attachments AS A2
                    ON A2.message_id = E2.message_id

                    WHERE C_RE2.contact_id = {contact_id} AND E2.content LIKE '%{word}%'"""

    query_3_union = f""" UNION """

    query_4_sms = f"""  SELECT
                            CASE
                                WHEN S.type = "1" THEN C_SMS.first_name || ' ' || C_SMS.last_name
                                WHEN S.type = "2" THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                                ELSE 'ERROR !'
                            END AS [Sender Name],
                            CASE
                                WHEN S.type = "1" THEN CPN.phone
                                WHEN S.type = "2" THEN (SELECT phone FROM MeAddress)
                                ELSE 'ERROR !'
                            END AS [Sender Address],
                            'Destinataire direct' AS [Recipient Type],
                            CASE
                                WHEN S.type = "1" THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                                WHEN S.type = "2" THEN C_SMS.first_name || ' ' || C_SMS.last_name
                                ELSE 'ERROR !'
                            END AS [Recipient Name],
                            CASE
                                WHEN S.type = "1" THEN (SELECT phone FROM MeAddress)
                                WHEN S.type = "2" THEN CPN.phone
                                ELSE 'ERROR !'
                            END AS [Recipient Address],
                            S.date AS [Date],
                            S.time AS [Time],
                            S.original_filename AS [Original filename],
                            S.body AS [Content],
                            "" AS [Attachments]


                        FROM Sms AS S
                        JOIN Sms_ContactPhoneNumber AS SCPN
                        ON SCPN.sms_id = S.sms_id
                        JOIN ContactPhoneNumbers AS CPN
                        ON CPN.phone_id = SCPN.phone_id
                        JOIN Contacts AS C_SMS
                        ON C_SMS.contact_id = CPN.contact_id
                        WHERE C_SMS.contact_id = {contact_id} AND S.body LIKE '%{word}%'"""

    query_5_union = f""" UNION """

    query_6_mms = f"""SELECT
                        CASE
                            WHEN M.msg_box = "1" THEN C_MMS.first_name || ' ' || C_MMS.last_name
                            WHEN M.msg_box = "2" THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                            ELSE 'ERROR !'
                        END AS [Sender Name],
                        CASE
                            WHEN M.msg_box = "1" THEN CPN2.phone
                            WHEN M.msg_box = "2" THEN (SELECT phone FROM MeAddress)
                            ELSE 'ERROR !'
                        END AS [Sender Address],
                        'Destinataire direct' AS [Recipient Type],
                        CASE
                            WHEN M.msg_box = "1" THEN (SELECT first_name || ' ' || last_name FROM MeContact)
                            WHEN M.msg_box = "2" THEN C_MMS.first_name || ' ' || C_MMS.last_name
                            ELSE 'ERROR !'
                        END AS [Recipient Name],
                        CASE
                            WHEN M.msg_box = "1" THEN (SELECT phone FROM MeAddress)
                            WHEN M.msg_box = "2" THEN CPN2.phone
                            ELSE 'ERROR !'
                        END AS [Recipient Address],
                        M.date AS [Date],
                        M.time AS [Time],
                        '' AS [Original filename],
                        (
                            SELECT text
                            FROM MmsPart AS MP_sub
                            JOIN Mms_MmsPart MMP_sub
                            ON MP_sub.part_id = MMP_sub.part_id
                            JOIN Mms As M_sub
                            ON M_sub.mms_id = MMP_sub.mms_id
                            WHERE MP_sub.seq = "0" and MP_sub.ct = "text/plain" AND MP_sub.text != '' AND M_sub.mms_id = M.mms_id
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
                            WHERE MP_sub.seq = "0" and MP_sub.ct != "text/plain" AND M_sub.mms_id = M.mms_id
                        )
                    ) AS [Attachments]
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
                    WHERE C_MMS.contact_id = {contact_id} AND MP_sub.text LIKE '%{word}%'
                    GROUP BY M.mms_id
                """
    query_end_order = f""" ORDER BY Date, Time """

    query = query_1_sms_with + query_2_emails + query_3_union + query_4_sms + query_5_union + query_6_mms + query_end_order

    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        for result in results:
            messages_list.append(result)

    return headers, messages_list

def find_by_tags(tags):
    pass








if __name__ == "__main__":
    #print(get_contact_id(first_name="Valentin", last_name="Libouton"))
    #print(get_email_id("valentin.libouton.git.des8s@8shield.net"))
    #print(get_emails_addresses_linked_to_contact_id(contact_id=2))
    headers, messages = get_messages_linked_to_contact_id(contact_id=3)
    for message in messages:
        print(message)

