import sqlite3
import datetime
import os
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")
def create_primary_key(sms):
    """
    :param sms: object
    :return:
    """
    primary_key = f"{sms.date}{sms.date_sent}"
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

def add_address(str_address):
    phone_id = None
    phone_id = check_value_existence(table_name="ContactPhoneNumbers", column_name="phone", value=str_address)
    if not phone_id:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO ContactPhoneNumbers (phone) VALUES (?)", (str_address,))

        # Récupérer l'ID généré automatiquement
        new_row_id = cursor.lastrowid

        # Récupérer les données insérées
        cursor.execute("SELECT * FROM ContactPhoneNumbers WHERE phone_id = ?", (new_row_id,))
        new_row = cursor.fetchone()

        connection.commit()
        connection.close()
        email_id = new_row[0]
        print(f"Inserted in ContactPhoneNumbers: phone_id={new_row[0]}, contact_id={new_row[1]}, phone={new_row[2]}")
    else:
        print(f"{str_address} already exist in table ContactPhoneNumbers with PK:{phone_id}.")
    return phone_id

def format_date_time(timestamp):
    # Convertir la timestamp en objet datetime
    date_obj = datetime.datetime.fromtimestamp(int(timestamp) / 1000.0)  # Divisé par 1000 car la timestamp est en millisecondes

    # Extraire la date et l'heure au format YYYYMMDD et HHMMSS
    date_format = date_obj.strftime("%Y%m%d")
    time_format = date_obj.strftime("%H%M%S")
    return date_format, time_format

def mtm_sms_id_phone_id(sms_id, phone_ids):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    for phone_id in phone_ids:
        cursor.execute("SELECT COUNT (*) FROM Sms_ContactPhoneNumber WHERE sms_id = ? AND phone_id = ?", (sms_id, phone_id))
        occurence = cursor.fetchone()[0]
        if occurence == 0:
            query = f"INSERT INTO Sms_ContactPhoneNumber (sms_id, phone_id) VALUES (?, ?)"
            cursor.execute(query, (sms_id, phone_id))
            connection.commit()
    connection.close()


def add_sms(primary_key, type_str, date, time, contact_name, phone_ids, body, protocol, type, subject, toa, sc_toa,
            service_center, read, status, locked, date_sent, sub_id, readable_date):
    mtm_sms_id_phone_id(sms_id=primary_key, phone_ids=phone_ids)
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT (*) FROM Sms WHERE sms_id = ?", (primary_key,))
    occurence = cursor.fetchone()[0]
    if occurence == 0:
        query = f"INSERT INTO Sms (sms_id, type_str, date, time, contact_name, body, protocol, type, subject, toa," \
                f"sc_toa, service_center, read, status, locked, date_sent, sub_id, readable_date)" \
                f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        cursor.execute(query, (primary_key, type_str, date, time, contact_name, body, protocol, type, subject, toa,
                               sc_toa, service_center, read, status, locked, date_sent, sub_id, readable_date))
    connection.commit()
    connection.close()
def add_smses(sms_list):
    type_str = None
    for sms in sms_list:
        primary_key = create_primary_key(sms=sms)
        if sms.type == "1":
            type_str = "Received"
        elif sms.type == "2":
            type_str = "Sent"
        date, time = format_date_time(sms.date)
        contact_name = sms.contact_name

        # Liste pour stocker les ID des numéros de téléphone liés à ce SMS
        phone_ids = []

        # Adresse du SMS (peut contenir plusieurs numéros)
        address = sms.address
        if len(address) > 18:
            addresses = address.split(' ')
            for address in addresses:
                phone_id = add_address(str_address=address)
                phone_ids.append(phone_id)
        else:
            address = address.replace(' ', '')
            phone_id = add_address(str_address=address)
            phone_ids.append(phone_id)
        add_sms(primary_key=primary_key, type_str=type_str, date=date, time=time, contact_name=contact_name,
                phone_ids=phone_ids, body=sms.body, protocol=sms.protocol, type=sms.type, subject=sms.subject, toa=sms.toa,
                sc_toa=sms.sc_toa, service_center=sms.service_center, read=sms.read, status=sms.status,
                locked=sms.locked, date_sent=sms.date_sent, sub_id=sms.sub_id, readable_date=sms.readable_date)

