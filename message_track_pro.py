import os
import sms_mms_from_xml
import sqlite3
import db_insertion_eml
import db_insertion_mms
import db_insertion_sms
from models import Email
import db_insertion_update
import db_viewer as db_v
import db_insertion_messenger
import mbox_extractor
import write_messages
import messenger_from_html
import time
from dotenv import load_dotenv

# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
EML_FILE_DIRECTORY = os.getenv("EML_FILE_DIRECTORY")
XML_FILE_DIRECTORY = os.getenv("XML_FILE_DIRECTORY")
XML_FILENAME = os.getenv("XML_FILENAME")
DB_TABLES = os.getenv("DB_TABLES")
DB_NAME = os.getenv("DB_NAME")
TIMEZONE = os.getenv("TIMEZONE")
YOURPHONENUMBER = os.getenv("YOURPHONENUMBER")
MBOX_FILEPATH = os.getenv("MBOX_FILEPATH")
MBOX_OUTPUT_DIRECTORY = os.getenv("MBOX_OUTPUT_DIRECTORY")
CSV_CONTACTS = os.getenv("CSV_CONTACTS")
CSV_TAGS = os.getenv("CSV_TAGS")
TITLE = os.getenv("TITLE")
MESSENGER_DIRECTORY = os.getenv("MESSENGER_DIRECTORY")


def create_database(DB_NAME, DB_TABLES):
    """
    Creates a new SQLite database and initializes it with tables from the specified SQL file.

    Args:
        db_name (str): The name of the SQLite database to create.
        db_tables (str): The path to the SQL file containing the table creation queries.
    """
    #try:
    # Lecture de la requête de création de table à partir du fichier .sql
    with open(DB_TABLES, 'r') as sql_file:
        create_table_query = sql_file.read()

    # Connexion à la base de données (crée un fichier database.db s'il n'existe pas)
    conn = sqlite3.connect(DB_NAME)

    # Exécution de la requête de création de table
    cursor = conn.cursor()
    cursor.executescript(create_table_query)

    # Validation des modifications et fermeture de la connexion
    conn.commit()
    conn.close()
    #except Exception as e:
    #    print(f"\033[93mErreur lors de la création de la base de données : {e} \033[0m")


def rename_file(directory, filename):
    try:
        if not directory.endswith("/"):
            directory = directory + '/'
        filepath_origin = directory + filename
        if not os.path.exists(filepath_origin):
            print(f"\033[93mErreur, le répertoire {directory} ne contient pas de fichier {filename}\033[0m")
            return None

        with open(filepath_origin, "r", encoding="utf-8") as eml_file:
            eml_content = eml_file.read()
        email = Email.Email(filepath_origin)
        try:
            date = email.strdate()
            time = email.strtime()
        except:
            print(
                f"\033[93mErreur lors de la récupération de la date et l'heure, le fichier {filepath_origin} ne sera pas renommé.\033[0m")
            return filepath_origin

        if date and time:
            i = 0
            while True:
                filename_expected = f"""{date}_{time}.eml""" if i == 0 else f"""{date}_{time}_{i}.eml"""
                filepath_expected = directory + filename_expected
                if not os.path.exists(filepath_expected):
                    break
                else:
                    # Lire le contenu du fichier existant
                    with open(filepath_expected, "r", encoding="utf-8") as existing_file:
                        existing_content = existing_file.read()
                        # Comparer le contenu des fichiers
                    if existing_content != eml_content:
                        print(f"Le fichier {filename_expected} existe déjà avec un contenu différent de {filename}")
                        i += 1
                    else:
                        # sinon on peut écraser et renommer...
                        # print("Ecrasement du fichier d'origine par sa nouvelle copie au contenu identique")
                        break

            # Renommer le fichier
            os.rename(filepath_origin, filepath_expected)
            # print(f"Le fichier {filename} a été renommé en {filename_expected}")
            return filepath_expected
        else:
            print(
                f"\033[93mErreur le champ date et/ou heure est vide, le fichier {filepath_origin} ne sera pas renommé.\033[0m")
            return filepath_origin


    except Exception as e:
        print(
            f"\033[93mUne erreur s'est produite lors du renommage du fichier {filename} du dossier {directory}: {e} \033[0m")
        return None


