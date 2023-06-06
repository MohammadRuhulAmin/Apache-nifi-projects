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
    SELECT passport_no,Count(passport_no) FROM PNL_Data.pax_details
    GROUP BY passport_no HAVING Count(passport_no)>1 limit 100
    """

    flightInfoCur = mydb.cursor()
    flightInfoCur.execute(queryflightInfo)
    passport_rows = flightInfoCur.fetchall()
    repeated_passport = []
    for x in range (0,len(passport_rows)):
        repeated_passport.append(passport_rows[x][0])
    operation_list = []


    for x in repeated_passport:
        flightInfoCur.execute("SELECT id,passport_no,created_at FROM PNL_Data.pax_details WHERE passport_no = %s Order by id asc",(x,))
        passport_data = flightInfoCur.fetchall()
        operation_list.append(passport_data)
        mydb.commit()

    for olist in operation_list:
        for x in range(0,len(olist)-1):
            flightInfoCur.execute("DELETE FROM PNL_Data.pax_details WHERE id = %s AND passport_no = %s ",(olist[x][0],olist[x][1],))
            mydb.commit()

    if flightInfoCur.rowcount > 0:
        print("Repeated Data has been deleted Successfully!")
        print("The passport list are : " , operation_list)
    else:
        print("No Repeated Data Found!")

iterator = 1
while True:
    print("Counter : ",iterator)
    dbExecuteQuery()
    time.sleep(3)
    iterator+=1








