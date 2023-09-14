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

def add_contact(first_name, last_name):
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
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""UPDATE Contacts
                SET first_name = ?,
                    last_name = ?
                WHERE contact_id = ?"""
    cursor.execute(query, (first_name, last_name, contact_id))
    connection.commit()
    connection.close()

def link_email_to_contact(email, contact_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""UPDATE ContactEmails
                SET contact_id = ?
                WHERE email = ?"""
    cursor.execute(query, (contact_id, email))
    connection.commit()
    connection.close()

def link_phone_to_contact(phone, contact_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""UPDATE ContactPhoneNumbers
                    SET contact_id = ?
                    WHERE phone = ?"""
    cursor.execute(query, (contact_id, phone))
    connection.commit()
    connection.close()

def insert_contacts_from_csv():
    with open(CSV_FILENAME, newline='') as csvfile:
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


if __name__ == "__main__":
    #--- Examples ---#
    #add_contact(first_name="Valentin", last_name="Lbtn")
    #update_contact(contact_id=1, first_name="Valentin", last_name="Libouton")
    #link_email_to_contact(email='valentin.libouton.git.des8s@8shield.net', contact_id=1)
    #link_phone_to_contact(phone="+32487123456", contact_id=3)
    