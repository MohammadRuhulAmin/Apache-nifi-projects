CREATE TABLE public.pax_master (
    id SERIAL PRIMARY KEY,
    src INTEGER,
    airlines_code TEXT,
    flight_date TEXT,
    docs TEXT,
    flight_code TEXT,
    pax_id TEXT
);

CREATE TABLE public.pax_details(
	id SERIAL PRIMARY KEY,
	passport_no TEXT,
	pax_id TEXT,
	pax_name TEXT,
	is_archived TEXT,
	docs TEXT,
	ticket_no TEXT
	

)

CREATE TABLE public.message_tbl(
	e_subject TEXT,
	e_sent_date TEXT,
	e_from TEXT,
	e_to TEXT,
	pax_id TEXT,
	msgbody TEXT,
	status INTEGER
	

)