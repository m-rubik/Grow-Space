"""!
This is the main thread from which the program is started/runs.
This thread will periodically call the sensor worker processes to 
poll for their data. This data is returned here, so it can be analysed
and control signals can be generated.
"""

import sys
import time
import os
from tkinter import Tk
from multiprocessing import Queue, Process
from src.GUI.GUI import GrowSpaceGUI
from src.utilities.sensor_template import Sensor
from src.sensors.temperature_sensor import TemperatureSensor

class ThreadedClient:
    """!
    This is the main thread class.
    In the future, when more boxes are implemented, there would be multiple
    instances of this class used, where each instance is for 1 box.
    @param gui: This is the main GUI
    @param master_queue: Queue between this thread and the GUI
    @param sensors: A dictionary mapping all Sensor class instances to a unique name. These are the sensors of the system.
    @param sensor_processes: A dictionary mapping all Sensor worker processes to a unique name. These are the sensor processes of the system.
    """

    gui: GrowSpaceGUI = None
    master_queue: Queue = Queue()
    sensors: dict = dict()
    sensor_processes: dict = dict()

    def __init__(self, master):
        """!
        Launches the GUI and the asynchronous worker processes (1 for each sensor).
        @param master: The root (instance) of a Tkinter top-level widget
        """

        self.gui = GrowSpaceGUI(master, self.master_queue, self.end_application)
        
        self.sensors['soil_moisture_sensor_1'] = Sensor(name="soil_moisture_sensor_1", queue=Queue())
        self.sensors['temperature_sensor'] = TemperatureSensor(name="temperature_sensor", queue=Queue())
        self.sensor_processes['soil_moisture_sensor_1'] = Process(target=self.sensors['soil_moisture_sensor_1'].run)
        self.sensor_processes['temperature_sensor'] = Process(target=self.sensors['temperature_sensor'].run)

        print(self.sensor_processes['temperature_sensor'])
        
        for sensor in self.sensor_processes.values():
            sensor.start()

        self.main_running = True

        # Ensure that there is a directory for log files to go to.
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # Start the periodic call in the GUI to check if the queue contains anything
        self.periodic_call()

    def periodic_call(self, gui_refresh_interval=200):
        """!
        This is the "main loop" of the main thread. Based on the refresh interval,
        it will periodically get data from the sensors and pass it to the GUI to be displayed, then call itself
        to run again.
        @param gui_refresh_interval: Polling time (in miliseconds) of the sensors
        """

        # TODO: Investigate switching this from a polling update to an event driven update

        self.gui.processIncoming()
        if not self.main_running:
            # Close the GUI
            self.gui.master.destroy()
            # Cleanup time! For each process, pass it a STOP signal
            for sensor in self.sensors.values():
                sensor.queue.put("STOP")
            # Wait for the processes to stop
            time.sleep(3)
            # Terminate and join all processes
            for sensor in self.sensor_processes.values():
                sensor.terminate()
                sensor.join()
            # Brutal system exit. Make sure everything is cleaned up first!
            # TODO: This doesn't seem to be closing everything properly yet...
            sys.exit(0)

        # For each sensor, check if there is any data in its queue
        for sensor_name, sensor in self.sensors.items():
            if not sensor.queue.empty():
                msg = [sensor_name, sensor.queue.get()]

                # TODO: Do stuff with the data here

                # Relay the data to the GUI so the user can see it
                self.master_queue.put(msg)

        # Wait for the requested time and then call itself
        self.gui.master.after(gui_refresh_interval, self.periodic_call)

    def end_application(self):
        """!
        This method simply flags main_running as False.
        The "main loop" a.k.a periodic_call will notice this and begin shutdown
        """
        self.main_running = False

if __name__ == "__main__":
    ROOT = Tk()
    WIDTH, HEIGHT = ROOT.winfo_screenwidth(), ROOT.winfo_screenheight()
    ROOT.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
    # ROOT.geometry("250x150")
    CLIENT = ThreadedClient(ROOT)
    ROOT.mainloop()
