import os
import mailbox
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

MBOX_FILEPATH = os.getenv("MBOX_FILEPATH")
MBOX_OUTPUT_DIRECTORY = os.getenv("MBOX_DIRECTORY")


def generate_eml_from_mbox(mbox_filepath=MBOX_FILEPATH, mbox_output_directory=MBOX_OUTPUT_DIRECTORY):
    """
    Converts emails from an MBOX file to individual EML files.

    Args:
        mbox_filepath (str): The path to the MBOX file to be processed.
        mbox_output_directory (str): The directory where the generated EML files will be saved.

    Returns:
        None

    This function reads emails from the specified MBOX file and converts each email into a separate EML file.
    The EML files are saved in the provided output directory with filenames like 'email_1.eml', 'email_2.eml', etc.

    Example:
        generate_eml_from_mbox('inbox.mbox', 'eml_output_directory')

    Note:
        - Make sure to have the 'mailbox' module installed.
        - Existing EML files in the output directory may be overwritten.
    """
    try:
        # Charger le fichier mbox
        mbox = mailbox.mbox(mbox_filepath)

        # Parcourir tous les e-mails dans la boîte aux lettres mbox
        for i, msg in enumerate(mbox):
            filename = f"email_{i+1}.eml"
            filepath = f"{mbox_output_directory}/{filename}"
            with open(filepath, 'w', errors='ignore') as eml_file:
                eml_file.write(msg.as_string())

        print("All emails have been converted to EML files.")
    except Exception as e:
        print(f"\033[93mUne erreur s'est produite lors de la génération des eml issu de mbox : {e} \033[0m")

