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
    SELECT passport_no,Count(*) FROM PNL_Data.pax_details
    GROUP BY passport_no HAVING Count(*)>1
    """

    flightInfoCur = mydb.cursor()
    flightInfoCur.execute(queryflightInfo)
    passport_rows = flightInfoCur.fetchall()
    # print(passport_rows)
    repeated_passport = []

    for x in range (0,len(passport_rows)):
        if bool(passport_rows[x][0]):
            repeated_passport.append(passport_rows[x][0])

    operation_list = []


    for x in repeated_passport:
        flightInfoCur.execute("SELECT passport_no,created_at FROM PNL_Data.pax_details WHERE passport_no = %s Order by created_at asc",(x,))
        passport_data = flightInfoCur.fetchall()
        operation_list.append(passport_data)


    for olist in operation_list:
        for x in range(0,len(olist)-1):
            flightInfoCur.execute("DELETE FROM PNL_Data.pax_details WHERE passport_no = %s AND created_at = %s",(olist[x][0],olist[x][1]))
            mydb.commit()

    if flightInfoCur.rowcount > 0:
        print("Repeated Data has been deleted Successfully!")
    else:
        print("No Repeated Data Found!")

while True:
    dbExecuteQuery()
    time.sleep(10)








