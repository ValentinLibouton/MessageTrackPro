import os
import datas_eml
import datas_sms_mms
import sqlite3
import eml_to_db
import mms_to_db
import sms_to_db
import email
import data_insertion
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
        print(f"Erreur lors de la création de la base de données : {e}")

def rename_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as eml_file:
            eml_content = eml_file.read()

        # Parser le contenu EML
        msg = email.message_from_string(eml_content)
        # Extraire date et heure
        date, time = datas_eml.extract_date_time(msg["Date"])

        filename = os.path.basename(filepath)
        newfilename = f"{date}_{time}.eml"
        if filename != newfilename:
            # Chemin complet pour le nouveau nom de fichier
            new_eml_file_path = os.path.join(EML_FILE_DIRECTORY, newfilename)

            # Renommer le fichier
            os.rename(filepath, new_eml_file_path)
            print(f"Le fichier {filename} a été renommé en {newfilename}")
            return new_eml_file_path
        return filepath
    except Exception as e:
        print(f"Une erreur s'est produite lors du renommage du fichier : {e}")
        return None
def list_files_in_directory(directory_path):
    try:
        # Utilise os.listdir() pour obtenir la liste des fichiers et dossiers dans le répertoire
        files = os.listdir(directory_path)

        # Filtre les éléments qui sont des fichiers (pas des dossiers)
        files = [file for file in files if os.path.isfile(os.path.join(directory_path, file))]

        return files
    except Exception as e:
        return f"Une erreur s'est produite : {e}"

if __name__ == "__main__":
    # Creation de la DB si inexistante
    create_database(DB_NAME=DB_NAME, DB_TABLES=DB_TABLES)

    # -------------------------------------- Contacts --------------------------------------#
    #data_insertion.insert_contacts_from_csv()

    #-------------------------------------- EMAILS --------------------------------------#

    # Liste les fichiers *.eml
    eml_list = list_files_in_directory(EML_FILE_DIRECTORY)
    for file in eml_list:
        filepath = f"{EML_FILE_DIRECTORY}/{file}"
        filepath = rename_file(filepath=filepath)
        # Pour chaque mail il crée un dictionnaire
        eml_dict = datas_eml.eml_to_dict(eml_file_path=filepath)
        eml_to_db.add_email(eml_dict=eml_dict)

    # -------------------------------------- SMS / MMS --------------------------------------#
    xml_file_path = f"{XML_FILE_DIRECTORY}/{XML_FILENAME}"
    sms_list, mms_list = datas_sms_mms.read_sms_mms_from_xml(xml_file_path=xml_file_path)
    sms_to_db.add_smses(sms_list=sms_list)
    mms_to_db.add_mmses(mms_list=mms_list)

    data_insertion.insert_contacts_from_csv()