def list_files_in_directory(directory_path):
    try:
        # Utilise os.listdir() pour obtenir la liste des fichiers et dossiers dans le répertoire
        files = os.listdir(directory_path)

        # Filtre les éléments qui sont des fichiers (pas des dossiers)
        files = [file for file in files if os.path.isfile(os.path.join(directory_path, file))]

        return files
    except Exception as e:
        return f"\033[93mUne erreur s'est produite : {e} \033[0m"


if __name__ == "__main__":
    start_time = time.time()
    # Creation de la DB si inexistante
    create_database(DB_NAME=DB_NAME, DB_TABLES=DB_TABLES)

    efe = 0
    if efe:
        print(
            f"\033[32m#------------------------------------ EMAILS FROM EML------------------------------------#\033[0m")
        # Liste les fichiers *.eml
        eml_list = list_files_in_directory(directory_path=EML_FILE_DIRECTORY)
        for file in eml_list:
            file_path = EML_FILE_DIRECTORY + '/' + file
            if os.path.getsize(file_path) > 0:
                filepath = rename_file(directory=EML_FILE_DIRECTORY, filename=file)
                if filepath:
                    email_obj = Email.Email(filepath)
                    db_insertion_eml.add_email(email_obj=email_obj)

    efm = 0
    if efm:
        print(
            f"\033[32m#------------------------------------ EMAILS FROM MBOX------------------------------------#\033[0m")
        mbox_extractor.generate_eml_from_mbox(mbox_filepath=MBOX_FILEPATH, mbox_output_directory=MBOX_OUTPUT_DIRECTORY)
        eml_list2 = list_files_in_directory(directory_path=MBOX_OUTPUT_DIRECTORY)
        for file in eml_list2:
            file_path = MBOX_OUTPUT_DIRECTORY + '/' + file
            if os.path.getsize(file_path) > 0:
                filepath = rename_file(directory=MBOX_OUTPUT_DIRECTORY, filename=file)
                if filepath:
                    email_obj = Email.Email(filepath)
                    db_insertion_eml.add_email(email_obj=email_obj)

    sms_mms = 0
    if sms_mms:
        print(
            f"\033[32m# -------------------------------------- SMS / MMS --------------------------------------#\033[0m")
        xml_file_path = f"{XML_FILE_DIRECTORY}/{XML_FILENAME}"
        sms_list, mms_list = sms_mms_from_xml.read_sms_mms_from_xml(xml_file_path=xml_file_path)
        db_insertion_sms.add_smses(sms_list=sms_list)
        db_insertion_mms.add_mmses(mms_list=mms_list)

    messenger = 0
    if messenger:
        print(
            f"\033[32m# -------------------------------------- Messenger --------------------------------------#\033[0m")
        messages = messenger_from_html.create_list_messenger_objects(messenger_directory=MESSENGER_DIRECTORY)
        db_insertion_messenger.add_messages(list_message_obj=messages, allow_duplicates=True)

    contacts = 0
    if contacts:
        print(
            f"\033[32m# --------------------------------------- Contacts ---------------------------------------#\033[0m")
        db_insertion_update.insert_contacts_from_csv(csv_filename=CSV_CONTACTS)

    tags = 0
    if tags:
        print(
            f"\033[32m# ----------------------------------------- Tags -----------------------------------------#\033[0m")
        db_insertion_update.insert_tags_from_csv(csv_tags=CSV_TAGS)

    generator = 1
    if generator:
        print(
            f"\033[32m# ---------------------------------- PDF/HTML Generator ----------------------------------#\033[0m")
        headers, list_of_messages_obj = db_v.get_messages(contact_id=3, word="école")
        write_messages.write_messages(title=TITLE, list_of_messages_obj=list_of_messages_obj)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Le programme a pris {elapsed_time} secondes pour s'exécuter.")
