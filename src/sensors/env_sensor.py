"""!
This code is for the intialization and communicaiton of a BME680 Multifunction Environment Sensor.
"""

import time
import board
from datetime import datetime
from busio import I2C
import adafruit_bme680
from src.utilities.sensor_template import Sensor


class EnvironmentSensor(Sensor):
    """!
    The environment sensor measures:
    1. Temperature
    2. Volatile Organic Compounds (VOC/gas)
    3. Humidity
    4. Pressure
    5. Altitude
    @param i2c_interface: The sensor communicates to the RPi via I2C. This is the interface.
    @param sensor_board: This is the "board" object of the sensor board.
    @param data_dict: This is the dictionary containing all the sensor readings.
    """

    i2c_interface = None
    sensor_board = None
    data_dict: dict = {}

    def __init__(self, name="default", queue=None, polling_interval=2, sea_level_pressure=1013.25):
        super().__init__(name, queue, polling_interval)

        # Create I2C interface library object
        self.i2c = I2C(board.SCL, board.SDA)
        # Create our sensor board object
        self.sensor_board = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, debug=False)
        # change this to match the location's pressure (hPa) at sea level
        self.sensor_board.sea_level_pressure = sea_level_pressure

    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Take the readings
        try:
            self.data_dict['temperature'] = self.sensor_board.temperature   # [Celcius]
            self.data_dict['gas'] = self.sensor_board.gas                   # [Ohm]
            self.data_dict['humidity'] = self.sensor_board.humidity         # [%]
            self.data_dict['pressure'] = self.sensor_board.pressure         # [hPa]
            self.data_dict['altitude'] = self.sensor_board.altitude         # [m]
        except Exception as err:
            print(err)

        # Step 2: Relay the readings
        self.queue.put(self.data_dict)

        # Step 3: Log the reading
        current_time = datetime.now()
        with open(self.log_file_name,"a+") as f:
            f.write(str(current_time)+": ")
            for entry, value in self.data_dict.items():
                f.write(entry + ": " + str(value) + ", ")
            f.write("\n")

    def shutdown(self):
        """!
        Shutdown event bound to the atexit condition.
        Currently does not have any special functionality.
        """
        print(self.name, "shutting down.")

def unit_test():
    """
    Code from:
    https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/python-circuitpython

    remember to install both the adafruit_blinka and adafruit-circuitpython-bme680 libraries
    """
    i2c = I2C(board.SCL, board.SDA)
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
    bme680.sea_level_pressure = 1013.25
    
    while True:
        print("\nTemperature: %0.1f C" % bme680.temperature)
        print("Gas: %d ohm" % bme680.gas)
        print("Humidity: %0.1f %%" % bme680.humidity)
        print("Pressure: %0.3f hPa" % bme680.pressure)
        print("Altitude = %0.2f meters" % bme680.altitude)
        time.sleep(1)


if __name__ == "__main__":
    unit_test()