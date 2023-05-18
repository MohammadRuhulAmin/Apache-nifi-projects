

CREATE TABLE pax_master (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airlines_code TEXT,
    flight_date TEXT,
    flight_code TEXT,
    pax_id TEXT,
    created_at DATETIME 
);



CREATE TABLE pax_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passport_no TEXT,
    pax_id TEXT,
    pax_name TEXT,
    ticket_no TEXT,
    created_at DATETIME
);


CREATE TABLE message_tbl (
    id INT AUTO_INCREMENT PRIMARY KEY,
    e_subject TEXT,
    e_sent_date TEXT,
    e_from TEXT,
    e_to TEXT,
    pax_id TEXT,
    msgbody TEXT,
    status INT,
    created_at DATETIME  
);