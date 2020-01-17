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
from multiprocessing import Queue, Process, active_children, set_start_method
from src.GUI.GUI import GrowSpaceGUI
from datetime import datetime
from src.utilities.pickle_utilities import export_object
from src.utilities.json_utilities import save_as_json

class ThreadedClient:
    """!
    This is the main thread class.
    In the future, when more boxes are implemented, there would be multiple
    instances of this class used, where each instance is for 1 box.
    @param gui: This is the main GUI
    @param master_queue: Queue between this thread and the GUI
    @param sensors: A dictionary mapping all Sensor class instances to a unique name. These are the sensors of the system.
    @param sensor_processes: A dictionary mapping all Sensor worker processes to a unique name. These are the sensor processes of the system.
    @param main_running: Flag to show if the main loop is running or called to exit.
    @param db_master: Master database.
    @param statueses: Dictionary containing all operating statuses
    @param simulated: Flag to show if the environment is a simulation
    """

    gui: GrowSpaceGUI = None
    master_queue: Queue = Queue()
    sensors: dict = dict()
    sensor_processes: dict = dict()
    main_running: bool = True
    db_master: dict = dict()
    statuses: dict = dict()
    simulated: bool = False

    def __init__(self, master, simulate_environment=False):
        """!
        Launches the GUI and the asynchronous worker processes (1 for each sensor).
        @param master: The root (instance) of a Tkinter top-level widget.
        @param simulate_environment: Flag for if the environment is to be simulated (for development).
        """

        self.simulated = simulate_environment
        self.gui = GrowSpaceGUI(master, self.master_queue, self.end_application)

        self.load_configuration()

        self.spawn_processes()

        # Ensure that there is a directory for log files to go to.
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # Ensure that there is a directory for databases to be stored.
        if not os.path.exists('database'):
            os.mkdir('database')
        self.db_master['latest'] = {}

        # Start the periodic call (main loop)
        self.periodic_call()

    def load_configuration(self):
        # TODO: Load the actual configuration file
        configuration_dict = {"Moisture_High": 80, "Moisture_Low": 60, "Moisture_Target": 70}
        for item, value in configuration_dict.items():
            self.db_master[item] = value

    def spawn_processes(self):
        if self.simulated:
            print("Running simulation...")
            from src.simulations import sim_env_sensor, sim_soil_sensor
            self.sensors['environment_sensor'] = sim_env_sensor.EnvironmentSensor(name="sim_environment_sensor", queue=Queue())
            self.sensors['soil_moisture_sensor_1'] = sim_soil_sensor.SoilMoistureSensor(name="sim_soil_moisture_sensor_1", queue=Queue())
        else:
            print("Running system...")
            from src.sensors.soil_moisture_sensor import SoilMoistureSensor
            from src.sensors.env_sensor import EnvironmentSensor
            self.sensors['soil_moisture_sensor_1'] = SoilMoistureSensor(name="soil_moisture_sensor_1", queue=Queue())
            self.sensors['environment_sensor'] = EnvironmentSensor(name="environment_sensor", queue=Queue())

        # Add all processes to dict
        for name, value in self.sensors.items():
            self.sensor_processes[name] = Process(target=value.run)
            self.sensor_processes[name].start()
        # Flag start
        self.main_running = True

    def periodic_call(self, gui_refresh_interval=200):
        """!
        This is the "main loop" of the main thread. Based on the refresh interval,
        it will periodically get data from the sensors and pass it to the GUI to be displayed, then call itself
        to run again.
        @param gui_refresh_interval: Polling time (in miliseconds) of the sensors
        """

        self.gui.processIncoming()
        if not self.main_running: # Time to shutdown
            self.gui.master.destroy() # Close the GUI
            for process in active_children(): # Terminate each process
                process.terminate()
                process.join()
            # Save database
            export_object("./database/master", self.db_master)
            save_as_json("./database/master", self.db_master)
            return 0

        # For each sensor, check if there is any data in its queue
        for sensor_name, sensor in self.sensors.items():
            if not sensor.queue.empty():
                sensor_data = sensor.queue.get()
                # Store in master database
                time = datetime.now().strftime("%m-%d-%y %H:%M:%S")
                if time not in self.db_master:
                    self.db_master[time] = {}
                self.db_master[time][sensor_name] = sensor_data
                self.db_master['latest'][sensor_name] = sensor_data
                # Save database
                export_object("./database/master", self.db_master)
                save_as_json("./database/master", self.db_master)
                # TODO: Run algorithms on the data
                if sensor_name == "soil_moisture_sensor_1":
                    from src.utilities.algorithms import watering_algorithm
                    msg = watering_algorithm(self.db_master, self.simulated)
                # Relay the data to the GUI so the user can see it
                else:
                    msg = [sensor_name, sensor_data]
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
    # WIDTH, HEIGHT = ROOT.winfo_screenwidth(), ROOT.winfo_screenheight()
    # ROOT.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
    ROOT.resizable()
    ROOT.geometry("350x150")
    CLIENT = ThreadedClient(ROOT, simulate_environment=True)
    ROOT.mainloop() # Blocking!
