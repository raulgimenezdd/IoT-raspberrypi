import threading

import Adafruit_DHT
from publisher import *
import uuid
from rpi_lcd import LCD
import RPi.GPIO as GPIO
import time
from gps3 import gps3
from threading import Lock
from signal import signal,SIGTERM, SIGHUP, pause

lcd = LCD()
pressed = False
temperature = 0.0
humidity = 0.0
mutex = Lock()

def button_pressed_callback(channel):
    global pressed
    pressed = not pressed

def safe_exit(signum, frame):
    exit(1)

def deviceGPSSensor():

    socket = gps3.GPSDSocket()
    data = gps3.DataStream()
    socket.connect()
    socket.watch()

    print(socket)
    for new_data in socket:
        if new_data:
            data.unpack(new_data)

            latitude = data.TPV['lat']
            longitud = data.TPV['lon']
            print(latitude)
            print(longitud)
            if latitude != 'n/a' and longitud != 'n/a':
                return str(latitude) + ", " + str(longitud)




def temperatureSensor():
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    newtemperature = 0
    global pressed
    while True:
        temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)[1]
        if temperature is not None:
            if(newtemperature != temperature):
                newtemperature = temperature
                send_temperature(temperature)
                send_timestamp()
                print(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
            print("Temp={0:0.1f}C".format(temperature))
            if pressed:
                mutex.acquire()
                lcd.text('Temp: ' + str(temperature), 1)
                time.sleep(0.5)
                mutex.release()
        else:
            print("sensor failure. check wiring")
            if pressed:
                mutex.acquire()
                lcd.text('Sensor failure', 1)
                time.sleep(0.5)
                mutex.release()


def humiditySensor():
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    newhumidity = 0
    global pressed
    while True:
        humidity = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)[0]
        if humidity is not None:
            if(newhumidity != humidity):
                newhumidity = humidity
                send_humidity(humidity)
            print("Hum={0:0.1f}%".format(humidity))
            if not pressed:
                mutex.acquire()
                lcd.text('Hum: ' + str(humidity), 1)
                time.sleep(0.5)
                mutex.release()

        else:
            print("sensor failure. check wiring")
            if not pressed:
                mutex.acquire()
                lcd.text('Sensor failure', 1)
                time.sleep(0.5)
                mutex.release()


def timeStampChanges():
    newTimeStamp = time.strftime("%M", time.localtime())
    while True:
        actual_time = time.strftime("%M", time.localtime())
        if actual_time != newTimeStamp:
            newTimeStamp = actual_time
            send_timestamp()
            print(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))

def sensor_on():
    make_connection()
    id = ':'.join(['{:02x}' .format((uuid.getnode() >> ele) & 0xff)
                   for ele in range(0,8*6,8)][::-1])
    print(id)
    #send_state("Active")
    location = deviceGPSSensor()
    send_location(location)
    send_id(str(id) + " Active")

def safe_exit(singum, frame):
    exit(1)


signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)


if __name__ == "__main__":
    sensor_on()

    BUTTON_GPIO = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)


    temperature_thread = threading.Thread(target=temperatureSensor)
    humidity_thread = threading.Thread(target=humiditySensor)
    timestamp_thread = threading.Thread(target=timeStampChanges)

    temperature_thread.start()
    humidity_thread.start()
    timestamp_thread.start()




