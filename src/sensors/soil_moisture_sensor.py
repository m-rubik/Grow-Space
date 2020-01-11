"""!
Code for the Soil Moisture Sensor
"""

import RPi.GPIO as GPIO
from src.utilities.sensor_template import Sensor
from datetime import datetime


class SoilMoistureSensor(Sensor):

    channel: int = None

    def __init__(self, name="default", queue=None, polling_interval=2, pin=None):
        super().__init__(name, queue, polling_interval)
        self.channel = pin # TODO: This should maybe be passed in???
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)


    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Take a reading.
        self._previous_val = self._current_val
        self._current_val = GPIO.input(self.channel)
        
        # TODO Step 1.5: Run algorithms with the data??? 

        # Step 2: Relay the reading
        self.queue.put(self._current_val)
        
        # Step 3: Log the reading
        current_time = datetime.now()
        with open("logs/"+self.name+".txt","a+") as f:
            f.write(str(current_time)+":"+str(self._current_val)+"\n")

if __name__ == "__main__":
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