import sqlite3
import csv
import os
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")
CSV_FILENAME = os.getenv("CSV_FILENAME")
CSV_TAGS = os.getenv("CSV_TAGS")


def add_contact(first_name, last_name):
    """
    Add a contact with the provided first name and last name to the database if it doesn't already exist.

    If a contact with the same first name and last name already exists in the database,
    it retrieves the ID of the existing contact. If not, it inserts a new contact record
    into the database and returns the ID of the newly created contact.

    Args:
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.

    Returns:
        int: The ID of the contact (either newly created or existing).
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Vérifier si le contact existe déjà
    query = f"""SELECT contact_id FROM Contacts WHERE first_name = ? AND last_name = ?"""
    cursor.execute(query, (first_name, last_name))
    existing_contact = cursor.fetchone()

    if existing_contact:
        # Si le contact existe, récupérer l'ID du contact existant
        contact_id = existing_contact[0]
        print(f"The contact already exists with ID: {contact_id}")
    else:
        # Si le contact n'existe pas, l'ajouter à la base de données
        query = f"""INSERT INTO Contacts (first_name, last_name)
                    VALUES (?, ?)"""
        cursor.execute(query, (first_name, last_name))
        # Récupérer l'ID généré automatiquement
        contact_id = cursor.lastrowid
        connection.commit()
        print(f"Inserted a new contact: {first_name} {last_name} with ID {contact_id}")

    connection.close()
    return contact_id


def update_contact(contact_id, first_name, last_name):
    """
    Update the contact with the provided contact_id, first name, and last name in the database.

    Args:
        contact_id (int): The ID of the contact to be updated.
        first_name (str): The updated first name of the contact.
        last_name (str): The updated last name of the contact.

    Returns:
        None
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""UPDATE Contacts
                SET first_name = ?,
                    last_name = ?
                WHERE contact_id = ?"""
    cursor.execute(query, (first_name, last_name, contact_id))
    connection.commit()
    connection.close()
    print(f"Contact updated: first name: {first_name}, last name: {last_name}, contact_id: {contact_id}")


def link_email_to_contact(email, contact_id):
    """
    Link an email address to a contact in the database, creating a link if the email doesn't exist.

    Args:
        email (str): The email address to be linked.
        contact_id (int): The ID of the contact to link the email to.

    Returns:
        None
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Vérifier d'abord si l'adresse e-mail existe dans la base de données
    cursor.execute("SELECT email FROM ContactEmails WHERE email = ?", (email,))
    retr_email = cursor.fetchone()

    if retr_email:
        # L'adresse e-mail existe déjà, nous pouvons la mettre à jour
        query = """UPDATE ContactEmails
                   SET contact_id = ?
                   WHERE email = ?"""
        cursor.execute(query, (contact_id, email))
    else:
        # L'adresse e-mail n'existe pas encore, nous pouvons l'ajouter
        query = """INSERT INTO ContactEmails (contact_id, email)
                   VALUES (?, ?)"""
        cursor.execute(query, (contact_id, email))

    connection.commit()
    connection.close()
    print(f"Contact_id: {contact_id} linked to email address: {email}")


def link_phone_to_contact(phone, contact_id):
    """
    Link a phone number to a contact in the database, creating a link if the phone number doesn't exist.

    Args:
        phone (str): The phone number to be linked.
        contact_id (int): The ID of the contact to link the phone number to.

    Returns:
        None
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Vérifier d'abord si le numéro de téléphone existe dans la base de données
    cursor.execute("SELECT phone FROM ContactPhoneNumbers WHERE phone = ?", (phone,))
    retr_phone = cursor.fetchone()

    if retr_phone:
        # Le numéro de téléphone existe déjà, nous pouvons le mettre à jour
        query = """UPDATE ContactPhoneNumbers
                   SET contact_id = ?
                   WHERE phone = ?"""
        cursor.execute(query, (contact_id, phone))
    else:
        # Le numéro de téléphone n'existe pas encore, nous pouvons l'ajouter
        query = """INSERT INTO ContactPhoneNumbers (contact_id, phone)
                   VALUES (?, ?)"""
        cursor.execute(query, (contact_id, phone))

    connection.commit()
    connection.close()
    print(f"Contact_id: {contact_id} linked to phonenumber: {phone}")


def insert_contacts_from_csv(csv_filename=CSV_FILENAME):
    """
     Insert contacts from a CSV file into the database.

     Args:
         csv_filename (str): The path to the CSV file containing contact information.

     Returns:
         None
     """
    # Check if CSV file exists
    if os.path.exists(csv_filename):
        with open(csv_filename, newline='') as csvfile:
            contacts = csv.DictReader(csvfile)
            for contact in contacts:
                first_name = contact['first_name']
                last_name = contact['last_name']
                phone_numbers = contact['phone_numbers'].split(',')
                email_addresses = contact['email_addresses'].split(',')
                contact_id = add_contact(first_name=first_name, last_name=last_name)
                for phone in phone_numbers:
                    link_phone_to_contact(phone=phone, contact_id=contact_id)
                for email_address in email_addresses:
                    link_email_to_contact(email=email_address, contact_id=contact_id)
    else:
        print(f"Le fichier {csv_filename} n'existe pas.")


def insert_tag(tag):
    """
    Insert a tag into the database if it doesn't already exist.

    Args:
        tag (str): The tag to be inserted.

    Returns:
        int: The ID of the inserted or existing tag.
    """
    query_get_tag_if_exist = f"""
        SELECT tag_id
        FROM Tags
        WHERE tag = '{tag}' """
    query_insert_tag = f"""
        INSERT INTO Tags
        (tag)
        VALUES (?)"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(query_get_tag_if_exist)
    tag_id = cursor.fetchone()
    if tag_id:
        tag_id = tag_id[0]
    else:
        cursor.execute(query_insert_tag, (tag,))
        tag_id = cursor.lastrowid
        connection.commit()
    print(f"Tag: {tag} inserted with tag_id: {tag_id}")
    return tag_id


