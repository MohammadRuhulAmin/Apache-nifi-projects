import re
import json
import uuid
import email
import mimetypes
from email.parser import Parser
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from java.io import BufferedReader, InputStreamReader
from org.apache.nifi.processors.script import ExecuteScript
from org.apache.nifi.processor.io import InputStreamCallback
from org.apache.nifi.processor.io import StreamCallback
from org.apache.nifi.processor.io import OutputStreamCallback
from datetime import datetime


class PyInputStreamCallback(InputStreamCallback):
    _text = None

    def __init__(self):
        pass

    def getText(self):
        return self._text

    def process(self, inputStream):
        self._text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)


flowFile = session.get()


class PyOutputStreamCallback(OutputStreamCallback):
    def __init__(self, data):
        self.data = data

    def process(self, outputStream):
        outputStream.write(bytearray(self.data.encode('utf-8')))


def date_timeFormatDate(Date):
    month_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07',
                  'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
    m_date = re.findall(r'([A-Z]+)', Date)[0]
    return datetime.now().strftime("%Y") + "-" + month_dict.get(m_date, m_date) + "-" + re.findall(r'([0-9]+)', Date)[0]


def process_data(email):
    pregex = r'([A-Z]+\s[A-Z]+\s([A-Z]+\s)?([A-Z]+\s+)?\s+[A-Z]+\s+[A-Z]\s+[A-Z0-9]+)'
    matches = re.findall(pregex, email)
    pax_master = {
        "pax_id": flowFile.getAttribute('email.headers.message-id'),
        "airlines_code": "",
        "flight_code": re.findall(r'SV\d+', email)[0],
        "flight_date": date_timeFormatDate(re.findall(r'\d{1,2}[A-Z]{3}', email)[0]),
        "docs": ""
    }

    parsed_data = []
    for x in matches:
        replacedData = x[0].replace(" ", "|")
        pax_name = replacedData.split("|")[1] + " " + replacedData.split("|")[2] + " " + replacedData.split("|")[0]
        passport = replacedData.split("|")[-1]
        if bool(passport):
            pax_details = {
                "pax_id": flowFile.getAttribute('email.headers.message-id'),
                "pax_name": pax_name,
                "passport_no": passport,
                "ticket_no": "",
            }

            parsed_data.append(pax_details)

            full_data = {
                "pax_master": [pax_master],
                "pax_details": parsed_data

            }

    return (json.dumps(full_data))


if flowFile is not None:
    reader = PyInputStreamCallback()
    session.read(flowFile, reader)
    msg = email.message_from_string(reader.getText())
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=False)  # decode
                output = process_data(body)

                break
    else:
        body = msg.get_payload(decode=True)

    # flowFile = session.putAttribute(flowFile, 'msgbody', output.decode('utf-8', 'ignore')) #
    write_cb = PyOutputStreamCallback(output)
    flowFile = session.write(flowFile, write_cb)

    session.transfer(flowFile, ExecuteScript.REL_SUCCESS)  # your code goes here