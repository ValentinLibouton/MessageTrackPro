import json, re, pytz, os
from dateutil import parser
from mailparser import parse_from_file
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "../variables.env"
load_dotenv(dotenv_path)
TIMEZONE = os.getenv("TIMEZONE")


class Email:
    """
        Represents an email message parsed from a file.

        Args:
            filepath (str): The path to the email file to be parsed.

        Attributes:
            sender_name (str): The name of the email sender.
            sender_email (str): The email address of the email sender.
            subject (str): The subject of the email.
            recipients_to (list): The list of primary recipients' email addresses.
            recipients_cc (list): The list of CC (Carbon Copy) recipients' email addresses.
            recipients_bcc (list): The list of BCC (Blind Carbon Copy) recipients' email addresses.
            date (datetime.date): The date when the email was sent.
            strdate (str): The date as a string without hyphens.
            time (datetime.time): The time when the email was sent.
            strtime (str): The time as a string without colons.
            body (str): The content of the email body.
            filename (str): The filename of the email file.
            attachments_names (list): The filenames of attachments in the email.
            attachments (list): The list of attachments as dictionaries.

        Methods:
            __str__(): Returns a formatted string representation of the Email object.

        Note:
            This class is designed to parse and represent email messages from files. It provides various properties
            to access different parts of the email message, including sender information, recipients, date, time, body,
            and attachments.

        """
    def __init__(self, filepath):
        self.__parsed_email = parse_from_file(filepath)
        self.__filename = os.path.basename(filepath)
        self.__attachments = self.__parsed_email.attachments

    @property
    def sender_name(self):
        return self.__parsed_email.from_[0][0]

    def sender_email_old(self):
        return self.__parsed_email.from_[0][1]
    @property
    def sender_email(self):
        from_ = self.__parsed_email.from_
        is_redirection = False
        email_list = []
        for elem in from_:  # [( John Doe, john.doe@mail.be )]
            for sub_elem in elem:  # ( John Doe, john.doe@mail.be )
                ssub_elem_list = sub_elem.split()
                for ssub_elem in ssub_elem_list:  # ['John', 'Doe', 'john.doe@mail.be']
                    if ssub_elem == "via":
                        # Two email addresses can be included in the sender field in the case of email redirection
                        # In this case the keyword "via" is in the sender field
                        is_redirection = True
                    elif '@' in ssub_elem and '.' in ssub_elem:
                        ssub_elem = ssub_elem.lower()
                        ssub_elem = ssub_elem.replace('<', '')
                        ssub_elem = ssub_elem.replace('>', '')
                        ssub_elem = ssub_elem.replace('"', '')
                        ssub_elem = ssub_elem.replace("'", '')
                        if ssub_elem not in email_list:
                            email_list.append(ssub_elem)
        if not email_list:
            raise ValueError(
                f"""No email address was found in sender field. Class: {self.__class__} , Fiels: {from_}""")
        elif len(email_list) == 1:
            return email_list[0]
        elif len(email_list) == 2 and is_redirection:
            # if it is an email redirection, we take the email address of the original sender
            return email_list[0]
        elif len(email_list) == 2 and not is_redirection:
            # if it is not a redirection then the last field assimilated to an email address is the email address.
            # Because we assume that in front it is the name in the form of an email address probably rewritten incorrectly
            return email_list[1]
        else:
            raise ValueError(
                f"""More than two string has been assimilated to a sender email address. Class: {self.__class__} , Fiels: {from_}""")

    @property
    def subject(self):
        # Extraire le sujet de l'email
        return self.__parsed_email.subject

    @property
    def recipients_to_2(self):
        # Extraire les destinataires de l'email
        return self.__parsed_email.to

    @property
    def recipients_to(self):
        delivered_to =None
        delivered_to2 = None
        address_list = []
        # Expression régulière pour vérifier si la chaîne ressemble à une adresse e-mail
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        # Extraire les en-têtes JSON
        headers_json = self.__parsed_email.headers_json
        if headers_json:
            headers = json.loads(headers_json)
            for key in headers.keys():
                # Recherche de la clé "To", "TO", ou "to" (insensible à la casse)
                if re.match(r'(?i)^to$', key):
                    delivered_to = headers[key]
                # Recherche de la clé "Delivered-To" (insensible à la casse)
                if re.match(r'(?i)^X-Original-To$', key):
                    delivered_to2 = headers[key]

            if not delivered_to or not delivered_to.strip():
                delivered_to = delivered_to2
            if delivered_to:
                str_to = delivered_to.split(',')
                for elem in str_to:  # parcours nom + email de chaque personne
                    sub_elems = elem.split(' ')
                    for sub_elem in sub_elems:  # parcours du nom et de l'email de la personne
                        if sub_elem.startswith("<") and sub_elem.endswith(">") and '@' in sub_elem:
                            sub_elem = sub_elem.replace('<', '')
                            sub_elem = sub_elem.replace('>', '')
                            address_list.append(sub_elem)
            return address_list

        else:
            print(f"No headers detected")
        return None

    @property
    def recipients_cc(self):
        str_cc = None
        address_list = []
        # Expression régulière pour vérifier si la chaîne ressemble à une adresse e-mail
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        # Extraire les en-têtes JSON
        headers_json = self.__parsed_email.headers_json
        if headers_json:
            headers = json.loads(headers_json)
            for key in headers.keys():
                # Recherche de la clé "Cc", "CC", ou "cc" ... (insensible à la casse)
                if re.match(r'(?i)^cc$', key):
                    str_cc = headers[key]
            if str_cc:
                str_cc = str_cc.split(',')
                for elem in str_cc:  # parcours nom + email de chaque personne
                    sub_elems = elem.split(' ')
                    for sub_elem in sub_elems:  # parcours du nom et de l'email de la personne
                        if sub_elem.startswith("<") and sub_elem.endswith(">") and '@' in sub_elem:
                            sub_elem = sub_elem.replace('<', '')
                            sub_elem = sub_elem.replace('>', '')
                            address_list.append(sub_elem)
                return address_list
        return None

    @property
    def recipients_bcc(self):
        str_bcc = None
        address_list = []
        # Expression régulière pour vérifier si la chaîne ressemble à une adresse e-mail
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        # Extraire les en-têtes JSON
        headers_json = self.__parsed_email.headers_json
        if headers_json:
            headers = json.loads(headers_json)
            for key in headers.keys():
                # Recherche de la clé "Bcc", "BCC", ou "bcc"... (insensible à la casse)
                if re.match(r'(?i)^bcc$', key):
                    str_bcc = headers[key]
            if str_bcc:
                str_bcc = str_bcc.split(',')
                for elem in str_bcc:  # parcours nom + email de chaque personne
                    sub_elems = elem.split(' ')
                    for sub_elem in sub_elems:  # parcours du nom et de l'email de la personne
                        if sub_elem.startswith("<") and sub_elem.endswith(">") and '@' in sub_elem:
                            sub_elem = sub_elem.replace('<', '')
                            sub_elem = sub_elem.replace('>', '')
                            address_list.append(sub_elem)
                return address_list
            return None

    def date(self, timezone=TIMEZONE):
        headers_json = self.__parsed_email.headers_json
        if headers_json:
            headers = json.loads(headers_json)
            for key in headers.keys():
                # Recherche de la clé "Date"... (insensible à la casse)
                if re.match(r'(?i)^Date$', key):
                    date_str = headers[key]
                    date_splited = date_str.split()
                    date_str = ''
                    for elem in date_splited:
                        if elem.startswith('(GMT') and elem.endswith(')'):
                            elem = '(GMT)'
                        date_str += elem + ' '
            # Analyse de la date avec dateutil
            parsed_date = parser.parse(date_str)
            tz = pytz.timezone(timezone)
        date_with_tz = parsed_date.astimezone(tz)
        return date_with_tz.date()

    def strdate(self, timezone=TIMEZONE):
        return str(self.date(timezone)).replace('-', '')

    def time(self, timezone=TIMEZONE):
        headers_json = self.__parsed_email.headers_json
        if headers_json:
            headers = json.loads(headers_json)
            for key in headers.keys():
                # Recherche de la clé "Date"... (insensible à la casse)
                if re.match(r'(?i)^Date$', key):
                    date_str = headers[key]
                    date_splited = date_str.split()
                    date_str = ''
                    for elem in date_splited:
                        if elem.startswith('(GMT') and elem.endswith(')'):
                            elem = '(GMT)'
                        date_str += elem + ' '
            # Analyse de la date avec dateutil
            parsed_date = parser.parse(date_str)
            tz = pytz.timezone(timezone)
        date_with_tz = parsed_date.astimezone(tz)
        return date_with_tz.time()

    def strtime(self, timezone=TIMEZONE):
        return str(self.time(timezone)).replace(':', '')

    @property
    def body(self):
        return self.__parsed_email.body

    @property
    def filename(self):
        return self.__filename

    @property
    def attachments_names(self):
        attachments_names_list = []
        attachments = self.__attachments
        for attachment in attachments:
            attachments_names_list.append(attachment['filename'])
        return attachments_names_list

    @property
    def attachments(self):
        attachments_list = []
        attachments = self.__attachments
        for attachment in attachments:
            attachments_list.append(attachment)
        return attachments_list

    def __str__(self):
        return f"""
        Name sender:\t{self.sender_name()}\n
        Email sender:\t{self.sender_email()}\n
        Subject:\t{self.subject()}\n
        Recipients to:\t{self.recipients_to()}\n
        Recipients cc:\t{self.recipients_cc()}\n
        Recipients bcc:\t{self.recipients_bcc()}\n
        Date:\t{self.date()}\n
        Time:\t{self.time()}\n
        Body:\t{self.body()}\n
        Filename:\t{self.filename()}\n
        Attachments names:\t{self.attachments_names()}\n\n
        """


