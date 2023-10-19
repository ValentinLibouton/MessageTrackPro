from dateutil import parser
import datetime
class Message:
    """
    Represents an email message.

    Args:
        sender_name (str): The name of the message sender.
        sender_address (str): The email address of the message sender.
        recipient_type (str): The type of recipient (e.g., 'To', 'Cc', 'Bcc').
        recipient_name (str): The name of the message recipient.
        recipient_address (str): The email address of the message recipient.
        date (str): The date of the message in string format.
        time (str): The time of the message in string format.
        original_filename (str): The original filename of the message.
        content (str): The content or body of the message.
        attachments (list): A list of attachment filenames.
        tags (list): A list of tags associated with the message.
        message_id (str): The unique message identifier.

    Attributes:
        sender_name (str): The name of the message sender.
        sender_address (str): The email address of the message sender.
        recipient_type (str): The type of recipient (e.g., 'To', 'Cc', 'Bcc').
        recipient_name (str): The name of the message recipient.
        recipient_address (str): The email address of the message recipient.
        strdate (str): The date of the message in string format.
        date (datetime.date): The date of the message as a date object.
        strtime (str): The time of the message in string format.
        time (datetime.time): The time of the message as a time object.
        fulldate (datetime.datetime): The full date and time of the message as a datetime object.
        filename (str): The original filename of the message.
        content (str): The content or body of the message.
        attachments (list): A list of attachment filenames.
        tags (list): A list of tags associated with the message.
        message_id (str): The unique message identifier.

    Methods:
        __str__(): Returns a formatted string representation of the message.

    Example:
        message = Message(sender_name='John Doe', sender_address='johndoe@example.com', recipient_type='To',
                          recipient_name='Alice', recipient_address='alice@example.com', date='2023-08-30',
                          time='14:30:00', original_filename='email.eml', content='Hello, Alice!',
                          attachments=['attachment1.pdf'], tags=['Important'], message_id='12345')
        print(message)

    Note:
        - The `date` and `time` attributes are parsed into date and time objects for convenience.
    """

    def __init__(self, sender_name, sender_address, recipient_type, recipient_name, recipient_address, date, time,
                 subject, original_filename, content, attachments, tags, message_id):
        self.__sender_name = sender_name
        self.__sender_address = sender_address
        self.__recipient_type = recipient_type
        self.__recipient_name = recipient_name
        self.__recipient_address = recipient_address
        self.__date = date
        self.__time = time
        self.__subject = subject
        self.__original_filename = original_filename
        self.__content = content
        self.__attachments = attachments
        self.__tags = tags
        self.__message_id = message_id


    @property
    def sender_name(self):
        return self.__sender_name

    @property
    def sender_address(self):
        return self.__sender_address

    @property
    def recipient_type(self):
        return self.__recipient_type

    @property
    def recipient_name(self):
        return self.__recipient_name

    @property
    def recipient_address(self):
        return self.__recipient_address

    @property
    def strdate(self):
        return self.__date

    @property
    def date(self):
        date = self.strdate
        _date_obj = parser.parse(date)
        return _date_obj.date()

    @property
    def strtime(self):
        return self.__time

    @property
    def time(self):
        time = self.strtime
        _time_obj = parser.parse(time)
        return _time_obj.time()

    @property
    def fulldate(self):
        return datetime.datetime.combine(self.date, self.time)

    @property
    def filename(self):
        return self.__original_filename

    @property
    def content(self):
        return self.__content

    @property
    def attachments(self):
        return self.__attachments

    @property
    def tags(self):
        return self.__tags

    @property
    def message_id(self):
        return self.__message_id

    @property
    def subject(self):
        return self.__subject

    def __str__(self):
        return f"""
                Name sender:\t{self.sender_name}\n
                Subject:\t{self.subject}\n
                Email sender:\t{self.sender_address}\n
                Recipient type:\t{self.recipient_type}\n
                Recipients to:\t{self.recipient_name}\n
                Recipient address:\t{self.recipient_address}\n
                Date:\t{self.date}\n
                Time:\t{self.time}\n
                Filename:\t{self.filename}\n
                Attachments names:\t{self.attachments}\n
                Tags:\t{self.tags}\n
                Message id:\t{self.message_id}\n
                Body:\t{self.content}\n\n
                """

