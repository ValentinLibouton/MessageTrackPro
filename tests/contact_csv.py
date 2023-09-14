import csv

# Fonction pour convertir une liste en chaîne de caractères
def list_to_string(lst):
    return ', '.join(lst)

# Données à écrire dans le fichier CSV
data = [
    {'first_name': 'John', 'last_name': 'Doe', 'phone_numbers': ["0488000000", "+32488000000"], 'email_addresses': ["abc@def.com"]},
    {'first_name': 'Jane', 'last_name': 'Dong', 'phone_numbers': ["0488880000", "+32488880000"], 'email_addresses': ["abcd@defg.com"]}
]

# Écrire les données dans le fichier CSV
with open('../contacts.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name', 'phone_numbers', 'email_addresses']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for contact in data:
        contact['phone_numbers'] = list_to_string(contact['phone_numbers'])
        contact['email_addresses'] = list_to_string(contact['email_addresses'])
        writer.writerow(contact)

# Lire et afficher les données du fichier CSV
with open('../contacts.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['phone_numbers'])
        phones_str = row['phone_numbers'].replace(' ','')
        phones_lst = list(phones_str.split(','))
        print(phones_lst)
        print(type(phones_lst))
