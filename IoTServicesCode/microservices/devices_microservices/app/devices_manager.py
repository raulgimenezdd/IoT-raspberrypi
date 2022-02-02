import mysql.connector
import json
import os

def connect_database ():

    mydb = mysql.connector.connect(
        host=os.getenv('DBHOST'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASSWORD'),
        database=os.getenv('DBDATABASE')
    )
    return mydb

def devices_retriever():
    mydb = connect_database()
    r = []
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT device_id, status, location, register_time FROM devices ORDER BY id DESC LIMIT 1;")
        myresult = mycursor.fetchall()
        for device_id, status, location, register_time in myresult:
            r.append({"device_id": device_id, "status": status, "location": location, "register_time": register_time})
        mydb.commit()
    result = json.dumps(r, sort_keys=True)
    return result

def devices_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "REPLACE INTO devices (device_id, status, location, register_time) VALUES (%s, %s, %s, %s)"
        val = (params["device_id"], params["status"], params["location"], params["register_time"])
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except:
            print("Error inserting the device")
