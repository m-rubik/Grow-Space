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
import RPi.GPIO as GPIO


class SoilMoistureSensor(Sensor):

    i2c_interface = None
    ads = None
    sensor_board = None
    channel = None 

    def __init__(self, name="default", queue=None, polling_interval=2, channel=None, max_v=3.0, min_v=0.8):
        super().__init__(name, queue, polling_interval)

        self.i2c_interface = I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c_interface)
        self.max_volt = max_v
        self.min_volt = min_v
        self.voltage_list = []

        self.pin = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.is_off = True 
        GPIO.output(self.pin, self.is_off)

        if channel == 0:
            self.channel = AnalogIn(self.ads, ADS.P0)
        elif channel == 1:
            self.channel = AnalogIn(self.ads, ADS.P1)
        elif channel == 2:
            self.channel = AnalogIn(self.ads, ADS.P2)
        elif channel == 3:
            self.channel = AnalogIn(self.ads, ADS.P3)

    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Take a reading and normalize voltage value
        self._previous_val = self._current_val
        self.turn_off() # Inverted logic???
        time.sleep(0.2)
        self._current_val = [self.channel.value, self.channel.voltage, 0]
        print("==================================", self._current_val)
        time.sleep(0.1)
        self.turn_on()

        # Step 2: Relay the reading
        self._current_val[2] = (-100/(self.max_volt-self.min_volt))*(self._current_val[1]-self.max_volt)
        if self._current_val[2] > 99.7:
            self._current_val[2] = 100.00
        elif self._current_val[2] < 0.3:
            self._current_val[2] = 0.00
            
        self.queue.put(round(self._current_val[2], 2))

        # Step 3: Log the reading
        current_time = datetime.now()
        with open(self.log_file_name, "a+") as f:
            f.write(str(current_time)+": "+str(self._current_val)+"\n")

    def toggle(self):
        if self.is_off:
            self.turn_on()
            self.is_off = False
        else:
            self.turn_off()

    def turn_on(self):
        self.is_off = False
        GPIO.output(self.pin, self.is_off)
        print("Turning on", self.name)

    def turn_off(self):
        self.is_off = True
        GPIO.output(self.pin, self.is_off)
        print("Turning off", self.name)

    def shutdown(self):
        """!
        Shutdown event bound to the atexit condition.
        Currently does not have any special functionality.
        """
        print(self.name, "shutting down.")
        self.turn_on()

def unit_test():
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


if __name__ == "__main__":
    unit_test()