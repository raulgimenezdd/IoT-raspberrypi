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

def measurements_retriever():
    mydb = connect_database()
    r = []
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT temperature, humidity, measure_time FROM sensor_data ORDER BY measure_time DESC;")
        myresult = mycursor.fetchall()
        for temperature, humidity, measure_time in myresult:
            r.append({"temperature": temperature, "humidity": humidity, "measure_time": measure_time})
        mydb.commit()
    result = json.dumps(r, sort_keys=True)
    return result

def measurements_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO sensor_data (temperature, humidity, measure_time) VALUES (%s, %s, %s)"
        val = (params["temperature"], params["humidity"], params["measure_time"])
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
