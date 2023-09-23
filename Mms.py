import datetime
class MmsAddress:
    def __init__(self, address, type, charset):
        self.__address = address
        self.__type = type
        self.__charset = charset

    @property
    def address(self):
        return self.__address

    @property
    def type(self):
        return self.__type

    @property
    def charset(self):
        return self.__charset

    def __str__(self):
        return f"""
            Address:\t{self.address}\n
            Type:\t{self.type}\n
            Charset:\t{self.charset}\n\n"""
class MmsPart:
    def __init__(self, seq, ct, name, chset, cd, fn, cid, cl, ctt_s, ctt_t, text, data=None):
        self.__seq = seq
        self.__ct = ct
        self.__name = name
        self.__chset = chset
        self.__cd = cd
        self.__fn = fn
        self.__cid = cid
        self.__cl = cl
        self.__ctt_s = ctt_s
        self.__ctt_t = ctt_t
        self.__text = text
        self.__data = data

    @property
    def seq(self):
        return self.__seq

    @property
    def ct(self):
        return self.__ct

    @property
    def name(self):
        return self.__name

    @property
    def chset(self):
        return self.__chset

    @property
    def cd(self):
        return self.__cd

    @property
    def fn(self):
        return self.__fn

    @property
    def cid(self):
        return self.__cid

    @property
    def cl(self):
        return self.__cl

    @property
    def ctt_s(self):
        return self.__ctt_s

    @property
    def ctt_t(self):
        return self.__ctt_t

    @property
    def text(self):
        return self.__text

    @property
    def data(self):
        return self.__data

    def __str__(self):
        return f"""
                Seq:\t{self.seq}\n
                Ct:\t{self.ct}\n
                Name:\t{self.name}\n
                Chset:\t{self.chset}\n
                Cd:\t{self.cd}\n
                Fn:\t{self.fn}\n
                Cid:\t{self.cid}\n
                Cl:\t{self.cl}\n
                Ctt_s:\t{self.ctt_s}\n
                Ctt_t:\t{self.ctt_t}\n
                Text:\t{self.text}\n
                Data:\t{self.data}\n\n"""
