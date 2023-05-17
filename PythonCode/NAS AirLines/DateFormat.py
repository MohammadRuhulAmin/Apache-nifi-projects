from org.apache.nifi.processors.script import ExecuteScript
from datetime import datetime

def convertDate(dateString):
    dateObj = datetime.strptime(dateString, "%d-%b-%y")
    year = str(dateObj.year)
    month = str(dateObj.month)
    day = str(dateObj.day)
    if int(month)<10 :
        return year + "-" +"0"+str(month)+ "-" + day 
    else:
        return year + "-" + month + "-" + day

flowFile = session.get()
if flowFile is not None:
    dateString = flowFile.getAttribute('Flight_Date')
    convertedDate = convertDate(dateString)
    flowFile = session.putAttribute(flowFile, 'Formated_Flight_Date', convertedDate)
    session.transfer(flowFile, ExecuteScript.REL_SUCCESS)
