# Soil Moisture Sensors

import RPi.GPIO as GPIO
import time
import datetime

channel = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    time = datetime.datetime.now()
    reading = GPIO.input(channel)
    if reading == 1:
        print(time, "Reading is", str(reading)+". No water")
    else:
        print(time, "Reading is", str(reading)+". Water detected")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

while True:
    time.sleep(0.1)