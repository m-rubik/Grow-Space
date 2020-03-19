"""!
This code is for the simulation of a BME680 Multifunction Environment Sensor.
"""

import random
from datetime import datetime
from src.utilities.sensor_template import Sensor

class EnvironmentSensor(Sensor):
    """!
    Contains the code for simulating the environment sensor.
    Since this is for a simulated sensor, there is no I2C interface,
    nor board object.
    @param data_dict: Dictionary that stores the simualted sensor readings.
    """

    data_dict: dict = {}

    def __init__(self, name="default", queue=None, polling_interval=2):
        super().__init__(name, queue, polling_interval)

    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Generate pseudorandom readings (within a range)
        self.data_dict['temperature'] = random.randrange(10, 40)    # [Celcius]
        self.data_dict['gas'] = random.randrange(100000, 900000)    # [Ohm]
        self.data_dict['humidity'] = random.randrange(0, 100)       # [%]
        self.data_dict['pressure'] = random.randrange(500, 1500)    # [hPa]
        self.data_dict['altitude'] = random.randrange(0, 2000)      # [m]
       
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
