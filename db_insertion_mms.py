import sqlite3
import os
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")
def create_primary_key(mms):
    """
    Creates a primary key for an MMS message based on its attributes.

    Args:
        mms (MMS): The MMS message for which the primary key is generated.

    Returns:
        str: A unique primary key for the MMS message.

    Example:
        mms = MMS(date='2023-08-30 14:30:00', date_sent='2023-08-30', ...)
        primary_key = create_primary_key(mms)
        print(primary_key)  # Output: '2023083014300020230830'

    Note:
        The primary key is created by combining the message's date, time, and date_sent attributes as a string.
    """
    primary_key = f"{mms.strdate}{mms.strtime}{mms.date_sent}"
    return primary_key

def check_value_existence(table_name, column_name, value):
    """
    Checks the existence of a value in a specific column of a database table.

    Args:
        table_name (str): The name of the database table to search.
        column_name (str): The name of the column to check for the value.
        value: The value to search for in the specified column.

    Returns:
        bool: True if the value exists in the column, False otherwise.

    Example:
        # Check if an email address exists in the 'ContactEmails' table.
        email = 'example@email.com'
        exists = check_value_existence(table_name='ContactEmails', column_name='email', value=email)
        if exists:
            print(f"{email} exists in the 'ContactEmails' table.")
        else:
            print(f"{email} does not exist in the 'ContactEmails' table.")

    Note:
        This function connects to a SQLite database specified by the global 'DB_NAME' variable.
        It performs a SELECT query on the specified table and column to check for the existence of the given value.
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

def add_address(str_address):
    """
    Adds a new address (phone number) to the 'ContactPhoneNumbers' table if it doesn't already exist.

    Args:
        str_address (str): The address (phone number) to add.

    Returns:
        int: The primary key (phone_id) of the inserted or existing address if successful, or None if there was an error.

    Example:
        # Add a new phone number to the 'ContactPhoneNumbers' table.
        phone_number = '+1234567890'
        phone_id = add_address(phone_number)
        if phone_id is not None:
            print(f"Added phone number '{phone_number}' with phone_id={phone_id}.")
        else:
            print("Failed to add the phone number.")

    Note:
        This function connects to a SQLite database specified by the global 'DB_NAME' variable.
        It checks if the address (phone number) already exists in the 'ContactPhoneNumbers' table and adds it if not.
    """
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
        #print(f"Inserted in ContactPhoneNumbers: phone_id={new_row[0]}, contact_id={new_row[1]}, phone={new_row[2]}")
    else:
        #print(f"{str_address} already exist in table ContactPhoneNumbers with PK:{phone_id}.")
        pass
    return phone_id



def mtm_mms_id_phone_id(mms_id, phone_ids):
    """
    Creates many-to-many (MTM) relationships between an MMS message and phone numbers in the 'Mms_ContactPhoneNumber' table.

    Args:
        mms_id (int): The primary key (message_id) of the MMS message.
        phone_ids (list): A list of primary keys (phone_ids) of phone numbers to associate with the MMS message.

    Example:
        # Create MTM relationships between an MMS message and phone numbers.
        mms_message_id = 123  # Replace with the actual MMS message ID.
        phone_number_ids = [1, 2, 3]  # Replace with the actual phone number IDs.
        mtm_mms_id_phone_id(mms_message_id, phone_number_ids)

    Note:
        This function connects to a SQLite database specified by the global 'DB_NAME' variable.
        It associates the given MMS message ID with the specified phone numbers in the 'Mms_ContactPhoneNumber' table.
        If a relationship already exists, it won't create a duplicate.
    """
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
    """
    Adds an MMS part to the 'MmsPart' table in the database.

    Args:
        part (MmsPart): An MmsPart object representing the MMS part to be added.

    Returns:
        int: The primary key (part_id) of the newly added MMS part.

    Example:
        # Create an MmsPart object (replace with actual data).
        mms_part = MmsPart(seq=1, ct="text/plain", name="part1.txt", chset="UTF-8", cd=None, fn=None, cid="content-id-1",
                           cl=None, ctt_s="7bit", ctt_t=None, text="This is the text content of the part.")

        # Add the MMS part to the database.
        part_id = add_part(mms_part)

    Note:
        This function connects to a SQLite database specified by the global 'DB_NAME' variable.
        It inserts the MMS part data into the 'MmsPart' table and returns the primary key (part_id) of the new part.
    """
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
    """
    Establishes a many-to-many relationship between an MMS message and a part by inserting a record
    into the 'Mms_MmsPart' table.

    Args:
        mms_id (str): The primary key (mms_id) of the MMS message.
        part_id (int): The ID of the part to associate with the MMS message.

    Example:
        # Establish a many-to-many relationship between MMS message '12345678901234'
        # and part '5678'.
        mtm_mms_id_part_id('12345678901234', 5678)
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""INSERT INTO Mms_MmsPart (mms_id, part_id) VALUES (?, ?)"""
    cursor.execute(query, (mms_id, part_id))
    connection.commit()
    connection.close()

def add_mmsaddr(addr):
    """
    Adds an MMS address (recipient or sender) to the 'MmsAddr' table in the database.

    Args:
        addr (MmsAddress): An MmsAddress object representing the MMS address.

    Returns:
        int: The ID of the newly inserted MMS address in the database.

    Example:
        # Create an MmsAddress object
        address = MmsAddress("example@example.com", "TO", "UTF-8")
        # Add the MMS address to the database and retrieve its ID
        addr_id = add_mmsaddr(address)
    """
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
    """
    Creates a many-to-many relationship between an MMS message and an MMS address in the database.

    This function inserts a record into the 'Mms_MmsAddr' table, linking an MMS message (identified by its 'mms_id')
    with an MMS address (identified by its 'addr_id').

    Args:
        mms_id (str): The unique identifier of the MMS message.
        addr_id (int): The ID of the MMS address to associate with the MMS message.

    Returns:
        None

    Example:
        # Assuming you have 'mms_id' and 'addr_id' values
        mms_id = "202308301200001"
        addr_id = 1
        # Create a many-to-many relationship between the MMS message and the MMS address
        mtm_mms_id_addr_id(mms_id, addr_id)
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    query = f"""INSERT INTO Mms_MmsAddr (mms_id, addr_id) VALUES (?, ?)"""
    cursor.execute(query, (mms_id, addr_id))
    connection.commit()
    connection.close()


