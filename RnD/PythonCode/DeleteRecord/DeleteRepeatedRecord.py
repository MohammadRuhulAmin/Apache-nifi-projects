import mysql.connector
import time

pax_idList = []

def dbExecuteQuery():
    mydb = mysql.connector.connect(
        host="175.29.186.209",
        port=33306,
        user="ruhul",
        password="R43sfg%liPaw",
        database="PNL_Data"
    )


    queryflightInfo ="""
    SELECT flight_code,flight_date,COUNT(*) from PNL_Data.pax_master
    GROUP By flight_code,flight_date HAVING COUNT(*)>1
    """

    flightInfoCur = mydb.cursor()
    flightInfoCur.execute(queryflightInfo)
    flight_rows = flightInfoCur.fetchall()


    flightCodeList = []

    for x in flight_rows:
        if x[0] !='':
            flightCodeList.append(x[0])

    for i in flightCodeList:
        flightInfoCur.execute("SELECT created_at,pax_id from PNL_Data.pax_master where flight_code = %s order by created_at asc",(i,))
        flight_row = flightInfoCur.fetchall()
        for i in range(len(flight_row)-1):
            pax_idList.append(flight_row[i][1])

    for i in pax_idList:
        flightInfoCur.execute("DELETE FROM PNL_Data.pax_master WHERE pax_id = %s", (i,))
        mydb.commit()
        flightInfoCur.execute("DELETE FROM PNL_Data.pax_details WHERE pax_id = %s",(i,))
        mydb.commit()
        flightInfoCur.execute("DELETE FROM PNL_Data.message_tbl WHERE pax_id = %s",(i,))
        mydb.commit()
    if flightInfoCur.rowcount > 0:
        print("Repeated Data Found and Deleted the previous Record! ")
    else:
        print("No Repeated Data Found !  ", )


while True:
    dbExecuteQuery()
    time.sleep(10)







