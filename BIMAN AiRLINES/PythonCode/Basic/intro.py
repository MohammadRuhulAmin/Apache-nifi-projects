

from org.apache.nifi.processors.script import ExecuteScript
from datetime import datetime

def convertDate(dateString):
    dateObj = datetime.strptime(dateString, "%d-%b-%y")
    year = str(dateObj.year)
    month = str(dateObj.month)
    day = str(dateObj.day)
    return  (year + "-" + month+"-"+ day)

flowFile = session.get()
if flowFile is not None:
	
    flowFile = session.putAttribute(flowFile, 'msgbody', "mm")
    session.transfer(flowFile, ExecuteScript.REL_SUCCESS)