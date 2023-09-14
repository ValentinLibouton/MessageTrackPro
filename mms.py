
class MmsAddress:
    def __init__(self, address, type, charset):
        self.address = address
        self.type = type
        self.charset = charset
class MmsPart:
    def __init__(self, seq, ct, name, chset, cd, fn, cid, cl, ctt_s, ctt_t, text, data=None):
        self.seq = seq
        self.ct = ct
        self.name = name
        self.chset = chset
        self.cd = cd
        self.fn = fn
        self.cid = cid
        self.cl = cl
        self.ctt_s = ctt_s
        self.ctt_t = ctt_t
        self.text = text
        self.data = data
class MMS:
    def __init__(self, date, rr, sub, ct_t, read_status, seen, msg_box, address, sub_cs, resp_st, retr_st, d_tm,
                 text_only, exp, locked, m_id, st, retr_txt_cs, retr_txt, creator, date_sent, read, m_size, rpt_a,
                 ct_cls, pri, sub_id, tr_id, resp_txt, ct_l, m_cls, d_rpt, v, _id, m_type, readable_date, contact_name,
                 parts, addrs):
        self.date = date
        self.rr = rr
        self.sub = sub
        self.ct_t = ct_t
        self.read_status = read_status
        self.seen = seen
        self.msg_box = msg_box
        self.address = address
        self.sub_cs = sub_cs
        self.resp_st = resp_st
        self.retr_st =retr_st
        self.d_tm = d_tm
        self.text_only = text_only
        self.exp = exp
        self.locked = locked
        self.m_id = m_id
        self.st = st
        self.retr_txt_cs = retr_txt_cs
        self.retr_txt = retr_txt
        self.creator = creator
        self.date_sent = date_sent
        self.read = read
        self.m_size = m_size
        self.rpt_a = rpt_a
        self.ct_cls = ct_cls
        self.pri = pri
        self.sub_id = sub_id
        self.tr_id = tr_id
        self.resp_txt = resp_txt
        self.ct_l = ct_l
        self.m_cls = m_cls
        self.d_rpt = d_rpt
        self.v = v
        self._id = _id
        self.m_type = m_type
        self.readable_date = readable_date
        self.contact_name = contact_name
        self.parts = parts  # MmsPart object
        self.addrs = addrs  # MmsAddress object