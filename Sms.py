import datetime


class SMS:
    """
    Represents a Short Message Service (SMS) message.

    Attributes:
        protocol (str): The protocol of the SMS.
        address (str): The recipient's address.
        date (str): The date of the SMS.
        type (str): The type of the SMS (e.g., "Received" or "Sent").
        subject (str): The subject of the SMS.
        body (str): The body or content of the SMS.
        toa (str): Type of Address for the recipient.
        sc_toa (str): Service Center Type of Address.
        service_center (str): The service center associated with the SMS.
        read (str): Whether the SMS has been read.
        status (str): The status of the SMS.
        locked (str): Whether the SMS is locked.
        date_sent (str): The date the SMS was sent.
        sub_id (str): The subscription ID.
        readable_date (str): The human-readable date of the SMS.
        contact_name (str): The name of the contact associated with the SMS.

    Methods:
        recipient_list: Returns a list of recipient addresses.
        timestamp: Returns the timestamp of the SMS.
        type_str: Returns the type of the SMS as a string.
        date: Returns the date of the SMS as a datetime.date object.
        time: Returns the time of the SMS as a datetime.time object.
        strdate: Returns the date of the SMS as a string without dashes.
        strtime: Returns the time of the SMS as a string without colons.

    Example:
        sms = SMS(protocol="SMS",
                  address="12345",
                  date="2023-08-30 12:34:56",
                  type="1",
                  subject="Hello",
                  body="Hi there!",
                  toa="SMR",
                  sc_toa="SCA",
                  service_center="98765",
                  read="1",
                  status="-1",
                  locked="0",
                  date_sent="2023-08-30 12:34:56",
                  sub_id="1",
                  readable_date="30 août 2023 12:34:56",
                  contact_name="John Doe")
        print(sms)
    """
    def __init__(self, protocol, address, date, type, subject, body, toa, sc_toa, service_center, read, status,
                 locked, date_sent, sub_id, readable_date, contact_name):
        self.__protocol = protocol
        self.__address = address
        self.__date = date
        self.__type = type
        self.__subject = subject
        self.__body = body
        self.__toa = toa
        self.__sc_toa = sc_toa
        self.__service_center = service_center
        self.__read = read
        self.__status = status
        self.__locked = locked
        self.__date_sent = date_sent
        self.__sub_id = sub_id
        self.__readable_date = readable_date
        self.__contact_name = contact_name

    @property
    def protocol(self):
        return self.__protocol

    @property
    def address(self):
        return self.__address

    @property
    def recipient_list(self):
        addr_list = []
        if len(self.__address) > 18:
            addresses = self.__address.split(' ')
            for address in addresses:
                addr_list.append(address)
        else:
            address = self.__address.replace(' ', '')
            addr_list.append(address)
        return addr_list


    @property
    def timestamp(self):
        return self.__date

    @property
    def type_str(self):
        if self.__type == '1':
            return "Received"
        elif self.__type == '2':
            return "Sent"
        else:
            return None
    @property
    def type(self):
        return self.__type

    @property
    def subject(self):
        return self.__subject

    @property
    def body(self):
        return self.__body

    @property
    def toa(self):
        return self.__toa

    @property
    def sc_toa(self):
        return self.__sc_toa

    @property
    def service_center(self):
        return self.__service_center

    @property
    def read(self):
        return self.__read

    @property
    def status(self):
        return self.__status

    @property
    def locked(self):
        return self.__locked

    @property
    def date_sent(self):
        return self.__date_sent

    @property
    def sub_id(self):
        return self.__sub_id

    @property
    def readable_date(self):
        return self.__readable_date

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
        date_str = self.__readable_date
        date_list = date_str.split()

        # Utiliser le dictionnaire pour obtenir le numéro du mois
        month_num = month_dict.get(date_list[1])

        # Créer un objet datetime à partir des parties de date
        date_obj = datetime.datetime(year=int(date_list[2]),
                                     month=month_num,
                                     day=int(date_list[0]),
                                     hour=int(date_list[3].split(':')[0]),
                                     minute=int(date_list[3].split(':')[1]),
                                     second=int(date_list[3].split(':')[2]))

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
        date_str = self.__readable_date
        date_list = date_str.split()

        # Utiliser le dictionnaire pour obtenir le numéro du mois
        month_num = month_dict.get(date_list[1])

        # Créer un objet datetime à partir des parties de date
        date_obj = datetime.datetime(year=int(date_list[2]),
                                     month=month_num,
                                     day=int(date_list[0]),
                                     hour=int(date_list[3].split(':')[0]),
                                     minute=int(date_list[3].split(':')[1]),
                                     second=int(date_list[3].split(':')[2]))

        return date_obj.time()

    @property
    def strdate(self):
        return str(self.date).replace('-', '')

    @property
    def strtime(self):
        return str(self.time).replace(':', '')

    @property
    def contact_name(self):
        return self.__contact_name

    def __str__(self):
        return f"""
        Protocol: {self.protocol}
        Address: {self.address}
        Timestamp: {self.timestamp}
        Type: {self.type}
        Subject: {self.subject}
        Body: {self.body}
        Toa: {self.toa}
        Sc_toa: {self.sc_toa}
        Service Center: {self.service_center}
        Read: {self.read}
        Status: {self.status}
        Locked: {self.locked}
        Date Sent: {self.date_sent}
        Sub Id: {self.sub_id}
        Readable Date: {self.readable_date}
        Date: {self.date}
        Time: {self.time}
        Contact Name: {self.contact_name}
        """

