import time
import paho.mqtt.client as paho
from measurement_register_interface import *
from device_register_interface import *
import os

# global vars definition
current_temperature = 0
current_humidity = 0
current_timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
device_state = ""
device_location = ""
actual_time = ""
device = ""

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
        client.subscribe("/uc3m/classrooms/leganes/gr83/temperature")
        client.subscribe("/uc3m/classrooms/leganes/gr83/humidity")
        client.subscribe("/uc3m/classrooms/leganes/gr83/device_info")
        client.subscribe("/uc3m/classrooms/leganes/gr83/timestamp")
        client.subscribe("/uc3m/classrooms/leganes/gr83/device_state")
        client.subscribe("/uc3m/classrooms/leganes/gr83/location")

    else:
        print("Connected fail with code", {rc})


# define mqtt callback
def on_message(client, userdata, message):
    global current_temperature, current_humidity, current_timestamp, device, device_location, actual_time
    print("received message =",str(message.payload.decode("utf-8")))
    if message.topic == "/uc3m/classrooms/leganes/gr83/temperature":
        current_temperature = float(message.payload.decode("utf-8"))
        data = {"device_id": device, "temperature": current_temperature, "humidity": current_humidity, "measure_time": current_timestamp}
        submit_data_to_store(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/gr83/humidity":
        current_humidity = float(message.payload.decode("utf-8"))
        data = {"device_id": device, "temperature": current_temperature, "humidity": current_humidity, "measure_time": current_timestamp}
        submit_data_to_store(data)
        print(data)

    if message.topic == "/uc3m/classrooms/leganes/gr83/timestamp":
        current_timestamp = message.payload.decode("utf-8")
        data = {"device_id": device, "temperature": current_temperature, "humidity": current_humidity, "measure_time": current_timestamp}
        submit_data_to_store(data)
        print(data)

    #if message.topic == "/uc3m/classrooms/leganes/gr83/device_state":
    #    device_state = message.payload.decode("utf-8")

    if message.topic == "/uc3m/classrooms/leganes/gr83/location":
        device_location = message.payload.decode("utf-8")

    if message.topic == "/uc3m/classrooms/leganes/gr83/device_info":
        r = message.payload.decode("utf-8")
        device = r.split(" ")[0]
        device_state = r.split(" ")[1]
        if device_state == "Active":
            actual_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        data = {"device_id": device, "status": device_state, "location": device_location, "register_time": actual_time}
        submit_device_info_to_store(data)
        print(data)

# Create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
host= os.getenv("BROKER_ADDRESS")
port= int(os.getenv("BROKER_PORT"))
user= os.getenv("BROKER_USER")
psw= os.getenv("BROKER_PWD")
keepalive= int(os.getenv("BROKER_KEEP_ALIVE"))
client=paho.Client()
client.username_pw_set(username=user, password=psw)
client.on_connect = on_connect
# Bind function to callback
client.on_message=on_message
# Initializate cursor instance
print("connecting to broker ",host)
client.connect(host, port, keepalive) # connect
# Start loop to process received messages
client.loop_forever()
