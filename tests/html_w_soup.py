from bs4 import BeautifulSoup

# Votre code pour lire le fichier HTML
with open('message_1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Analyse du HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Recherche des balises div avec une classe spécifique
dates = soup.find_all('div', class_='_3-94 _2lem')
names = soup.find_all('div', class_='_3-96 _2pio _2lek _2lel')
msgs = soup.find_all('div', class_='_3-96 _2let')

# Utilisation de zip pour combiner les listes
for date, name, msg in zip(dates, names, msgs):
    # Votre logique pour extraire des données spécifiques
    date_data = date.text
    name_data = name.text
    msg_data = msg.text

    # Imprimez ou traitez les données comme nécessaire
    print(f"Date: {date_data}, Name: {name_data}, Message: {msg_data}")