def add_mmses(mms_list):
    """
    Adds a list of MMS messages to the database.

    Args:
        mms_list (list): A list of MMS objects to be added to the database.

    Example:
        # Create a list of MMS objects (replace with actual data).
        mms_objects = [mms1, mms2, mms3]

        # Add the MMS messages to the database.
        add_mmses(mms_objects)

    Note:
        This function connects to a SQLite database specified by the global 'DB_NAME' variable.
        It inserts MMS message data into the 'Mms' table and related data into other tables.
        If a message with the same primary key (mms_id) already exists, it is not added again.
    """
    for mms in mms_list:
        primary_key = create_primary_key(mms=mms)

        # Liste pour stocker les ID des numéros de téléphone liés à ce SMS
        phone_ids = []
        for address in mms.recipient_list:
        #for address in mms.address:
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

            cursor.execute(query, (primary_key, mms.type_msg_box, str(mms.date), str(mms.time), mms.contact_name, mms.rr, mms.sub, mms.ct_t, mms.read_status, mms.seen,
                                   mms.msg_box, mms.sub_cs, mms.resp_st, mms.retr_st, mms.d_tm, mms.text_only, mms.exp, mms.locked, mms.m_id, mms.st,
                                   mms.retr_txt_cs, mms.retr_txt,
                                   mms.creator, mms.date_sent, mms.read, mms.m_size, mms.rpt_a, mms.ct_cls, mms.pri, mms.sub_id, mms.tr_id, mms.resp_txt, mms.ct_l,
                                   mms.m_cls, mms.d_rpt,
                                   mms.v, mms.id, mms.m_type, mms.readable_date))
            connection.commit()

            for part in mms.parts:
                part_id = add_part(part=part)
                # Creation of the link between tables
                mtm_mms_id_part_id(mms_id=primary_key, part_id=part_id)
            for addr in mms.addrs:
                addr_id = add_mmsaddr(addr=addr)
                # Creation of the link between tables
                mtm_mms_id_addr_id(mms_id=primary_key, addr_id=addr_id)

        connection.close()



