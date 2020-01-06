from src.utilities.sensor_template import Sensor
from datetime import datetime

class TemperatureSensor(Sensor):

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
