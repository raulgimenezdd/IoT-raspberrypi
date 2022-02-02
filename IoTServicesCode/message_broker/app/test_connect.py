import paho.mqtt.client as mqtt


def on_connect(clients, userdata, flags, rc):
    if rc == 0:
        print("Conection success")
    else:
        print("Conection failed with code", {rc})

client = mqtt.Client()
client.username_pw_set(username="dso_server", password="mqtt1234")
client.on_connect = on_connect
client.connect("35.246.205.15", 1883, 68)
client.loop_forever()