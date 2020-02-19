"""!
This is the main thread from which the program is started/runs.
This thread will periodically call the sensor worker processes to 
poll for their data. This data is returned here, so it can be analysed
and control signals can be generated.
"""

import sys
import time
import datetime
import os
import atexit
from tkinter import Tk
from multiprocessing import Queue, Process, active_children, set_start_method
from src.GUI.GUI import GrowSpaceGUI
from datetime import datetime
from src.utilities.pickle_utilities import export_object
from src.utilities.json_utilities import save_as_json
from src.utilities.algorithms import watering_algorithm, environment_algorithm, lighting_algorithm


class ThreadedClient:
    """!
    This is the main thread class.
    In the future, when more boxes are implemented, there would be multiple
    instances of this class used, where each instance is for 1 box.
    @param gui: This is the main GUI
    @param main_to_gui_queue: Uni-directional queue going FROM this thread TO the gui
    @param gui_to_main_queue: Uni-directional queue going FROM the gui TO this thread
    @param sensors: A dictionary mapping all Sensor class instances to a unique name. These are the sensors of the system.
    @param sensor_processes: A dictionary mapping all Sensor worker processes to a unique name. These are the sensor processes of the system.
    @param controls: A dictionary containing access to control objects (relays)
    @param main_running: Flag to show if the main loop is running or called to exit.
    @param db_master: Master database.
    @param statuses: Dictionary containing all operating statuses
    @param simulated: Flag to show if the environment is a simulation
    @param configuration_file: Path to the current active system configuration file
    """

    gui: GrowSpaceGUI = None
    main_to_gui_queue: Queue = Queue()
    gui_to_main_queue: Queue = Queue()
    sensors: dict = dict()
    sensor_processes: dict = dict()
    controls: dict = dict()
    main_running: bool = True
    db_master: dict = dict()
    statuses: dict = dict()
    simulated: bool = False
    configuration_file: str = None

    def __init__(self, master, configuration_file="./configuration_files/basil", simulate_environment=False):
        """!
        Launches the GUI and the asynchronous worker processes (1 for each sensor).
        @param master: The root (instance) of a Tkinter top-level widget.
        @param configuration_file: The path to the configuration file that is to be loaded.
        @param simulate_environment: Flag for if the environment is to be simulated (for development).
        """

        # Before doing anything else, register a safe shutdown method for if the program crashes
        atexit.register(self.end_application)

        # Ensure that there is a directory for log files to go to.
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # Ensure that there is a directory for databases to be stored.
        if not os.path.exists('database'):
            os.mkdir('database')
        self.db_master['latest'] = {}

        # Set initial databse entries
        self.db_master["Pump Status"] = "OFF"
        self.db_master["Fan Status"] = "OFF"
        self.db_master["RGB LED Status"] = [0, 0, 0]
        self.db_master["UV LED Status"] = "OFF"

        self.simulated = simulate_environment
        self.configuration_file = configuration_file

        self.gui = GrowSpaceGUI(master, self.main_to_gui_queue, self.gui_to_main_queue, self.end_application)
        self.load_configuration()
        self.spawn_processes()
        self.add_controllers()

        # Start the periodic call (main loop)
        self.periodic_call()
        p_time = Process()

    def load_configuration(self):
        # Load configuration file
        from src.utilities.json_utilities import load_from_json
        configuration_dict = load_from_json(self.configuration_file)

        # Transfer configuration file data into master database
        for item, value in configuration_dict.items():
            self.db_master[item] = value

        # Set configuration parameters in GUI
        self.gui.SoilMoistureRange_value.configure(text=str(self.db_master["Moisture_Low"])+"% - "+str(self.db_master["Moisture_High"])+"%")
        self.gui.TemperatureRange_value.configure(text=str(self.db_master["Temperature_Low"])+"°C - "+str(self.db_master["Temperature_High"])+"°C")
        self.gui.HumidityRange_value.configure(text=str(self.db_master["Humidity_Low"])+"% - "+str(self.db_master["Humidity_High"])+"%")
        self.gui.VOCRange_value.configure(text=str(self.db_master["VOC_Low"])+"kΩ - "+str(self.db_master["VOC_High"])+"kΩ")
    
    def add_controllers(self):
        if self.simulated:
            from src.simulations import sim_relay, sim_led_strip
            self.controls['fan'] = sim_relay.Relay(pin=17, name="fan")
            self.controls['pump'] = sim_relay.Relay(pin=22, name="pump")
            self.controls['UV LED'] = sim_relay.Relay(pin=27, name="UV LED")
            self.controls['RGB LED'] = sim_led_strip.LEDStrip(LED_PIN=18, LED_COUNT=107, name="RGB LED")
        else:
            from src.controls import fan, pump, uv_led, led_strip
            self.controls['fan'] = fan.Fan(pin=17, name="fan", queue=Queue())
            self.controls['pump'] = pump.Pump(pin=22, name="pump", queue=Queue())
            self.controls['UV LED'] = uv_led.UVLed(pin=27, name="UV LED", queue=Queue())
            self.controls['RGB LED'] = led_strip.LEDStrip(LED_PIN=18, name="RGB LED")
        
        # Make sure everything starts off
        self.controls['fan'].turn_off()
        self.controls['pump'].turn_off()
        self.controls['UV LED'].turn_off()
        self.controls['RGB LED'].adjust_color(red_content=0, green_content=0, blue_content=0)

        # Send initial status to GUI
        self.main_to_gui_queue.put(["Pump Status", self.db_master["Pump Status"]])
        self.main_to_gui_queue.put(["Fan Status", self.db_master["Fan Status"]])
        self.main_to_gui_queue.put(["UV LED Status", self.db_master["UV LED Status"]])
        self.main_to_gui_queue.put(["RGB LED Status", self.db_master["RGB LED Status"]])

    def spawn_processes(self):
        if self.simulated:
            print("Running simulation...")
            from src.simulations import sim_env_sensor, sim_soil_sensor
            self.sensors['environment_sensor'] = sim_env_sensor.EnvironmentSensor(name="sim_environment_sensor", queue=Queue())
            self.sensors['soil_moisture_sensor_1'] = \
                sim_soil_sensor.SoilMoistureSensor(name="sim_soil_moisture_sensor_1", queue=Queue())
        else:
            print("Running system...")
            from src.sensors.soil_moisture_sensor import SoilMoistureSensor
            from src.sensors.env_sensor import EnvironmentSensor
            self.sensors['soil_moisture_sensor_1'] = SoilMoistureSensor(name="soil_moisture_sensor_1", queue=Queue(), channel=0, max_v=3, min_v=1)
            self.sensors['soil_moisture_sensor_2'] = SoilMoistureSensor(name="soil_moisture_sensor_2", queue=Queue(), channel=1, max_v=3, min_v=1)
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
        @param gui_refresh_interval: How often (in miliseconds) the GUI will get check its inbound queue for new data to display
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
                # p_lights = Process(target=lighting_algorithm, args=(self.db_master, self.controls,
                #                                                   self.simulated, False))
                # p_lights.start()

                if sensor_name == "soil_moisture_sensor_1":
                    msg = watering_algorithm(self.db_master, self.controls, self.simulated)
                elif sensor_name == "environment_sensor":
                    msg = environment_algorithm(self.db_master, self.controls, self.simulated)

                # if sensor_name == "soil_moisture_sensor_1":
                #     if self.db_master["last_watering"] < \
                #             self.db_master["last_watering"] + datetime.timedelta(minutes=1): # TODO change minutes
                #         p_water = Process(target=watering_algorithm, args=(self.db_master, self.controls,
                #                                                            self.simulated))
                #         p_water.start()
                #         self.db_master["last_watering"] = datetime.datetime.now()
                # elif sensor_name == "environment_sensor":
                #     p_env_sensor = Process(target=environment_algorithm, args=(self.db_master, self.controls,
                #                                                                self.simulated))
                #     p_env_sensor.start()
                # else:
                #     msg = [sensor_name, sensor_data]
                self.main_to_gui_queue.put(msg)

        # Check if the GUI is sending anything to main
        if not self.gui_to_main_queue.empty():
            msg = self.gui_to_main_queue.get()
            print("Received manual control from GUI:", msg)
            if msg == "Toggle Pump":
                self.controls['pump'].toggle()
                if self.db_master["Pump Status"] == "ON":
                    self.db_master["Pump Status"] = "OFF"
                else:
                    self.db_master["Pump Status"] = "ON"
                self.main_to_gui_queue.put(["Pump Status", self.db_master["Pump Status"]])
            elif msg == "Toggle Fan":
                self.controls['fan'].toggle()
                if self.db_master["Fan Status"] == "ON":
                    self.db_master["Fan Status"] = "OFF"
                else:
                    self.db_master["Fan Status"] = "ON"
                self.main_to_gui_queue.put(["Fan Status", self.db_master["Fan Status"]])
            elif msg == "Toggle UV":
                self.controls['UV LED'].toggle()
                if self.db_master["UV LED Status"] == "ON":
                    self.db_master["UV LED Status"] = "OFF"
                else:
                    self.db_master["UV LED Status"] = "ON"
                self.main_to_gui_queue.put(["UV LED Status", self.db_master["UV LED Status"]])
            elif isinstance(msg, list):
                if msg[0] == "RELOAD":
                    self.configuration_file = msg[1]
                    self.load_configuration()
                else:

                    if msg[0] == '' or int(msg[0]) < 0 or int(msg[0]) > 255:
                        red = 0
                    else:
                        red = int(msg[0])

                    if msg[1] == '' or int(msg[1]) < 0 or int(msg[1]) > 255:
                        green = 0
                    else:
                        green = int(msg[1])

                    if msg[2] == '' or int(msg[2]) < 0 or int(msg[2]) > 255:
                        blue = 0
                    else:
                        blue = int(msg[2])

                    self.controls['RGB LED'].adjust_color(red_content=red, green_content=green, blue_content=blue)
                    self.db_master["RGB LED Status"] = [red, green, blue]
                    if red == 69 or green == 69 or blue == 69 or (red == 6 and green == 9) or (green == 6 and blue ==9):
                        for _ in range(50):
                            import random
                            self.controls['RGB LED'].adjust_color(red_content=random.randint(0,255), green_content=random.randint(0,255), blue_content=random.randint(0,255))
                            time.sleep(0.2)
                            self.controls['RGB LED'].adjust_color(red_content=0, green_content=0, blue_content=0)
                            time.sleep(0.2)
                    self.main_to_gui_queue.put(["RGB LED Status", self.db_master["RGB LED Status"]])
                    if red == 4 and green == 2 and blue == 0:
                        r = 0
                        g = 150
                        while g > 0:
                            self.controls['RGB LED'].adjust_color(red_content=r, green_content=g, blue_content=0)
                            time.sleep(0.02)
                            g = g-1
                            r = r+1

                        time.sleep(5)
                        self.controls['RGB LED'].adjust_color(red_content=0, green_content=0, blue_content=0)

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
    # ROOT.resizable()
    ROOT.geometry("1024x600")
    CLIENT = ThreadedClient(ROOT, simulate_environment=True)
    ROOT.mainloop() # Blocking!
