import re
import json
import uuid
import email
import mimetypes
import datetime
from email.parser import Parser
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from java.io import BufferedReader, InputStreamReader
from org.apache.nifi.processors.script import ExecuteScript
from org.apache.nifi.processor.io import InputStreamCallback
from org.apache.nifi.processor.io import StreamCallback
from org.apache.nifi.processor.io import OutputStreamCallback




class PyInputStreamCallback(InputStreamCallback):
    _text = None

    def __init__(self):
        pass

    def getText(self) :
        return self._text

    def process(self, inputStream):
        self._text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)

flowFile = session.get()
if flowFile is not None:
	allAttributes = flowFile.getAttributes()
	emailId = allAttributes.get('email.headers.message-id')
	uid = emailId

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
    pregex = r'^P\/([A-Z0-9]{1,3})\/([A-Z0-9]+)\/([A-Z]{2,3})\/(\d{2,4}[A-Z]{3}\d{2,4})\/([MF])\/(\d{2,4}[A-Z]{3}\d{2,4})\/([A-Z]+)'


    data = re.sub(r'^\s+', '', email, flags=re.MULTILINE)
    data = re.sub(r'=C2=A5','',data,flags=re.MULTILINE)
    data = re.sub(r'=20','',data,flags=re.MULTILINE)
    data = data.split('\n')
    data = [re.sub(r'\s+', ' ', line).strip() for line in data]
    header = data[:2]


    pax_master= {}
    pax_master = {
        "pax_id":flowFile.getAttribute('email.headers.message-id'),
        "airlines_code": header[1].split(" ")[0] ,
        "src":0,
        "receieved_at":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "flight_code":str(header[1].split(" ")[0])+str(header[1].split(" ")[1]),
        "flight_date": date_timeFormatDate(header[1].split(" ")[2]),
        "docs": ' '.join(header)
        }

    email_gist = '\n'.join(data[2:])

    cleaned_email_gist = email_gist.split('LFTD')
    # return email_gist

    parsed_data = []

    for i in cleaned_email_gist:
        val = i.split('\n')
        for items in val:
            # print(items)
            if re.match(pregex,items):
                p_info = items

                try:
                    pax_details = {
						"passport_no": p_info.split('/')[2],
                        "pax_id": flowFile.getAttribute('email.headers.message-id'),
                        "pax_name": p_info.split('/')[7]+"/"+p_info.split('/')[8],
                        "is_archived": 0,
                        "docs": re.sub("\n"," ", i)+"LFTD",
						"ticket_no": i.split("\n")[-1].split(" ")[-6] if len(i.split("\n")) >= 1 and len(i.split("\n")[-1].split(" ")) >= 6 else None,
                    }
                   #pax_details = {

                    #    "pax_master_id": flowFile.getAttribute('email.headers.message-id'),
                    #    "pax_name": p_info.split('/')[7]+"/"+p_info.split('/')[8],
                    #    "passport_no": p_info.split('/')[2],
                    #    "ticket_no": i.split("\n")[-1].split(" ")[-6],
                    #    "is_archived": 0,
                    #    "docs": re.sub("\n"," ", i)+"LFTD"
                    #}

                except IndexError:

                    pax_details = {
						"passport_no": p_info.split('/')[2],
                        "pax_id": flowFile.getAttribute('email.headers.message-id'),
                        "pax_name": p_info.split('/')[7]+"/"+p_info.split('/')[8],
                        "is_archived": 0,
                        "docs": re.sub("\n"," ", i),
						"ticket_no": "Ticket Number Not Found"
                    }




                parsed_data.append(pax_details)
            else:
                pass


    main_data ={
        "pax_master": [pax_master],
        "pax_details": parsed_data
    }



    return json.dumps(main_data)


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
    # added this two lines
    write_cb = PyOutputStreamCallback(output)
    flowFile = session.write(flowFile, write_cb)


    session.transfer(flowFile, ExecuteScript.REL_SUCCESS)# your code goes here