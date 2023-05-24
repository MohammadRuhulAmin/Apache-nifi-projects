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
 
    def getText(self) : 
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
    month_dict = {'JAN': '01','FEB': '02','MAR': '03','APR': '04','MAY': '05','JUN': '06','JUL': '07','AUG': '08','SEP':'09','OCT': '10','NOV': '11','DEC': '12'}
    m_date = re.findall(r'([A-Z]+)', Date)[0]
    return datetime.datetime.now().strftime("%Y") + "-"+ month_dict.get(m_date,m_date) + "-" + re.findall(r'([0-9]+)',Date)[0]



def process_data(email):
    pregex = r'(\d*\.)(.*\/\w*)(.*)(\d{13})(\s*AS\s+)(CPN SERIAL NUM \d{2,}\s*)(UI-[A-Z0-9]{0,}\s+)([A-z]{3}\s*\w+)?'

    data = re.sub(r'=C2=A5','',email,flags=re.MULTILINE)
    data = re.sub(r'=20','',data,flags=re.MULTILINE)
    data = re.sub(r'=','',data,flags=re.MULTILINE)
    uniqueId = str(uuid.uuid4())
    matches = re.findall(pregex, data)
    # print(matches)

    pax_master = {
        "pax_id":flowFile.getAttribute('email.headers.message-id'),
        "airlines_code": "" ,
        "src": 0,
        "receieved_at":1111,
        "flight_code":re.search(r'[S][V]\d+', email).group(),
        "flight_date": date_timeFormatDate(re.search(r'\d{1,2}[A-Z]{3}',email).group()),
        "docs": ""
        }  

    parsed_data = []
    for i in matches:
        passport = i[7].split()
        if bool(passport):
            pax_details = {
                    "pax_id":flowFile.getAttribute('email.headers.message-id'),
                    "pax_name": i[1].replace("/"," "),
                    "passport_no": passport[1],
                    "ticket_no": i[3], 
                    "is_archived": 0,
                    "docs": ""
                }
            
            parsed_data.append(pax_details)

            full_data = {
                "pax_master" : [pax_master],
                "pax_details" : parsed_data

            }

    return(json.dumps(full_data))
        


if flowFile is not None :
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
    
       
    session.transfer(flowFile, ExecuteScript.REL_SUCCESS)# your code goes here