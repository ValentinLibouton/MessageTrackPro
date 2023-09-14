class Message:
    """
    This classe represent a message. A message can be an email, a, sms, or an mms
    """
    def __init__(self, sender_address, receivers_adresses, sender_name, receivers_names, date, time, content):
        self.sender_address = sender_address
        self.receivers_adresses = receivers_adresses
        self.sender_name = sender_name
        self.receivers_names = receivers_names
        self.date = date
        self.time = time
        self.content = content