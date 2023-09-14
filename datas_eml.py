import email
from email.header import decode_header
import chardet
from bs4 import BeautifulSoup
import os
import pytz
from datetime import datetime
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
TIMEZONE = os.getenv("TIMEZONE")

def extract_mail_subject(msg):
    special_encodings = ['ISO-8859-1', 'MacRoman']
    # Obtenir le sujet du message (avec décodage)
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        # Détecter l'encodage approprié du sujet
        if encoding:
            try:
                subject = subject.decode(encoding)
            except UnicodeDecodeError:
                subject = subject.decode('utf-8', errors='replace')
        else:
            detected_encoding = chardet.detect(subject)['encoding']
            if detected_encoding and detected_encoding in special_encodings:
                subject = subject.decode(detected_encoding)
            else:
                subject = subject.decode('utf-8', errors='replace')
    return subject


def extract_email_sender(msg):
    sender, _ = decode_header(msg["From"])[0]
    if isinstance(sender, bytes):
        sender = sender.decode('utf-8')
    fullname_sender, email_sender = email.utils.parseaddr(sender)
    return email_sender


def extract_emails_recipients(recipients_string):
    emails = []
    if recipients_string:
        for recipient in recipients_string.split(','):
            fullname_recipient, email_recipient = email.utils.parseaddr(recipient)
            emails.append(email_recipient)
    return emails


def extract_date_time(eml_date):
    # Convertir la date du format EML en objet datetime
    date_obj = datetime.strptime(eml_date, "%a, %d %b %Y %H:%M:%S %z")
    timezone = pytz.timezone(TIMEZONE)
    date_obj = date_obj.astimezone(timezone)

    date = date_obj.strftime("%Y%m%d")
    time = date_obj.strftime("%H%M%S")
    return date, time


def extract_html_text(msg):
    html_text = ""
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html_text = part.get_payload(decode=True).decode("utf-8")
            break  # Sortir de la boucle après avoir trouvé la première partie HTML
    return html_text


def extract_readable_text(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()


def extract_attachment_names(msg):
    attachment_names = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename, encoding = decode_header(part.get_filename())[0]
            if isinstance(filename, bytes):
                filename = filename.decode(encoding if encoding else "utf-8", errors="replace")
            attachment_names.append(filename)
    return attachment_names


def eml_to_dict(eml_file_path):
    try:
        # Ouvrir le fichier .eml et le lire
        with open(eml_file_path, "r", encoding="utf-8") as eml_file:
            eml_content = eml_file.read()
        filename = os.path.basename(eml_file_path)
        # Parser le contenu EML
        msg = email.message_from_string(eml_content)

        # Extraire l'email de l'expéditeur
        email_sender = extract_email_sender(msg)

        # Extraire les emails des destinataires
        emails_to = extract_emails_recipients(msg["To"])
        emails_cc = extract_emails_recipients(msg["Cc"])
        emails_bcc = extract_emails_recipients(msg["Bcc"])

        # Extraire le sujet du mail
        subject = extract_mail_subject(msg=msg)

        # Extraire date et heure
        date, time = extract_date_time(msg["Date"])
        # Traitement du corps de texte
        html_text = extract_html_text(msg)
        readable_text = extract_readable_text(html_text)

        # Extraire la liste des noms de pièces jointes
        attachments_list = extract_attachment_names(msg)

        email_dict = {

            'email_sender': email_sender,
            'recipient_to': emails_to,  # list
            'recipient_cc': emails_cc,  # list
            'recipient_bcc': emails_bcc,  # list
            'subject': subject,
            'date': date,
            'time': time,
            'content': readable_text,
            'original_filename': filename,
            'attachments_names': attachments_list  # list
        }
        return email_dict
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier EML : {e}")
        return None


if __name__ == "__main__":
    pass