class MMS:
    """
    Represents a Multimedia Messaging Service (MMS) message.

    Args:
        date (str): The date and time of the message.
        rr (str): Read receipt status.
        sub (str): Subject of the message.
        ct_t (str): Content type.
        read_status (str): Read status of the message.
        seen (str): Seen status of the message.
        msg_box (str): Message box identifier.
        address (str): The address associated with the message.
        sub_cs (str): Subject character set.
        resp_st (str): Response status.
        retr_st (str): Retrieve status.
        d_tm (str): Date and time of the message.
        text_only (str): Indicates if the message contains only text.
        exp (str): Expiry status of the message.
        locked (str): Lock status of the message.
        m_id (str): Message ID.
        st (str): Status of the message.
        retr_txt_cs (str): Retrieve text character set.
        retr_txt (str): Retrieved text.
        creator (str): Message creator.
        date_sent (str): Date when the message was sent.
        read (str): Read status of the message.
        m_size (str): Message size.
        rpt_a (str): Report address.
        ct_cls (str): Content class.
        pri (str): Priority of the message.
        sub_id (str): Submission ID.
        tr_id (str): Transaction ID.
        resp_txt (str): Response text.
        ct_l (str): Content location.
        m_cls (str): Message class.
        d_rpt (str): Delivery report.
        v (str): Version.
        _id (str): Message ID.
        m_type (str): Message type.
        readable_date (str): Readable date.
        contact_name (str): Contact name.
        parts (list): List of MmsPart objects.
        addrs (list): List of MmsAddress objects.

    Attributes:
        recipient_list (list): List of recipient addresses.
        timestamp (str): The date and time of the message as a string.
        date (datetime.date): The date of the message.
        time (datetime.time): The time of the message.
        strdate (str): The date of the message as a string (YYYYMMDD).
        strtime (str): The time of the message as a string (HHMMSS).
        type_msg_box (str): Message box type (Received or Sent).

    Methods:
        __str__(): Returns a formatted string representation of the message.

    Example:
        mms = MMS(date='2023-08-30 14:30:00', rr='Read', sub='Hello', ct_t='Text', read_status='Unread', seen='No',
                  msg_box='1', address='alice@example.com', sub_cs='UTF-8', resp_st='OK', retr_st='Complete',
                  d_tm='2023-08-30 14:30:00', text_only='Yes', exp='No', locked='No', m_id='12345', st='Received',
                  retr_txt_cs='UTF-8', retr_txt='Message content', creator='John Doe', date_sent='2023-08-30',
                  read='No', m_size='1024', rpt_a='report@example.com', ct_cls='Personal', pri='Normal',
                  sub_id='56789', tr_id='98765', resp_txt='Response', ct_l='Location', m_cls='Standard',
                  d_rpt='No', v='1.0', _id='54321', m_type='Received', readable_date='30 août 2023 14:30:00',
                  contact_name='Alice', parts=[MmsPart(...)], addrs=[MmsAddress(...)])
        print(mms)

    Note:
        - The `date` and `time` attributes are parsed into date and time objects for convenience.
    """
    def __init__(self, date, rr, sub, ct_t, read_status, seen, msg_box, address, sub_cs, resp_st, retr_st, d_tm,
                 text_only, exp, locked, m_id, st, retr_txt_cs, retr_txt, creator, date_sent, read, m_size, rpt_a,
                 ct_cls, pri, sub_id, tr_id, resp_txt, ct_l, m_cls, d_rpt, v, _id, m_type, readable_date, contact_name,
                 parts, addrs):
        self.__date = date
        self.__rr = rr
        self.__sub = sub
        self.__ct_t = ct_t
        self.__read_status = read_status
        self.__seen = seen
        self.__msg_box = msg_box
        self.__address = address
        self.__sub_cs = sub_cs
        self.__resp_st = resp_st
        self.__retr_st = retr_st
        self.__d_tm = d_tm
        self.__text_only = text_only
        self.__exp = exp
        self.__locked = locked
        self.__m_id = m_id
        self.__st = st
        self.__retr_txt_cs = retr_txt_cs
        self.__retr_txt = retr_txt
        self.__creator = creator
        self.__date_sent = date_sent
        self.__read = read
        self.__m_size = m_size
        self.__rpt_a = rpt_a
        self.__ct_cls = ct_cls
        self.__pri = pri
        self.__sub_id = sub_id
        self.__tr_id = tr_id
        self.__resp_txt = resp_txt
        self.__ct_l = ct_l
        self.__m_cls = m_cls
        self.__d_rpt = d_rpt
        self.__v = v
        self.__id = _id
        self.__m_type = m_type
        self.__readable_date = readable_date
        self.__contact_name = contact_name
        self.__parts = parts  # MmsPart object
        self.__addrs = addrs  # MmsAddress object

    @property
    def recipient_list(self):
        addr_list = []
        for address_obj in self.__addrs:
            addr_list.append(address_obj.address)
        return addr_list
    @property
    def timestamp(self):
        return self.__date

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
    def rr(self):
        return self.__rr

    @property
    def sub(self):
        return self.__sub

    @property
    def ct_t(self):
        return self.__ct_t

    @property
    def read_status(self):
        return self.__read_status

    @property
    def seen(self):
        return self.__seen

    @property
    def msg_box(self):
        return self.__msg_box

    @property
    def type_msg_box(self):
        if self.__msg_box == '1':
            return "Received"
        elif self.__msg_box == '2':
            return "Sent"
        else:
            return None

    @property
    def address(self):
        return self.__address

    @property
    def sub_cs(self):
        return self.__sub_cs

    @property
    def resp_st(self):
        return self.__resp_st

    @property
    def retr_st(self):
        return self.__retr_st

    @property
    def d_tm(self):
        return self.__d_tm

    @property
    def text_only(self):
        return self.__text_only

    @property
    def exp(self):
        return self.__exp

    @property
    def locked(self):
        return self.__locked

    @property
    def m_id(self):
        return self.__m_id

    @property
    def st(self):
        return self.__st

    @property
    def retr_txt_cs(self):
        return self.__retr_txt_cs

    @property
    def retr_txt(self):
        return self.__retr_txt

    @property
    def creator(self):
        return self.__creator

    @property
    def date_sent(self):
        return self.__date_sent

    @property
    def read(self):
        return self.__read

    @property
    def m_size(self):
        return self.__m_size

    @property
    def rpt_a(self):
        return self.__rpt_a

    @property
    def ct_cls(self):
        return self.__ct_cls

    @property
    def pri(self):
        return self.__pri

    @property
    def sub_id(self):
        return self.__sub_id

    @property
    def tr_id(self):
        return self.__tr_id

    @property
    def resp_txt(self):
        return self.__resp_txt

    @property
    def ct_l(self):
        return self.__ct_l

    @property
    def m_cls(self):
        return self.__m_cls

    @property
    def d_rpt(self):
        return self.__d_rpt

    @property
    def v(self):
        return self.__v

    @property
    def id(self):
        return self.__id

    @property
    def m_type(self):
        return self.__m_type

    @property
    def readable_date(self):
        return self.__readable_date

    @property
    def contact_name(self):
        return self.__contact_name

    @property
    def parts(self):
        return self.__parts

    @property
    def addrs(self):
        return self.__addrs

    def __str__(self):
        return f"""
        Date: {self.date} {self.time}
        Read Receipt: {self.rr}
        Subject: {self.sub}
        Content Type: {self.ct_t}
        Read Status: {self.read_status}
        Seen: {self.seen}
        Message Box: {self.msg_box} ({self.type_msg_box})
        Recipient List: {', '.join(self.recipient_list)}  # Utilisation de la nouvelle propriété
        Sub Charset: {self.sub_cs}
        Response Status: {self.resp_st}
        Retrieve Status: {self.retr_st}
        Date Time: {self.d_tm}
        Text Only: {self.text_only}
        Expiry: {self.exp}
        Locked: {self.locked}
        Message ID: {self.m_id}
        Status: {self.st}
        Retrieve Text Charset: {self.retr_txt_cs}
        Retrieve Text: {self.retr_txt}
        Creator: {self.creator}
        Date Sent: {self.date_sent}
        Read: {self.read}
        Message Size: {self.m_size}
        Report Address: {self.rpt_a}
        Content Class: {self.ct_cls}
        Priority: {self.pri}
        Submission ID: {self.sub_id}
        Transaction ID: {self.tr_id}
        Response Text: {self.resp_txt}
        Content Location: {self.ct_l}
        Message Class: {self.m_cls}
        Delivery Report: {self.d_rpt}
        Version: {self.v}
        ID: {self.id}
        Message Type: {self.m_type}
        Readable Date: {self.readable_date}
        Contact Name: {self.contact_name}
        """
