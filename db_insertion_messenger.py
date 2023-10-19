import sqlite3
import os
from models import Messenger
from dotenv import load_dotenv

# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
DB_NAME = os.getenv("DB_NAME")


def check_value_existence(table_name, conditions_list):
    row = None
    params = []
    query = f"""SELECT * FROM {table_name} WHERE """
    for condition in conditions_list:
        column, value = condition
        query += f"""{column} = ? and """
        params.append(value)
    query = query[:-5]
    params = tuple(params)
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    connection.close()
    if row:
        return row[0]
    return False

def add_surname(msg):
    surname_id = check_value_existence(table_name='ContactMessenger', conditions_list=[('surname', msg.fullname)])
    if not surname_id:
        fullname = None
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ContactMessenger (surname) VALUES (?)", (msg.fullname,))
        # Récupérer l'ID généré automatiquement
        surname_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return surname_id

def add_group(msg):
    group_id = check_value_existence(table_name='GroupMessenger',
                                     conditions_list=[('group_name', msg.conversation_name)])
    if not group_id:
        group_name = None
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO GroupMessenger (group_name) VALUES (?)", (msg.conversation_name,))
        # Récupérer l'ID généré automatiquement
        group_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return group_id

def mtm_Group_Surname(group_id, surname_id):
    result = None
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    result = check_value_existence(table_name='MTM_GroupMessenger_ContactMessenger', conditions_list=[('group_id', group_id), ('surname_id',surname_id)])
    if not result:

        cursor.execute("INSERT INTO MTM_GroupMessenger_ContactMessenger (group_id, surname_id) VALUES (?,?)",
                       (group_id, surname_id))
        connection.commit()
    connection.close()


def add_message(msg, allow_duplicates):
    surname_id = add_surname(msg)
    group_id = add_group(msg)
    # Create Many To Many Link between "GroupMessenger" and "ContactMessenger"
    mtm_Group_Surname(group_id=group_id, surname_id=surname_id)
    #message_id = check_value_existence(table_name='Messenger', conditions_list=[('message', msg.message),
    #                                                                            ('date', str(msg.date)),
    #                                                                            ('time', str(msg.time)),
    #                                                                            ('group_id', group_id),
    #                                                                            ('surname_id', surname_id)])
    #if not message_id or allow_duplicates:
    # ToDo: Ajouter le nouveau message à la base de données
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Messenger (message, date, time, group_id, surname_id) VALUES (?, ?, ?, ?, ?)",
                   (msg.message, str(msg.date), str(msg.time), group_id, surname_id))
    connection.commit()
    connection.close()

def add_surnames(list_message_obj):
    print("Add surnames ...")
    # Création de la liste de tuples pour executemany sans doublons
    values = list({(message.fullname,) for message in list_message_obj})

    # Connexion à la base de données
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Requête pour vérifier si chaque élément de values existe déjà
    existing_values = [value[0] for value in values if not
                       check_value_existence('ContactMessenger', [('surname', value[0])])]

    # Requête d'insertion
    insert_query = "INSERT INTO ContactMessenger (surname) VALUES (?)"

    # Insérer chaque enregistrement s'il n'existe pas déjà
    cursor.executemany(insert_query, [(value,) for value in existing_values])

    # Validation des modifications et fermeture de la connexion
    connection.commit()
    connection.close()

def add_groups(list_message_obj):
    print("Add groups ...")
    # Création de la liste de tuples pour executemany sans doublons
    values = list({(message.conversation_name,) for message in list_message_obj})

    # Connexion à la base de données
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Requête pour vérifier si chaque élément de values existe déjà
    existing_values = [value[0] for value in values if not check_value_existence('GroupMessenger', [('group_name', value[0])])]

    # Requête d'insertion
    insert_query = "INSERT INTO GroupMessenger (group_name) VALUES (?)"

    # Insérer chaque enregistrement s'il n'existe pas déjà
    cursor.executemany(insert_query, [(value,) for value in existing_values])

    # Validation des modifications et fermeture de la connexion
    connection.commit()
    connection.close()

def mtm_group_surname(list_message_obj):
    print("Link surnames with groups ...")
    # Connexion à la base de données
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Récupérer les IDs des surnames et des groupes
    surname_ids = [check_value_existence('ContactMessenger', [('surname', message.fullname)]) for message in
                   list_message_obj]
    group_ids = [check_value_existence('GroupMessenger', [('group_name', message.conversation_name)]) for message in
                 list_message_obj]

    # Requête pour vérifier si chaque paire (group_id, surname_id) existe déjà
    existing_pairs = list({(group_id, surname_id) for group_id, surname_id in zip(group_ids, surname_ids) if not
    check_value_existence('MTM_GroupMessenger_ContactMessenger',
                          [('group_id', group_id), ('surname_id', surname_id)])})

    # Requête d'insertion
    insert_query = "INSERT INTO MTM_GroupMessenger_ContactMessenger (group_id, surname_id) VALUES (?, ?)"

    # Insérer chaque paire (group_id, surname_id) s'il n'existe pas déjà
    cursor.executemany(insert_query, existing_pairs)

    # Validation des modifications et fermeture de la connexion
    connection.commit()
    connection.close()


def add_messages(list_message_obj, allow_duplicates):
    add_surnames(list_message_obj=list_message_obj)
    add_groups(list_message_obj=list_message_obj)
    mtm_group_surname(list_message_obj=list_message_obj)

    # Connexion à la base de données
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Récupérer les IDs des surnames et des groupes
    surname_ids = [check_value_existence('ContactMessenger', [('surname', message.fullname)]) for message in
                   list_message_obj]
    group_ids = [check_value_existence('GroupMessenger', [('group_name', message.conversation_name)]) for message in
                 list_message_obj]
    if allow_duplicates:
        # Création d'une liste de tuples pour les données de Messenger
        messenger_data = [(message.message, str(message.date), str(message.time), group_id, surname_id) for
                          message, group_id, surname_id in zip(list_message_obj, group_ids, surname_ids)]
    else:
        # Création d'une liste de tuples pour les données de Messenger
        messenger_data = list({(message.message, str(message.date), str(message.time), group_id, surname_id) for
                          message, group_id, surname_id in zip(list_message_obj, group_ids, surname_ids) if not
                          check_value_existence('Messenger', [('message', message.message), ('date', str(message.date)),
                                                              ('time', str(message.time)), ('group_id', group_id),
                                                               ('surname_id', surname_id)])})
    print(f"""{len(messenger_data)} messages vont être insérés en DB""")

    # Requête d'insertion
    insert_query = "INSERT INTO Messenger (message, date, time, group_id, surname_id) VALUES (?, ?, ?, ?, ?)"

    # Insérer chaque enregistrement
    cursor.executemany(insert_query, messenger_data)

    # Validation des modifications et fermeture de la connexion
    connection.commit()
    connection.close()


if __name__ == '__main__':
    pass
