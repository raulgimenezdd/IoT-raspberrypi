import uuid
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connection success")
    else:
        print("connection fail with code:", {rc})

client = mqtt.Client()
def make_connection():
    client.username_pw_set(username="dso_server", password="mqtt1234")
    client.on_connect = on_connect
    id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                   for ele in range(0, 8 * 6, 8)][::-1])
    client.will_set('/uc3m/classrooms/leganes/gr83/device_info', str(id) + " Inactive")

    client.connect("35.246.205.15", 1883, 60)


def send_temperature(temperature):
    client.publish('/uc3m/classrooms/leganes/gr83/temperature', payload=temperature, qos=0, retain=False)
    time.sleep(1)

def send_humidity(humidity):
    client.publish('/uc3m/classrooms/leganes/gr83/humidity', payload=humidity, qos=0, retain=False)
    time.sleep(1)

def send_id(id):
    client.publish('/uc3m/classrooms/leganes/gr83/device_info', payload=id, qos=0, retain=False)
    time.sleep(1)

def send_timestamp():
    actual_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    client.publish('/uc3m/classrooms/leganes/gr83/timestamp', payload=actual_time, qos=0, retain=False)
    time.sleep(1)

def send_state(status):
    client.publish('/uc3m/classrooms/leganes/gr83/device_state', payload=status, qos=0, retain=False)
    time.sleep(1)

def send_location(location):
    client.publish('/uc3m/classrooms/leganes/gr83/location', payload=location, qos=0, retain=False)
    time.sleep(1)
