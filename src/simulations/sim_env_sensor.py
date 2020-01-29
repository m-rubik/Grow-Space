"""!
This code is for the simulation of a BME680 Multifunction Environment Sensor.
"""

import random
from datetime import datetime
from src.utilities.sensor_template import Sensor

class EnvironmentSensor(Sensor):

    data_dict: dict = {}

    def __init__(self, name="default", queue=None, polling_interval=2):
        super().__init__(name, queue, polling_interval)

    def poll(self):

        # Step 1: Generate random readings
        self.data_dict['temperature'] = random.randrange(10, 40)    # [Celcius]
        self.data_dict['gas'] = random.randrange(100000, 900000)    # [Ohm]
        self.data_dict['humidity'] = random.randrange(0, 100)       # [%]
        self.data_dict['pressure'] = random.randrange(500, 1500)    # [hPa]
        self.data_dict['altitude'] = random.randrange(0, 2000)      # [m]
       
        # print("\nTemperature: %0.1f C" % self.data_dict['temperature'])
        # print("Gas: %d ohm" % self.data_dict['gas'])
        # print("Humidity: %0.1f %%" % self.data_dict['humidity'])
        # print("Pressure: %0.3f hPa" % self.data_dict['pressure'])
        # print("Altitude = %0.2f meters" % self.data_dict['altitude'])

        # TODO Step 1.5: Run algorithms with the data??? 

        # Step 2: Relay the readings
        self.queue.put(self.data_dict)

        # Step 3: Log the reading
        current_time = datetime.now()
        with open("logs/"+self.name+".txt","a+") as f:
            f.write(str(current_time)+": ")
            for entry, value in self.data_dict.items():
                f.write(entry + ": " + str(value) + ", ")
            f.write("\n")

    def shutdown(self):
        print(self.name, "shutting down.")
