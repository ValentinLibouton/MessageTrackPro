import sqlite3
import datetime
import os
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")
def create_primary_key(mms):
    """
    :param mm: object
    :return:
    """
    primary_key = f"{mms.date}{mms.date_sent}"
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

def mtm_mms_id_phone_id(mms_id, phone_ids):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    for phone_id in phone_ids:
        cursor.execute("SELECT COUNT (*) FROM Mms_ContactPhoneNumber WHERE mms_id = ? AND phone_id = ?", (mms_id, phone_id))
        occurence = cursor.fetchone()[0]
        if occurence == 0:
            query = f"INSERT INTO Mms_ContactPhoneNumber (mms_id, phone_id) VALUES (?, ?)"
            cursor.execute(query, (mms_id, phone_id))
            connection.commit()
    connection.close()


def add_part(part):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""INSERT INTO MmsPart (text, seq, ct, name, chset, cd, fn, cid, cl, ctt_s, ctt_t, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (part.text, part.seq, part.ct, part.name, part.chset, part.cd, part.fn, part.cid, part.cl,
                        part.ctt_s, part.ctt_t, part.data))
    # Récupérer l'ID généré automatiquement
    part_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return part_id

def mtm_mms_id_part_id(mms_id, part_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""INSERT INTO Mms_MmsPart (mms_id, part_id) VALUES (?, ?)"""
    cursor.execute(query, (mms_id, part_id))
    connection.commit()
    connection.close()

def add_mmsaddr(addr):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""INSERT INTO MmsAddr (address, type, charset) VALUES (?, ?, ?)"""
    cursor.execute(query, (addr.address, addr.type, addr.charset))
    # Récupérer l'ID généré automatiquement
    addr_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return addr_id

def mtm_mms_id_addr_id(mms_id, addr_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""INSERT INTO Mms_MmsAddr (mms_id, addr_id) VALUES (?, ?)"""
    cursor.execute(query, (mms_id, addr_id))
    connection.commit()
    connection.close()


def add_mmses(mms_list):
    for mms in mms_list:
        primary_key = create_primary_key(mms=mms)
        if mms.msg_box == "1":
            msg_box_str = "Received"
        elif mms.msg_box == "2":
            msg_box_str = "Sent"
        date, time = format_date_time(mms.date)

        # Liste pour stocker les ID des numéros de téléphone liés à ce SMS
        phone_ids = []

        # Adresse du SMS (peut contenir plusieurs numéros)
        address = mms.address
        if len(address) > 18:
            addresses = address.split(' ')
            for address in addresses:
                phone_id = add_address(str_address=address)
                phone_ids.append(phone_id)
        else:
            address = address.replace(' ', '')
            phone_id = add_address(str_address=address)
            phone_ids.append(phone_id)

        mtm_mms_id_phone_id(mms_id=primary_key, phone_ids=phone_ids)
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT (*) FROM Mms WHERE mms_id = ?", (primary_key,))
        occurence = cursor.fetchone()[0]
        if occurence == 0:
            query = f"""INSERT INTO Mms (mms_id, msg_box_str, date, time, contact_name, rr, sub, ct_t, read_status, seen,
                            msg_box, sub_cs, resp_st, retr_st, d_tm, text_only, exp, locked, m_id, st, retr_txt_cs, retr_txt,
                            creator, date_sent, read, m_size, rpt_a, ct_cls, pri, sub_id, tr_id, resp_txt, ct_l, m_cls, d_rpt,
                            v, _id, m_type, readable_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            cursor.execute(query, (primary_key, msg_box_str, date, time, mms.contact_name, mms.rr, mms.sub, mms.ct_t, mms.read_status, mms.seen,
                                   mms.msg_box, mms.sub_cs, mms.resp_st, mms.retr_st, mms.d_tm, mms.text_only, mms.exp, mms.locked, mms.m_id, mms.st,
                                   mms.retr_txt_cs, mms.retr_txt,
                                   mms.creator, mms.date_sent, mms.read, mms.m_size, mms.rpt_a, mms.ct_cls, mms.pri, mms.sub_id, mms.tr_id, mms.resp_txt, mms.ct_l,
                                   mms.m_cls, mms.d_rpt,
                                   mms.v, mms._id, mms.m_type, mms.readable_date))
            connection.commit()
            # ToDo: Je dois m'assurer que tout est ok ci-dessous!
            for part in mms.parts:
                part_id = add_part(part=part)
                # Creation of the link between tables
                mtm_mms_id_part_id(mms_id=primary_key, part_id=part_id)
            for addr in mms.addrs:
                addr_id = add_mmsaddr(addr=addr)
                # Creation of the link between tables
                mtm_mms_id_addr_id(mms_id=primary_key, addr_id=addr_id)

        connection.close()



