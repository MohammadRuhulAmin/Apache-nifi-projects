CREATE TABLE pax_master (
    id SERIAL PRIMARY KEY,
    src INTEGER,
    airlines_code TEXT,
    flight_date TEXT,
    docs TEXT,
    flight_code TEXT,
    "email.headers.message-id" TEXT
);

CREATE TABLE pax_details{
	id SERIAL PRIMARY KEY,
	passport_no TEXT,
	pax_master_id TEXT,
	pax_name TEXT,
	is_archived TEXT,
	docs TEXT,
	ticket_no TEXT
	

}

CREATE TABLE message_tbl{
	"email.headers.subject" TEXT,
	"email.headers.sent_date" TEXT,
	"email.headers.from.0" TEXT,
	"email.headers.to.0" TEXT,
	"email.headers.message-id" TEXT,
	msgbody TEXT,
	status INTEGER
	

}