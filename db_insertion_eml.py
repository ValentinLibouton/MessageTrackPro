import sqlite3
import os
from models import Email
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")
DB_TABLES = os.getenv("DB_TABLES")
TIMEZONE = os.getenv("TIMEZONE")


def create_primary_key(email_obj):
    """
    Creates a primary key for an Email object based on the sender's email address, date, and time.

    Args:
        email_obj (Email): An Email object for which to generate the primary key.

    Returns:
        str: The generated primary key.

    Note:
        The primary key is created by combining the sender's email address, date (in YYYYMMDD format), and time
        (in HHMMSS format), providing a unique identifier for the email.

    """
    if isinstance(email_obj, Email.Email):
        email_sender = email_obj.sender_email
        date = email_obj.strdate(timezone=TIMEZONE)
        time = email_obj.strtime(timezone=TIMEZONE)
        primary_key = f"{date}{time}{email_sender}"
        return primary_key


def check_value_existence(table_name, column_name, value):
    """
    Checks the existence of a specified value in a given table and column of the database.

    Args:
        table_name (str): The name of the database table to search.
        column_name (str): The name of the column within the table to search.
        value (str): The value to check for existence in the specified column.

    Returns:
        int or False: Returns the primary key (if found) associated with the specified value in the table,
        or False if the value is not found.

    Note:
        This function queries the database to check if a specified value exists in a given column of a table.
        If the value is found, it returns the primary key associated with that value; otherwise, it returns False.

    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
    cursor.execute(query, (value,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return False
    else:
        return row[0]


def add_email_address(str_email):
    """
    Adds an email address to the 'ContactEmails' table in the database if it doesn't already exist.

    Args:
        str_email (str): The email address to be added.

    Returns:
        int: The primary key (email_id) associated with the added email address.

    Note:
        This function first checks if the email address already exists in the 'ContactEmails' table of the database.
        If the email address is not found, it inserts the email address into the table and returns the associated
        primary key (email_id). If the email address already exists, it returns the existing email_id without
        inserting a new record.

    """
    email_id = None
    email_id = check_value_existence(table_name="ContactEmails", column_name="email", value=str_email)
    if not email_id:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ContactEmails (email) VALUES (?)", (str(str_email),))

        # Récupérer l'ID généré automatiquement
        new_row_id = cursor.lastrowid
        # Récupérer les données insérées
        cursor.execute("SELECT * FROM ContactEmails WHERE email_id = ?", (new_row_id,))
        new_row = cursor.fetchone()

        connection.commit()
        connection.close()
        email_id = new_row[0]
        print(f"Inserted in ContactEmails: email_id={new_row[0]}, contact_id={new_row[1]}, email={new_row[2]}")
    else:
        #print(f"{str_email} already exist in table ContactEmails with PK:{email_id}.")
        pass
    return email_id

def add_attachments(message_id, attachments_names_list=None):
    """
    This function should only be called by the 'add_email' function to avoid duplicate entries.

    Args:
        message_id (str): The message ID to associate with the attachments.
        attachments_names_list (list, optional): A list of attachment filenames. Defaults to None.

    Note:
        This function inserts attachment filenames associated with a given message ID into the 'Attachments' table
        of the database. It ensures that duplicate entries are not created. It should typically be called by the
        'add_email' function to manage email attachments.

    """
    if attachments_names_list:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        for attachment_name in attachments_names_list:
            query = f"INSERT INTO Attachments (message_id, filename) VALUES (?, ?)"
            cursor.execute(query, (message_id, attachment_name))

            # Récupérer l'ID généré automatiquement
            new_row_id = cursor.lastrowid

            # Récupérer les données insérées
            cursor.execute("SELECT * FROM Attachments WHERE attachments_id = ?", (new_row_id,))
            new_row = cursor.fetchone()

            #print(f"Inserted in Attachments: attachments_id={new_row[0]}, message_id={new_row[1]}, filename={new_row[2]}")
        connection.commit()
        connection.close()


def add_recipient_list(message_id, email_obj):
    """
    Add recipients (To, Cc, and Bcc) of an email to the 'RecipientEmails' table in the database.

    Args:
        message_id (str): The message ID to associate with the recipients.
        email_obj (Email): An instance of the 'Email' class containing email details.

    Note:
        This function inserts recipient email addresses into the 'RecipientEmails' table of the database,
        associating them with a given message ID. It distinguishes between To, Cc, and Bcc recipients and sets
        appropriate flags for each. Duplicate email addresses are avoided by using the 'add_email_address' function.
    """
    recipient_to = email_obj.recipients_to
    recipient_cc = email_obj.recipients_cc
    recipient_bcc = email_obj.recipients_bcc
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    for recipient in recipient_to:
        email_id = add_email_address(recipient)
        cursor.execute("INSERT INTO RecipientEmails (message_id, email_id, is_cc, is_bcc) VALUES (?, ?, ?, ?)",
                       (message_id, email_id, 0, 0))
        # Récupérer l'ID généré automatiquement
        new_row_id = cursor.lastrowid
        # Récupérer les données insérées
        cursor.execute("SELECT * FROM RecipientEmails WHERE recipient_id = ?", (new_row_id, ))
        new_row = cursor.fetchone()
        connection.commit()
        #print(f"Inserted in RecipientEmails: recipient_id={new_row[0]}, message_id={new_row[1]}, email_id={new_row[2]}, is_cc={new_row[3]}, is_bcc={new_row[4]}")
    if recipient_cc:
        for recipient in recipient_cc:
            email_id = add_email_address(recipient)
            cursor.execute("INSERT INTO RecipientEmails (message_id, email_id, is_cc, is_bcc) VALUES (?, ?, ?, ?)",
                           (message_id, email_id, 1, 0))
            # Récupérer l'ID généré automatiquement
            new_row_id = cursor.lastrowid
            # Récupérer les données insérées
            cursor.execute("SELECT * FROM RecipientEmails WHERE recipient_id = ?", (new_row_id, ))
            new_row = cursor.fetchone()
            connection.commit()
            #print(f"Inserted in RecipientEmails: recipient_id={new_row[0]}, message_id={new_row[1]}, email_id={new_row[2]}, is_cc={new_row[3]}, is_bcc={new_row[4]}")
    if recipient_bcc:
        for recipient in recipient_bcc:
            email_id = add_email_address(recipient)
            cursor.execute("INSERT INTO RecipientEmails (message_id, email_id, is_cc, is_bcc) VALUES (?, ?, ?, ?)",
                           (message_id, email_id, 0, 1))
            # Récupérer l'ID généré automatiquement
            new_row_id = cursor.lastrowid
            # Récupérer les données insérées
            cursor.execute("SELECT * FROM RecipientEmails WHERE recipient_id = ?", (new_row_id, ))
            new_row = cursor.fetchone()
            connection.commit()
            #print(f"Inserted in RecipientEmails: recipient_id={new_row[0]}, message_id={new_row[1]}, email_id={new_row[2]}, is_cc={new_row[3]}, is_bcc={new_row[4]}")
    connection.close()


def add_email(email_obj):
    """
    Adds an email to the database.

    Args:
        email_obj (Email): An instance of the 'Email' class containing email details.

    Note:
        This function inserts the details of an email, including the message ID, sender, date, time, subject, content,
        original filename, and recipients into the database. Email addresses are inserted into the 'ContactEmails' table
        using the 'add_email_address' function. Attachments are added using the 'add_attachments' function, and recipients
        are inserted using the 'add_recipient_list' function.
    """
    if isinstance(email_obj, Email.Email):
        primary_key = create_primary_key(email_obj=email_obj)
        if not check_value_existence(table_name="Emails", column_name="message_id", value=primary_key):
            sender_email_id = add_email_address(str_email=email_obj.sender_email)

            connection = sqlite3.connect(DB_NAME)
            cursor = connection.cursor()
            query = f"""INSERT INTO Emails (message_id, sender_email_id, date, time, subject, content, original_filename)
                        VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, (primary_key, sender_email_id, str(email_obj.date(timezone=TIMEZONE)), str(email_obj.time(timezone=TIMEZONE)), email_obj.subject, email_obj.body, email_obj.filename))
            connection.commit()
            connection.close()
            # ToDo: je dois adapter pour faire fonctionne ce qu'il y a ci-dessous
            add_attachments(message_id=primary_key, attachments_names_list=email_obj.attachments_names)
            add_recipient_list(message_id=primary_key, email_obj=email_obj)


if __name__ == "__main__":
    pass