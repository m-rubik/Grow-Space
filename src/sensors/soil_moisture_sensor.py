from src.utilities.sensor_template import Sensor

class SoilMoistureSensor(Sensor):

    def poll(self):
        """!
        This method is called periodically to read sensor data and report
        it back to the main thread.
        """

        # Step 1: Take a reading.
        # For testing, to simulate asynchronous I/O, we create a random number at random intervals
        import random
        import time
        rand = random.Random()
        current_time = time.time()
        self.previous_val = self.current_val
        self.current_val = round(rand.random()*100,2)

        # TODO Step 1.5: Run algorithms with the data??? 

        # Step 2: Relay the reading
        self.queue.put(self.current_val)
        
        # Step 3: Log the reading
        with open("logs/"+self.name+".txt","a+") as f:
            f.write(str(current_time)+":"+str(self.current_val)+"\n")
