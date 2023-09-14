import sqlite3
import os
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")
DB_TABLES = os.getenv("DB_TABLES")

def create_primary_key(eml_dict):
    email_sender = eml_dict['email_sender']
    date = eml_dict['date']
    time = eml_dict['time']
    primary_key = f"{date}{time}{email_sender}"
    return primary_key

def check_value_existence(table_name, column_name, value):
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
    email_id = None
    email_id = check_value_existence(table_name="ContactEmails", column_name="email", value=str_email)
    if not email_id:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ContactEmails (email) VALUES (?)", (str_email,))

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
        print(f"{str_email} already exist in table ContactEmails with PK:{email_id}.")
    return email_id

def add_attachments(message_id, attachments_names_list=None):
    """
    Cette fonction ne peut être appellée que par la fonction add_email afin d'éviter des doublons de ligne
    :param message_id:
    :param attachments_names_list:
    :return:
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

            print(f"Inserted in Attachments: attachments_id={new_row[0]}, message_id={new_row[1]}, filename={new_row[2]}")
        connection.commit()
        connection.close()
def add_recipient_list(message_id, eml_dict):
    recipient_to = eml_dict['recipient_to']
    recipient_cc = eml_dict['recipient_cc']
    recipient_bcc = eml_dict['recipient_bcc']
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
        print(f"Inserted in RecipientEmails: recipient_id={new_row[0]}, message_id={new_row[1]}, email_id={new_row[2]}, is_cc={new_row[3]}, is_bcc={new_row[4]}")

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
        print(f"Inserted in RecipientEmails: recipient_id={new_row[0]}, message_id={new_row[1]}, email_id={new_row[2]}, is_cc={new_row[3]}, is_bcc={new_row[4]}")

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
        print(f"Inserted in RecipientEmails: recipient_id={new_row[0]}, message_id={new_row[1]}, email_id={new_row[2]}, is_cc={new_row[3]}, is_bcc={new_row[4]}")


    connection.close()

def add_email(eml_dict):
    if eml_dict:
        primary_key = create_primary_key(eml_dict=eml_dict)
        if not check_value_existence(table_name="Emails", column_name="message_id", value=primary_key):
            sender_email_id = add_email_address(eml_dict['email_sender'])

            connection = sqlite3.connect(DB_NAME)
            cursor = connection.cursor()
            query = f"""INSERT INTO Emails (message_id, sender_email_id, date, time, subject, content, original_filename)
                        VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, (primary_key, sender_email_id, eml_dict['date'], eml_dict['time'], eml_dict['subject'], eml_dict['content'], eml_dict['original_filename']))
            connection.commit()
            connection.close()
            add_attachments(message_id=primary_key, attachments_names_list=eml_dict['attachments_names'])
            add_recipient_list(message_id=primary_key, eml_dict=eml_dict)

if __name__ == "__main__":
    pass