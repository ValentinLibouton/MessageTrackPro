import os
import sms_mms_from_xml
import sqlite3
import db_insertion_eml
import db_insertion_mms
import db_insertion_sms
import Email
import db_insertion_update
import db_viewer as db_v
import write_messages
import filecmp
import mbox_extractor
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

def create_database(DB_NAME, DB_TABLES):
    """
    Creates a new SQLite database and initializes it with tables from the specified SQL file.

    Args:
        db_name (str): The name of the SQLite database to create.
        db_tables (str): The path to the SQL file containing the table creation queries.
    """
    try:
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
    except Exception as e:
        print(f"\033[93mErreur lors de la création de la base de données : {e} \033[0m")


def rename_file(directory, filename):
    try:
        date = None
        time = None
        filepath = f"{directory}/{filename}"
        print(f"try rename file: {filepath}")
        with open(filepath, "r", encoding="utf-8") as eml_file:
            eml_content = eml_file.read()
        email = Email.Email(filepath)
        try:
            date = email.strdate()
            time = email.strtime()
        except:
            print("Erreur lors de la récupération de la date et l'heure, le fichier ne sera pas renommé")
            return None
        if time and date:
            filename = os.path.basename(filepath)
            newfilename = f"{date}_{time}.eml"
            if filename != newfilename:
                check_name = True
                i = 0
                while check_name:
                    i+=1
                    # Chemin complet pour le nouveau nom de fichier
                    new_eml_file_path = os.path.join(directory, newfilename)
                    # Vérifier si le nouveau nom de fichier existe déjà
                    if os.path.exists(new_eml_file_path):
                        # Lire le contenu du fichier existant
                        with open(new_eml_file_path, "r", encoding="utf-8") as existing_file:
                            existing_content = existing_file.read()

                        # Comparer le contenu des fichiers
                        if existing_content != eml_content:
                            print(f"Le fichier {newfilename} existe déjà avec un contenu différent de {filename}")
                            newfilename = f"""{date}_{time}.{str(i)}.eml"""

                        else:
                            check_name = False
                    else:
                        check_name = False

                # Renommer le fichier
                os.rename(filepath, new_eml_file_path)
                print(f"Le fichier {filename} a été renommé en {newfilename}")
                return new_eml_file_path
            return filepath
    except Exception as e:
        print(f"\033[93mUne erreur s'est produite lors du renommage du fichier : {e} \033[0m")
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
    # Creation de la DB si inexistante
    create_database(DB_NAME=DB_NAME, DB_TABLES=DB_TABLES)


    efe = 0
    if efe:
        print(f"\033[32m#------------------------------------ EMAILS FROM EML------------------------------------#\033[0m")
        # Liste les fichiers *.eml
        eml_list = list_files_in_directory(directory_path=EML_FILE_DIRECTORY)
        for file in eml_list:
            filepath = rename_file(directory=EML_FILE_DIRECTORY, filename=file)
            if filepath:
                email_obj = Email.Email(filepath)
                db_insertion_eml.add_email(email_obj=email_obj)

    efm = 1
    if efm:
        print(f"\033[32m#------------------------------------ EMAILS FROM MBOX------------------------------------#\033[0m")
        #mbox_extractor.generate_eml_from_mbox(mbox_filepath=MBOX_FILEPATH, mbox_output_directory=MBOX_OUTPUT_DIRECTORY)
        eml_list2 = list_files_in_directory(directory_path=MBOX_OUTPUT_DIRECTORY)
        for file in eml_list2:
            filepath = rename_file(directory=MBOX_OUTPUT_DIRECTORY, filename=file)
            if filepath:
                email_obj = Email.Email(filepath)
                db_insertion_eml.add_email(email_obj=email_obj)


    sms_mms = 1
    if sms_mms:
        print(f"\033[32m# -------------------------------------- SMS / MMS --------------------------------------#\033[0m")
        xml_file_path = f"{XML_FILE_DIRECTORY}/{XML_FILENAME}"
        sms_list, mms_list = sms_mms_from_xml.read_sms_mms_from_xml(xml_file_path=xml_file_path)
        db_insertion_sms.add_smses(sms_list=sms_list)
        db_insertion_mms.add_mmses(mms_list=mms_list)

    contacts = 1
    if contacts:
        print(f"\033[32m# --------------------------------------- Contacts ---------------------------------------#\033[0m")
        db_insertion_update.insert_contacts_from_csv(csv_filename=CSV_CONTACTS)

    tags = 1
    if tags:
        print(f"\033[32m# ----------------------------------------- Tags -----------------------------------------#\033[0m")
        db_insertion_update.insert_tags_from_csv(csv_tags=CSV_TAGS)

    generator = 1
    if generator:
        print(f"\033[32m# ---------------------------------- PDF/HTML Generator ----------------------------------#\033[0m")
        headers, list_of_messages_obj = db_v.get_messages(contact_id=3)
        write_messages.write_messages(title=TITLE, list_of_messages_obj=list_of_messages_obj)


