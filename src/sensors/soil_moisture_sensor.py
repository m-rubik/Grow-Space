"""!
Code for the Soil Moisture Sensor
"""

import time
import board
from busio import I2C
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn 
from src.utilities.sensor_template import Sensor
from datetime import datetime


class SoilMoistureSensor(Sensor):

    i2c_interface = None
    ads = None
    sensor_board = None
    channel = None 

    def __init__(self, name="default", queue=None, polling_interval=2, channel=None, max_v=3, min_v=1):
        super().__init__(name, queue, polling_interval)

        self.i2c_interface = I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c_interface)
        self.max_v = max_v
        self.min_v = min_v
        self.voltage_list = []

        if channel == 0:
            self.channel = AnalogIn(self.ads, ADS.P0)
        elif channel == 1:
            self.channel = AnalogIn(self.ads, ADS.P1)
        elif channel == 2:
            self.channel = AnalogIn(self.ads, ADS.P2)
        elif channel == 3:
            self.channel = AnalogIn(self.ads, ADS.P3)

        self.voltage_list = []
        current_time = datetime.now()
        # sets max voltage from average of 5 readings from sensor
        #for _ in range(5):
            #self.voltage_list.append(self.channel.voltage)
            #time.sleep(1)
        # Initializes max voltage of the sensor
        #self.max_volt = sum(self.voltage_list)/len(self.voltage_list)
        self.max_volt = 3.292
        self.min_volt = 1.30

    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Take a reading and normalize voltage value
        self._previous_val = self._current_val
        self._current_val = [self.channel.value, self.channel.voltage, 3]
        
        # TODO Step 1.5: Run algorithms with the data??? 

        # Step 2: Relay the reading
        self._current_val[2]= (-100/(self.max_volt-self.min_volt))* (self._current_val[1]-self.max_volt)
        if self._current_val[2] > 99.7:
            self._current_val[2] = 100.00
        elif self._current_val[2]< 0.3:
            self._current_val[2] = 0.00
            
        self.queue.put(round(self._current_val[2],2)) # This is passing the raw value to the queue?

        # Step 3: Log the reading
        current_time = datetime.now()
        with open(self.log_file_name,"w+", "a+") as f:
            f.write(str(current_time)+": "+str(self._current_val)+"\n")

    def shutdown(self):
        print(self.name, "shutting down.")

if __name__ == "__main__":

    import time
    import board
    from busio import I2C
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn 

    # Create library object using our Bus I2C port
    i2c = I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P0)
    print("{:>5}\t{:>5}".format('raw', 'v'))

    while True:
        print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
        time.sleep(0.5)

    # CODE FOR DIGITAL SIGNAL ONLY
    # import RPi.GPIO as GPIO
    # import time
    # import datetime
    # channel = 16
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(channel, GPIO.IN)
    # def callback(channel):
    #     time = datetime.datetime.now()
    #     reading = GPIO.input(channel)
    #     if reading == 1:
    #         print(time, "Reading is", str(reading)+". No water")
    #     else:
    #         print(time, "Reading is", str(reading)+". Water detected")
    # GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
    # GPIO.add_event_callback(channel, callback)
    # while True:
    #     time.sleep(0.1)