def link_tag_to_message(tag, primary_key):
    """
    Link a tag to a message (email, SMS, or MMS) in the database.

    Args:
        tag (str): The tag to be linked.
        primary_key (int): The primary key (ID) of the message.

    Returns:
        None
    """
    table = None
    query_email = f"""
        SELECT message_id
        FROM Emails
        WHERE message_id = '{primary_key}' """

    query_sms = f"""
        SELECT sms_id
        FROM Sms
        WHERE sms_id = '{primary_key}'"""

    query_mms = f"""
        SELECT mms_id
        FROM Mms
        WHERE mms_id = '{primary_key}'"""

    query_insert_tag_email = f"""
        INSERT INTO MTM_Tags
        (message_id, tag_id)
        VALUES (?, ?)"""
    query_insert_tag_sms = f"""
        INSERT INTO MTM_Tags
        (sms_id, tag_id)
        VALUES (?, ?)"""
    query_insert_tag_mms = f"""
            INSERT INTO MTM_Tags
            (mms_id, tag_id)
            VALUES (?, ?)"""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(query_email)
    message_id = cursor.fetchone()

    cursor.execute(query_sms)
    sms_id = cursor.fetchone()

    cursor.execute(query_mms)
    mms_id = cursor.fetchone()

    # Get tag_id from Tags table
    tag_id = insert_tag(tag)

    query_get_mtm_message_id = f"""
            SELECT message_id, tag_id
            FROM MTM_Tags
            WHERE message_id = '{primary_key}' AND tag_id = {tag_id}"""

    query_get_mtm_sms_id = f"""
                SELECT sms_id, tag_id
                FROM MTM_Tags
                WHERE sms_id = '{primary_key}' AND tag_id = {tag_id}"""

    query_get_mtm_mms_id = f"""
                SELECT mms_id, tag_id
                FROM MTM_Tags
                WHERE mms_id = '{primary_key}' AND tag_id = {tag_id}"""

    if message_id:
        table = "Emails"
        message_id = message_id[0]
        # check if message_id already linked to tag_id
        cursor.execute(query_get_mtm_message_id)
        mtm_email = cursor.fetchone()
        if not mtm_email:
            cursor.execute(query_insert_tag_email, (message_id, tag_id))
            connection.commit()
    elif sms_id:
        table = "Sms"
        sms_id = sms_id[0]
        # check if sms_id already linked to tag_id
        cursor.execute(query_get_mtm_sms_id)
        mtm_sms = cursor.fetchone()
        if not mtm_sms:
            cursor.execute(query_insert_tag_sms, (sms_id, tag_id))
            connection.commit()
    elif mms_id:
        table = "Mms"
        mms_id = mms_id[0]
        # check if mms_id already linked to tag_id
        cursor.execute(query_get_mtm_mms_id)
        mtm_mms = cursor.fetchone()
        if not mtm_mms:
            cursor.execute(query_insert_tag_mms, (mms_id, tag_id))
            connection.commit()
    connection.close()
    print(f"Tag: {tag} linked to primary key: {primary_key} of table:{table}")


def insert_tags_from_csv(csv_tags=CSV_TAGS):
    """
    Insert tags from a CSV file and link them to messages in the database.

    Args:
        csv_tags (str): The path to the CSV file containing tag information and message IDs.

    Returns:
        None
    """
    # Check if CSV file exists
    if os.path.exists(csv_tags):
        with open(csv_tags, newline='') as csvtags:
            tags = csv.DictReader(csvtags)
            for row in tags:
                tag = row['tag']
                message_id = row['message_id']
                link_tag_to_message(tag=tag, primary_key=message_id)
    else:
        print(f"Le fichier {csv_tags} n'existe pas.")


if __name__ == "__main__":
    pass
    