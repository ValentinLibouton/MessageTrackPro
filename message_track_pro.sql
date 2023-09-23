-- Un contact possède un id, un nom et un prenom
CREATE TABLE IF NOT EXISTS Contacts (
    contact_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
);
-- Cette table lie des adresses mails à des utilisateurs. Un utilisateur peut avoir plusieurs email et email_id
CREATE TABLE IF NOT EXISTS ContactEmails (
    email_id INTEGER PRIMARY KEY,
    contact_id INTEGER,
    email TEXT,
    FOREIGN KEY (contact_id) REFERENCES Contacts(contact_id)
);

-- Cette table lie des numeros de telephone à des utilisateurs. Un utilisateur peut avoir plusieurs numéros
CREATE TABLE IF NOT EXISTS ContactPhoneNumbers (
    phone_id INTEGER PRIMARY KEY,
    contact_id INTEGER,
    phone TEXT,
    FOREIGN KEY (contact_id) REFERENCES Contacts(contact_id)
);

-- chaque fichier (pièce jointe) a un id et un nom qui est lié au message
CREATE TABLE IF NOT EXISTS Attachments (
    attachments_id INTEGER PRIMARY KEY,
    message_id INTEGER,
    filename TEXT,
    FOREIGN KEY (message_id) REFERENCES Emails(message_id)
);

-- Table représentant les données propre au message
CREATE TABLE IF NOT EXISTS Emails (
    message_id TEXT PRIMARY KEY,
    sender_email_id INTEGER,
    date DATE,
    time TIME,
    subject TEXT,
    content TEXT,
    resume TEXT,
    original_filename TEXT,
    FOREIGN KEY (sender_email_id) REFERENCES ContactEmails(email_id)
);

-- Table pour stocker les destinataires d'un message
CREATE TABLE IF NOT EXISTS RecipientEmails (
    recipient_id INTEGER PRIMARY KEY,
    message_id INTEGER,
    email_id INTEGER,
    is_cc INTEGER, -- 1 si destinataire en cc, 0 sinon
    is_bcc INTEGER, -- 1 si destinataire en bcc, 0 sinon
    FOREIGN KEY (message_id) REFERENCES Emails(message_id),
    FOREIGN KEY (email_id) REFERENCES ContactEmails(email_id)
);
CREATE TABLE IF NOT EXISTS Sms (
    sms_id TEXT PRIMARY KEY,
    type_str TEXT, -- String "Received" or "Sent"
    date DATE,
    time TIME,
    contact_name TEXT,
    body TEXT,
    original_filename TEXT,
    -- Others
    protocol TEXT,
    type TEXT,
    subject TEXT,
    toa TEXT,
    sc_toa TEXT,
    service_center TEXT,
    read TEXT,
    status TEXT,
    locked TEXT,
    date_sent TEXT,
    sub_id TEXT,
    readable_date TEXT

);
CREATE TABLE IF NOT EXISTS Sms_ContactPhoneNumber (
    sms_id INTEGER,
    phone_id INTEGER,
    FOREIGN KEY (sms_id) REFERENCES Sms (sms_id),
    FOREIGN KEY (phone_id) REFERENCES ContactPhoneNumbers (phone_id)
);


CREATE TABLE IF NOT EXISTS Calls (
    call_id INTEGER PRIMARY KEY,
    caller_phone_id INTEGER,
    date DATE,
    time TIME,
    subject TEXT,
    content TEXT,
    resume TEXT,
    callee_phone_id INTEGER,
    FOREIGN KEY (caller_phone_id) REFERENCES ContactPhoneNumbers(phone_id),
    FOREIGN KEY (callee_phone_id) REFERENCES ContactPhoneNumbers(phone_id)
);
DROP TABLE IF EXISTS Mms;
CREATE TABLE IF NOT EXISTS Mms (
    mms_id TEXT PRIMARY KEY,
    msg_box_str TEXT,  -- String "Received" or "Sent"
    date DATE,
    time TIME,
    contact_name TEXT,
    -- Others
    rr TEXT,
    sub TEXT,
    ct_t TEXT,
    read_status TEXT,
    seen TEXT,
    msg_box TEXT,
    sub_cs TEXT,
    resp_st TEXT,
    retr_st TEXT,
    d_tm TEXT,
    text_only TEXT,
    exp TEXT,
    locked TEXT,
    m_id TEXT,
    st TEXT,
    retr_txt_cs TEXT,
    retr_txt TEXT,
    creator TEXT,
    date_sent TEXT,
    read TEXT,
    m_size TEXT,
    rpt_a TEXT,
    ct_cls TEXT,
    pri TEXT,
    sub_id TEXT,
    tr_id TEXT,
    resp_txt TEXT,
    ct_l TEXT,
    m_cls TEXT,
    d_rpt TEXT,
    v TEXT,
    _id TEXT,
    m_type TEXT,
    readable_date TEXT
);

CREATE TABLE IF NOT EXISTS MmsPart (
    part_id INTEGER PRIMARY KEY,
    text TEXT,
    seq TEXT,
    ct TEXT,
    name TEXT,
    chset TEXT,
    cd TEXT,
    fn TEXT,
    cid TEXT,
    cl TEXT,
    ctt_s TEXT,
    ctt_t TEXT,
    data TEXT
);
-- Table de liaison des tables Mms et MmsPart
CREATE TABLE IF NOT EXISTS Mms_MmsPart(
    mms_id TEXT,
    part_id INTEGER,

    FOREIGN KEY (mms_id) REFERENCES Mms(mms_id),
    FOREIGN KEY (part_id) REFERENCES MmsPart(part_id)
);

CREATE TABLE IF NOT EXISTS MmsAddr (
    addr_id INTEGER PRIMARY KEY,
    address TEXT,
    type TEXT,
    charset TEXT
);
-- Table de liaison des tables Mms et MmsAddr
CREATE TABLE IF NOT EXISTS Mms_MmsAddr (
    mms_id TEXT,
    addr_id INTEGER,
    FOREIGN KEY (mms_id) REFERENCES Mms(mms_id),
    FOREIGN KEY (addr_id) REFERENCES MmsAddr(addr_id)
);

CREATE TABLE IF NOT EXISTS Mms_ContactPhoneNumber (
    mms_id INTEGER,
    phone_id INTEGER,
    FOREIGN KEY (mms_id) REFERENCES Mms (mms_id),
    FOREIGN KEY (phone_id) REFERENCES ContactPhoneNumbers (phone_id)
);

CREATE TABLE IF NOT EXISTS Tags (
    tag_id INTEGER PRIMARY KEY,
    tag TEXT
);

-- Many to many between Tags and (Emails OR Sms OR Mms)
CREATE TABLE IF NOT EXISTS MTM_Tags (
    message_id TEXT,
    sms_id TEXT,
    mms_id TEXT,
    tag_id INTEGER,
    FOREIGN KEY (message_id) REFERENCES  Emails (message_id),
    FOREIGN KEY (sms_id) REFERENCES  Sms (sms_id),
    FOREIGN KEY (mms_id) REFERENCES  Mms (mms_id),
    FOREIGN KEY (tag_id) REFERENCES Tags (tag_id)
)