import xml.etree.ElementTree as ET
import sms as s, mms as m
import os
from dotenv import load_dotenv
# Load environnement variables from .env
dotenv_path = "variables.env"
load_dotenv(dotenv_path)

# Get environnement variables
XML_FILE_DIRECTORY = os.getenv("XML_FILE_DIRECTORY")
SMS_FILENAME = os.getenv("SMS_FILENAME")

xml_file_path = f"{XML_FILE_DIRECTORY}/{SMS_FILENAME}"


def read_sms_mms_from_xml(xml_file_path):
    sms_list = []
    mms_list = []
    # Vérification si xml_file_path est None
    if xml_file_path is None:
        print(f"Le fichier xml_file_path est inexistant, impossible de lire les sms et mms")
        return sms_list, mms_list

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for sms_element in root.findall('.//sms'):
        protocol = sms_element.get('protocol')
        address = sms_element.get('address')
        date = sms_element.get('date')
        type = sms_element.get('type')
        subject = sms_element.get('subject')
        body = sms_element.get('body')
        toa = sms_element.get('toa')
        sc_toa = sms_element.get('sc_toa')
        service_center = sms_element.get('service_center')
        read = sms_element.get('read')
        status = sms_element.get('status')
        locked = sms_element.get('locked')
        date_sent = sms_element.get('date_sent')
        sub_id = sms_element.get('sub_id')
        readable_date = sms_element.get('readable_date')
        contact_name = sms_element.get('contact_name')

        sms = s.SMS(protocol=protocol, address=address, date=date, type=type, subject=subject, body=body, toa=toa,
                  sc_toa=sc_toa, service_center=service_center, read=read, status=status, locked=locked,
                  date_sent=date_sent, sub_id=sub_id, readable_date=readable_date, contact_name=contact_name)
        sms_list.append(sms)

    # Metadata extraction
    for mms_element in root.findall('.//mms'):
        date = mms_element.get('date')
        rr = mms_element.get('rr')
        sub = mms_element.get('sub')
        ct_t = mms_element.get('ct_t')
        read_status = mms_element.get('read_status')
        seen = mms_element.get('seen')
        msg_box = mms_element.get('msg_box')
        address = mms_element.get('address')
        sub_cs = mms_element.get('sub_cs')
        resp_st = mms_element.get('resp_st')
        retr_st = mms_element.get('retr_st')
        d_tm = mms_element.get('d_tm')
        text_only = mms_element.get('text_only')
        exp = mms_element.get('exp')
        locked = mms_element.get('locked')
        m_id = mms_element.get('m_id')
        st = mms_element.get('st')
        retr_txt_cs = mms_element.get('retr_txt_cs')
        retr_txt = mms_element.get('retr_txt')
        creator = mms_element.get('creator')
        date_sent = mms_element.get('date_sent')
        read = mms_element.get('read')
        m_size = mms_element.get('m_size')
        rpt_a = mms_element.get('rpt_a')
        ct_cls = mms_element.get('ct_cls')
        pri = mms_element.get('pri')
        sub_id = mms_element.get('sub_id')
        tr_id = mms_element.get('tr_id')
        resp_txt = mms_element.get('resp_txt')
        ct_l = mms_element.get('ct_l')
        m_cls = mms_element.get('m_cls')
        d_rpt = mms_element.get('d_rpt')
        v = mms_element.get('v')
        _id = mms_element.get('_id')
        m_type = mms_element.get('m_type')
        readable_date = mms_element.get('readable_date')
        contact_name = mms_element.get('contact_name')


        # Extraction of MMS elements (text/plain, image,...)
        parts_list = []
        parts = mms_element.findall('parts/part')
        for part in parts:
            seq = part.get('seq')
            ct = part.get('ct')
            name = part.get('name')
            chset = part.get('chset')
            cd = part.get('cd')
            fn = part.get('fn')
            cid = part.get('cid')
            cl = part.get('cl')
            ctt_s = part.get('ctt_s')
            ctt_t = part.get('ctt_t')
            text = part.get("text")
            data = part.get("data")

            part = m.MmsPart(seq=seq, ct=ct, name=name, chset=chset, cd=cd, fn=fn, cid=cid, cl=cl, ctt_s=ctt_s,
                           ctt_t=ctt_t, text=text, data=data)
            parts_list.append(part)

        #Extraction of addresses
        addrs_list = []
        addrs = mms_element.findall('addrs/addr')
        for addr in addrs:
            address = addr.get('address')
            type = addr.get('type')
            charset = addr.get('charset')

            addr = m.MmsAddress(address=address, type=type, charset=charset)
            addrs_list.append(addr)

        mms = m.MMS(date=date, rr=rr, sub=sub, ct_t=ct_t, read_status=read_status,  seen=seen, msg_box=msg_box,
                  address=address, sub_cs=sub_cs, resp_st=resp_st, retr_st=retr_st, d_tm=d_tm, text_only=text_only,
                  exp=exp, locked=locked, m_id=m_id, st=st, retr_txt_cs=retr_txt_cs, retr_txt=retr_txt, creator=creator,
                  date_sent=date_sent, read=read, m_size=m_size, rpt_a=rpt_a, ct_cls=ct_cls, pri=pri, sub_id=sub_id,
                  tr_id=tr_id, resp_txt=resp_txt, ct_l=ct_l, m_cls=m_cls, d_rpt=d_rpt, v=v, _id=_id, m_type=m_type,
                  readable_date= readable_date, contact_name=contact_name, parts=parts_list, addrs=addrs_list)
        mms_list.append(mms)

    return sms_list, mms_list