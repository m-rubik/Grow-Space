from src.utilities.sensor_template import Sensor
from datetime import datetime

# BME680 Installation
    # Pi 3V3 (1, 17) to sensor VIN
    # Pi GND (5, 9, 25,39, 6, 14, 20, 30, 34) to sensor GND
    # Pi SCL (11(SPI0) or 21 (SPI1)) to sensor SCK
    # Pi SDA (2) to sensor SDI
    # Need to install adafruit_bme680.mpy and adafruit_bus_device


class TemperatureSensor(Sensor):

    """
    def __init__(self):
        import time, board
        from busio import I2C
        import adafruit_bme680
        # Create library object using our Bus I2C port
        i2c = I2C(board.SCL, board.SDA)
        sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
        # change this to match the location's pressure (hPa) at sea level
        bme680.sea_level_pressure = 1013.25

        # Temperature in units of Celsius
        self.temp_previous_val = sel.temp_current_val
        self.temp_current_val = sensor.temperature

        # Humidity in units of percentage
        self.humidity_previous_val = self.humidity_current_val
        self.humidity_current_val = sensor.humidity

        # Pressure readings in units of hPa
        self.pressure_previous_val = self.pressure_current_val
        self.pressure_current_val = sensor.pressure

        # Gas in units of Ohms. Proportional to amount of VOC particles in air
        self.gas_previous_val = self.gas_current_val
        self.gas_current_val = sensor.gas
        pass
    """
    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Take a reading.
        # For testing, to simulate asynchronous I/O, we create a random number at random intervals
        import random
        import time
        current_time = datetime.now()
        self._previous_val = self._current_val
        self._current_val = random.randrange(10, 40)

        # TODO Step 1.5: Run algorithms with the data??? 

        # Step 2: Relay the reading
        self.queue.put(self._current_val)
        
        # Step 3: Log the reading
        with open("logs/"+self.name+".txt","a+") as f:
            f.write(str(current_time)+":"+str(self._current_val)+"\n")
