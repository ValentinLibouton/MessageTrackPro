class SMS:
    def __init__(self, protocol, address, date, type, subject, body, toa, sc_toa, service_center, read, status,
                 locked, date_sent, sub_id, readable_date, contact_name):
        self.protocol = protocol
        self.address = address
        self.date = date
        self.type = type
        self.subject = subject
        self.body = body
        self.toa = toa
        self.sc_toa = sc_toa
        self.service_center = service_center
        self.read = read
        self.status = status
        self.locked = locked
        self.date_sent = date_sent
        self.sub_id = sub_id
        self.readable_date = readable_date
        self.contact_name = contact_name