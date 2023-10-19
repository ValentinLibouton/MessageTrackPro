import os
from bs4 import BeautifulSoup
from models import Messenger
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)
MESSENGER_DIRECTORY = os.getenv("MESSENGER_DIRECTORY")
def list_files(directory, target_filename='message_1.html'):
    file_tuples = []

    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename == target_filename:
                file_path = os.path.join(foldername, filename)
                parent_folder = os.path.basename(foldername)
                conversation_name = extract_conversation_name(parent_folder)
                file_tuples.append((conversation_name, file_path))


    return file_tuples


def extract_conversation_name(string):
    return string.split('_')[0]


def extract_and_create_messengers(conversation_name, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Recherche des balises div avec une classe spécifique
    dates = soup.find_all('div', class_='_3-94 _2lem')
    names = soup.find_all('div', class_='_3-96 _2pio _2lek _2lel')
    msgs = soup.find_all('div', class_='_3-96 _2let')

    datas_messages = zip(dates, names, msgs)

    return datas_messages

def create_list_messenger_objects(messenger_directory):
    i=0
    messenger_list = []
    for message in list_files(messenger_directory):
        conversation_name, file_path = message
        for date, name, msg in extract_and_create_messengers(conversation_name=conversation_name, file_path=file_path):
            if conversation_name and date.text and name.text and msg.text:
                i+=1
                print(f"Creation objet Message N°{i}")
                message = Messenger.Messenger(conversation_name=conversation_name, fullname=name.text, date=date.text,
                                              message=msg.text)
                messenger_list.append(message)
    return messenger_list


