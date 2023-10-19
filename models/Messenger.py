import re
from dateutil import parser
from datetime import datetime
class Messenger:
    """
        A class representing a message in a messaging application.

        Attributes:
        - conversation_name (str): The name of the conversation or group.
        - fullname (str): The full name of the sender.
        - date (str): The date string of the message in the format "day month year hour:minute".
        - message (str): The content of the message.

        Properties:
        - conversation_name (str): Getter for the conversation_name attribute.
        - fullname (str): Getter for the fullname attribute.
        - message (str): Getter for the message attribute.
        - date (datetime.date): Getter for the date attribute, parsed from the date string.
        - time (datetime.time): Getter for the time attribute, parsed from the date string.
        - strdate (str): Getter for the date attribute in string format (YYYY-MM-DD).
        - strtime (str): Getter for the time attribute in string format (HHMM).

        Methods:
        - __str__(): Returns a string representation of the Messenger object.

        Note: The date string is expected to be in the format "day month year hour:minute",
        and it uses a dictionary to map month names to their numerical values.
        """
    def __init__(self, conversation_name, fullname, date, message):
        self.__conversation_name = conversation_name
        self.__fullname = fullname
        self.__date = date
        self.__message = message


    @property
    def conversation_name(self):
        return self.__conversation_name

    @property
    def fullname(self):
        return self.__fullname

    @property
    def message(self):
        return self.__message

    @property
    def date(self):
        month_dict = {
            'janv.': 1,
            'févr.': 2,
            'mars': 3,
            'avr.': 4,
            'mai': 5,
            'juin': 6,
            'juil.': 7,
            'août': 8,
            'sept.': 9,
            'oct.': 10,
            'nov.': 11,
            'déc.': 12
        }
        date_str = self.__date
        date_list = date_str.split()

        # Utiliser le dictionnaire pour obtenir le numéro du mois
        month_num = month_dict.get(date_list[1])

        # Créer un objet datetime à partir des parties de date
        date_obj = datetime(    year=int(date_list[2]),
                                month=month_num,
                                day=int(date_list[0]),
                                hour=int(date_list[4].split(':')[0]),
                                minute=int(date_list[4].split(':')[1]))

        return date_obj.date()

    @property
    def time(self):
        month_dict = {
            'janv.': 1,
            'févr.': 2,
            'mars': 3,
            'avr.': 4,
            'mai': 5,
            'juin': 6,
            'juil.': 7,
            'août': 8,
            'sept.': 9,
            'oct.': 10,
            'nov.': 11,
            'déc.': 12
        }
        date_str = self.__date
        date_list = date_str.split()

        # Utiliser le dictionnaire pour obtenir le numéro du mois
        month_num = month_dict.get(date_list[1])

        # Créer un objet datetime à partir des parties de date
        date_obj = datetime(year=int(date_list[2]),
                            month=month_num,
                            day=int(date_list[0]),
                            hour=int(date_list[4].split(':')[0]),
                            minute=int(date_list[4].split(':')[1]))

        return date_obj.time()

    @property
    def strdate(self):
        return str(self.date).replace('-', '')

    @property
    def strtime(self):
        return str(self.time).replace(':', '')

    def __str__(self):
        return f"""
            Conversation name: {self.conversation_name}\n
            Full name: {self.fullname}\n
            Date: {self.date}\n
            Time: {self.time}\n
            Message: {self.message}\n\n
            """