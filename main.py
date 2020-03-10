"""!
This is the main thread from which the program is started/runs.
This thread will periodically call the sensor worker processes to 
poll for their data. This data is returned here, so it can be analysed
and control signals can be generated.
"""

import sys
import time
import datetime
import atexit
import argparse
import os
from tkinter import Tk
from multiprocessing import Queue, Process, active_children, set_start_method
from src.GUI.GUI import GrowSpaceGUI
from datetime import datetime, timedelta
from src.utilities.pickle_utilities import export_object
from src.utilities.json_utilities import save_as_json, load_from_json
from src.utilities.logger_utilities import get_logger
from src.utilities.file_utilities import generate_unique_filename
from src.utilities.algorithms import watering_algorithm, environment_algorithm, lighting_algorithm
from src.utilities.control_processes import watering_process, fan_process, lighting_process


class ThreadedClient:
    """!
    This is the main thread class.
    In the future, when more boxes are implemented, there would be multiple
    instances of this class used, where each instance is for 1 box.
    @param configuration_file: Path to the current active system configuration file.
    @param controls: A dictionary containing access to control objects (e.g, relays).
    @param control_processes: A dictionary containing access to control processes.
    @param control_statuses: A dictionary containing information about the status of control elements.
    @param db_master: The master database of the system.
    @param gui: This is the main GUI window.
    @param main_running: Flag to show if the main loop is running/called to exit.
    @param main_to_gui_queue: Uni-directional queue going FROM this thread TO the gui
    @param gui_to_main_queue: Uni-directional queue going FROM the gui TO this thread
    @param sensors: A dictionary mapping all Sensor class instances to a unique name. These are the sensors of the system.
    @param sensor_processes: A dictionary mapping all Sensor worker processes to a unique name. These are the sensor processes of the system.
    @param simulated: Flag to show if the environment is a simulation
    """

    configuration_file: str = None
    controls: dict = dict()
    control_processes: dict = dict()
    control_statuses: dict = dict()
    db_master: dict = dict()
    gui: GrowSpaceGUI = None
    main_running: bool = True
    main_to_gui_queue: Queue = Queue()
    gui_to_main_queue: Queue = Queue()
    sensors: dict = dict()
    sensor_processes: dict = dict()
    simulated: bool = False

    def __init__(self, master, configuration_file="basil", gui_refresh_interval=200, polling_interval=2, simulate_environment=False):
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

        # Create the logger for the main process (Main logger)
        self.logger = get_logger("Main")
        self.logger.debug("System start up.")

        # Ensure that there is a directory for databases to be stored.
        if not os.path.exists('database'):
            os.mkdir('database')
        self.db_master['latest'] = {}

        # Set initial database entries of control element status
        self.db_master["Pump Status"] = "OFF"
        self.db_master["Fan Status"] = "OFF"
        self.db_master["RGB LED Status"] = [0, 0, 0]
        self.db_master["UV LED Status"] = "OFF"

        # Set initial database entries for manual override conditions
        self.db_master['Manual Overrides'] = {}
        self.db_master['Manual Overrides']['Pump'] = False
        self.db_master['Manual Overrides']['Fan'] = False
        self.db_master['Manual Overrides']['RGB LED'] = False
        self.db_master['Manual Overrides']['UV LED'] = False

        # Initialize the storage for the algorithm processes and their corresponding queues
        self.control_processes['watering'] = {}
        self.control_processes['watering']['Process'] = None
        self.control_processes['watering']['Queue'] = Queue()
        self.control_processes['fan'] = {}
        self.control_processes['fan']['Process'] = list()
        self.control_processes['fan']['Queue'] = Queue()

        # Initialize control statuses
        # Status is either "Free" or "Busy"
        self.control_statuses['pump'] = "Free"
        self.control_statuses['fan'] = "Free"
        self.control_statuses['UV LED'] = "Free"
        self.control_statuses['RGB LED'] = "Free"

        self.simulated = simulate_environment
        self.configuration_file = configuration_file

        # Spawn the GUI
        self.gui = GrowSpaceGUI(master, self.main_to_gui_queue, self.gui_to_main_queue, self.end_application)

        # Load the configuration file
        self.load_configuration()

        # Spawn all sensor processes
        self.spawn_sensor_processes(polling_interval)

        # Add control elements
        self.add_controllers()

        # Start the periodic call (main loop)
        self.periodic_call(gui_refresh_interval)

    def load_configuration(self):
        """!
        This method is used to load/reload the system based on a configuration file.
        """
        # Load configuration file
        self.logger.debug("Loading configuration file: "+self.configuration_file)
        configuration_dict = load_from_json("./configuration_files/"+self.configuration_file)

        # Transfer configuration file data into master database
        self.logger.debug("Transferring configuration data into the master database...")
        for item, value in configuration_dict.items():
            self.logger.debug("Transferring: "+str(item)+" : "+str(value))
            self.db_master[item] = value
        self.logger.debug("Transfer complete.")

        # Set configuration parameters in GUI
        self.logger.debug("Updating control parameters in GUI...")
        self.gui.SoilMoistureRange_value.configure(text=str(self.db_master["Moisture_Low"])+"% - "+str(self.db_master["Moisture_High"])+"%")
        self.gui.TemperatureRange_value.configure(text=str(self.db_master["Temperature_Low"])+"°C - "+str(self.db_master["Temperature_High"])+"°C")
        self.gui.HumidityRange_value.configure(text=str(self.db_master["Humidity_Low"])+"% - "+str(self.db_master["Humidity_High"])+"%")
        self.gui.VOCRange_value.configure(text=str(self.db_master["VOC_Low"])+"kΩ - "+str(self.db_master["VOC_High"])+"kΩ")

        # TODO: Insert RGB and UV LEDs once algorithm is created
        self.logger.debug("Configuration file loaded. System is now running on new environment parameters.")
    
    def add_controllers(self):
        """!
        This method is used for adding all the control elements (controllers) into the main memory heap.
        This way, the main thread has access to all the control elements.
        It will also ensure that everything starts up as OFF
        """
        if self.simulated:
            from src.simulations import sim_relay, sim_led_strip
            self.controls['fan'] = sim_relay.Relay(pin=17, name="fan")
            self.controls['pump'] = sim_relay.Relay(pin=22, name="pump")
            self.controls['UV LED'] = sim_relay.Relay(pin=27, name="UV LED")
            self.controls['RGB LED'] = sim_led_strip.LEDStrip(LED_PIN=18, LED_COUNT=107, name="RGB LED")
        else:
            from src.controls import fan, pump, uv_led, led_strip
            self.controls['fan'] = fan.Fan(pin=17, name="fan")
            self.controls['pump'] = pump.Pump(pin=22, name="pump")
            self.controls['UV LED'] = uv_led.UVLed(pin=27, name="UV LED")
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

    def spawn_sensor_processes(self, polling_interval):
        """!
        This method is used to spawn all the sensor processes.
        Based on whether the system is to be simulated or not, it will chose which processes to use
        as the sensor processes.
        """
        if self.simulated:
            self.logger.debug("Running simulation...")
            from src.simulations import sim_env_sensor, sim_soil_sensor
            self.sensors['environment_sensor'] = sim_env_sensor.EnvironmentSensor(name="sim_environment_sensor", queue=Queue(), polling_interval=polling_interval)
            self.sensors['soil_moisture_sensor_1'] = sim_soil_sensor.SoilMoistureSensor(name="sim_soil_moisture_sensor_1", queue=Queue(), polling_interval=polling_interval)
            self.sensors['soil_moisture_sensor_2'] = sim_soil_sensor.SoilMoistureSensor(name="sim_soil_moisture_sensor_2", queue=Queue(), polling_interval=polling_interval)
        else:
            self.logger.debug("Running system...")
            from src.sensors.soil_moisture_sensor import SoilMoistureSensor
            from src.sensors.env_sensor import EnvironmentSensor
            self.sensors['soil_moisture_sensor_1'] = SoilMoistureSensor(name="soil_moisture_sensor_1", queue=Queue(), polling_interval=polling_interval, channel=0, max_v=3, min_v=1)
            self.sensors['soil_moisture_sensor_2'] = SoilMoistureSensor(name="soil_moisture_sensor_2", queue=Queue(), polling_interval=polling_interval, channel=1, max_v=3, min_v=1)
            self.sensors['environment_sensor'] = EnvironmentSensor(name="environment_sensor", queue=Queue(), polling_interval=polling_interval)

        # Add all processes to dict
        for name, value in self.sensors.items():
            self.sensor_processes[name] = Process(target=value.run)
            self.sensor_processes[name].start()
        # Flag start
        self.main_running = True

    def periodic_call(self, gui_refresh_interval=200):
        """!
        This is the "main loop" of the main thread.
        In order to conserve processing power, this loop has a delay between iterations equal to the gui_refresh_interval.
        The process is as follows:
        1. Check if the user has signalled for the application to shutdown. If so, shutdown everything.
        2. Check if the user is trying to do any manual overrides using the "control" window of the GUI.
        For each control element that is manually overriden, it will add a corresponding flag into the master database.
        This flag is checked by the control algorithms, and if it is present, it will prevent the algorithms from controlling that control element.
        These flags are cleared and automaticity is regained when the user closes the "control" window. 
        3. Check if there is new data coming in from a sensor. If there is, run an algorithm on the data to generate a control message.
        This control message is then passed to a control_process (if necessary and not blocked)

        @param gui_refresh_interval: How often (in miliseconds) the GUI will get check its inbound queue for new data to display
        """

        self.gui.process_incoming()

        # Check if the user has signaled to shutdown the application
        if not self.main_running:
            self.gui.master.destroy() # Close the GUI
            for process in active_children(): # Terminate each process
                process.terminate()
                process.join()
            # Save database
            export_object("./database/master", self.db_master)
            save_as_json("./database/master", self.db_master)
            return 0

        # Check if the GUI is sending anything to main (manual override commands)
        if not self.gui_to_main_queue.empty():
            msg = self.gui_to_main_queue.get()
            self.manual_override(msg) # Execute the manual override command

        # Get the current time and send it to the lighting algorithm
        self.current_time = datetime.now()
        try:
            light_response = lighting_algorithm(self.current_time, self.previous_time)
            if light_response:
                lighting_process(self.db_master, self.controls)
        except AttributeError:
            self.logger.debug("Main loop is running its first iteration...")
        self.previous_time = self.current_time

        # For each sensor, check if there is any data in its queue
        for sensor_name, sensor in self.sensors.items():
            if not sensor.queue.empty():

                # If there is data, get it, save it to the master database, then save the master database
                sensor_data = sensor.queue.get()
                current_time = datetime.now().strftime("%m-%d-%y %H:%M:%S")
                if current_time not in self.db_master:
                    self.db_master[current_time] = {}
                self.db_master[current_time][sensor_name] = sensor_data
                self.db_master['latest'][sensor_name] = sensor_data
                export_object("./database/master", self.db_master)
                save_as_json("./database/master", self.db_master)

                if 'soil_moisture_sensor' in sensor_name:
                    # First, run the watering algorithm to generate the control message.
                    msg = watering_algorithm(self.db_master)

                    # Relay the message to the GUI so the values can be updated
                    self.main_to_gui_queue.put(msg)

                    # If the flag is not None, that means that the moisture level is outside of accepted range. So...
                    flag = msg[2]
                    if flag is not None:
                        try:
                            current_time = datetime.now()
                            do_process = True

                            # Check if the pump is currently being manually overridden
                            if self.db_master['Manual Overrides']['Pump']:
                                self.logger.debug("Moisture detected low, but pump is in manual override")
                                do_process = False

                            # Check if the pump is already running from a previous algorithm check
                            elif self.control_statuses['pump'] == "Busy":
                                self.logger.debug("Moisture detected low, but pump is already running")
                                do_process = False

                            # Check if the system is still waiting for the previous watering to soak into the soil
                            if "soak_end_time" in self.db_master:
                                if current_time <= self.db_master['soak_end_time']:
                                    self.logger.info("Waiting for soak-in to finish. Time remaining: " + str(self.db_master['soak_end_time'] - current_time))
                                    do_process = False

                            # If there is no condition blocking the control_process from running, execute it 
                            if do_process:
                                if flag == "LOW": # Water level is low, need to pump
                                    self.db_master["Pump Status"] = "ON"  # Explicitly declare that the pump is now ON
                                    self.controls['pump'].is_off = False
                                    self.logger.info("Pump has turned on.")
                                    self.main_to_gui_queue.put(["Pump Status", self.db_master["Pump Status"]])
                                    self.control_statuses['pump'] = "Busy"
                                    self.control_processes['watering']['Process'] = \
                                        Process(target=watering_process,
                                                args=(msg, self.controls, self.control_processes['watering']['Queue'],
                                                      self.db_master))
                                    self.control_processes['watering']['Process'].start()
                                elif flag == "HIGH":  # TODO: Are we going to do anything in this circumstance?
                                    pass
                                else:  # Water level is good, so no need to do anything
                                    pass

                        except Exception as err:
                            self.logger.error("Exception thrown in main: "+str(err))

                elif 'environment_sensor' in sensor_name:
                    # First, run the environment algorithm to generate the control message.
                    msg = environment_algorithm(self.db_master)

                    # Relay the message to the GUI so the values can be updated
                    self.main_to_gui_queue.put(msg)

                    temperature_flag = msg[1]['temperature']['flag']
                    if temperature_flag is not None:
                        current_time = datetime.now()
                        do_process = True

                        # Check if the fan is currently being manually overridden
                        if self.db_master['Manual Overrides']['Fan']:
                            self.logger.info("Fan is in manual override")
                            do_process = False

                        # Check if the fan is already running from a previous algorithm check
                        elif self.control_statuses['fan'] == "Busy":
                            self.logger.info("Fan is already running")
                            do_process = False
                        
                        # If there is no condition blocking the control_process from running, execute it 
                        if do_process:
                            self.control_statuses['fan'] = "Busy"  # Explicitly declare that the fan is now busy
                            if temperature_flag == "HIGH":
                                self.db_master["Fan Status"] = "ON"
                            elif temperature_flag == "LOW":
                                self.db_master["Fan Status"] = "OFF"
                            else:
                                self.logger.warning("Unexpected temperature flag: "+str(temperature_flag))
                            self.main_to_gui_queue.put(["Fan Status", self.db_master["Fan Status"]])
                            self.control_statuses['fan'] = "Busy"
                            self.control_processes['fan']['Process'] = \
                                Process(target=fan_process,
                                        args=(msg, self.controls, self.control_processes['fan']['Queue']))
                            self.control_processes['fan']['Process'].start()

        for control_process_name, control_process in self.control_processes.items():
            if not control_process['Queue'].empty():
                msg = control_process['Queue'].get()
                self.logger.debug("Message from "+str(control_process_name) + ": " + msg)
                if control_process_name == "watering":
                    self.db_master['last_watering'] = datetime.now()
                    self.db_master['soak_end_time'] = \
                        self.db_master['last_watering'] + timedelta(minutes=self.db_master['Soak_Minutes'])
                    self.control_statuses['pump'] = "Free"
                    self.controls['pump'].is_off = True
                    self.db_master["Pump Status"] = "OFF"
                    self.logger.info("Pump has turned off.")
                    self.main_to_gui_queue.put(["Pump Status", self.db_master["Pump Status"]])
                if control_process_name == "fan":
                    self.control_statuses['fan'] = "Free"
                    if msg == "Fan turned ON":
                        self.db_master["Fan Status"] = "ON"
                    elif msg == "Fan turned OFF":
                        self.db_master["Fan Status"] = "OFF"
                    else:
                        self.logger.warning("Unexpected msg from fan process" + str(msg))
                    self.main_to_gui_queue.put(["Fan Status", self.db_master["Fan Status"]])
                control_process['Process'].terminate()
                control_process['Process'].join()
    
        # Wait for a refresh interval to elapse, then call itself to execute again
        self.gui.master.after(gui_refresh_interval, self.periodic_call)

    def manual_override(self, msg):
        """!
        Whenever the main thread receives a manual override command, the command is passed to this function.
        This function decides what to do with the command, and updates database variables accordingly.

        @param msg: The manual override command.
        """
        self.logger.info("Received manual override: "+str(msg))
        if msg == "END":
            self.logger.info("Control window has been closed. Manual override disengaged.")
            self.db_master['Manual Overrides']['Pump'] = False
            self.control_statuses['pump'] = "Free"
            self.db_master['Manual Overrides']['Fan'] = False
            self.db_master['Manual Overrides']['RGB LED'] = False
            self.db_master['Manual Overrides']['UV LED'] = False

        elif msg == "Pump OFF":
            self.db_master['Manual Overrides']['Pump'] = True
            self.controls['pump'].turn_off()
            self.db_master["Pump Status"] = "OFF"
            self.main_to_gui_queue.put(["Pump Status", self.db_master["Pump Status"]])

        elif msg == "Pump ON":
            self.db_master['Manual Overrides']['Pump'] = True
            self.controls['pump'].turn_on()
            self.db_master["Pump Status"] = "ON"
            self.main_to_gui_queue.put(["Pump Status", self.db_master["Pump Status"]])

        elif msg == "Fan OFF":
            self.db_master['Manual Overrides']['Pump'] = True
            self.controls['fan'].turn_off()
            self.db_master["Fan Status"] = "OFF"
            self.main_to_gui_queue.put(["Fan Status", self.db_master["Fan Status"]])

        elif msg == "Fan ON":
            self.db_master['Manual Overrides']['Pump'] = True
            self.controls['fan'].turn_on()
            self.db_master["Fan Status"] = "ON"
            self.main_to_gui_queue.put(["Fan Status", self.db_master["Fan Status"]])

        elif msg == "UV OFF":
            self.db_master['Manual Overrides']['UV LED'] = True
            self.controls['UV LED'].turn_off()
            self.db_master["UV LED Status"] = "OFF"
            self.main_to_gui_queue.put(["UV LED Status", self.db_master["UV LED Status"]])

        elif msg == "UV ON":
            self.db_master['Manual Overrides']['UV LED'] = True
            self.controls['UV LED'].turn_on()
            self.db_master["UV LED Status"] = "ON"
            self.main_to_gui_queue.put(["UV LED Status", self.db_master["UV LED Status"]])

        # if msg == "Toggle Pump":
        #     self.db_master['Manual Overrides']['Pump'] = True
        #     self.controls['pump'].toggle()
        #     if self.db_master["Pump Status"] == "ON":
        #         self.db_master["Pump Status"] = "OFF"
        #     else:
        #         self.db_master["Pump Status"] = "ON"
        #     self.main_to_gui_queue.put(["Pump Status", self.db_master["Pump Status"]])
        #
        # elif msg == "Toggle Fan":
        #     self.db_master['Manual Overrides']['Fan'] = True
        #     self.controls['fan'].toggle()
        #     if self.db_master["Fan Status"] == "ON":
        #         self.db_master["Fan Status"] = "OFF"
        #     else:
        #         self.db_master["Fan Status"] = "ON"
        #     self.main_to_gui_queue.put(["Fan Status", self.db_master["Fan Status"]])
        #
        # elif msg == "Toggle UV":
        #     self.db_master['Manual Overrides']['UV LED'] = True
        #     self.controls['UV LED'].toggle()
        #     if self.db_master["UV LED Status"] == "ON":
        #         self.db_master["UV LED Status"] = "OFF"
        #     else:
        #         self.db_master["UV LED Status"] = "ON"
        #     self.main_to_gui_queue.put(["UV LED Status", self.db_master["UV LED Status"]])
    
        elif isinstance(msg, list):
            # It is considered a manual override to load a new configuration file. Hence the code appears here
            if msg[0] == "RELOAD":
                self.configuration_file = msg[1]
                self.load_configuration()
            else: # TODO: This isn't exactly the best idea. We really should be checking to ensure this is only for RGB LED and not anything else.
                self.db_master['Manual Overrides']['RGB LED'] = True

                # Check to ensure all colors are within the accepted range, else default to 0
                try:
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
                except ValueError as err:
                    self.logger.error("ValueError in main:" + str(err))
                    red, green, blue = 0, 0, 0

                # Adjust the RGB lights accordingly
                self.controls['RGB LED'].adjust_color(red_content=red, green_content=green, blue_content=blue)

                # Update the status in the master database
                self.db_master["RGB LED Status"] = [red, green, blue]

                # Just for fun!
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
    
    def end_application(self):
        """!
        This method simply flags main_running as False.
        The "main loop" a.k.a periodic_call will notice this and begin shutdown
        """
        self.main_running = False


def check_terminate_process(process):
    if not process.is_alive():
        process.terminate()
        process.join()
    return True      


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-r', '--refresh', type=int, default=200, help='GUI refresh interval (ms)')
    parser.add_argument('-p', '--polling', type=int, default=2, help='Sensor polling interval (s)')
    parser.add_argument('-s', '--simulate', action='store_true', help='Boolean for simulating the environment')
    parser.add_argument('-c', '--config', type=str, default="basil", help="Name of the environment configuration file")
    args = parser.parse_args()

    ROOT = Tk()
    # WIDTH, HEIGHT = ROOT.winfo_screenwidth(), ROOT.winfo_screenheight()
    # ROOT.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
    # ROOT.resizable()
    ROOT.geometry("1024x600")

    if args.simulate:
        CLIENT = ThreadedClient(ROOT, configuration_file= args.config, gui_refresh_interval=args.refresh, polling_interval=args.polling, simulate_environment=True)
    else:
        CLIENT = ThreadedClient(ROOT, configuration_file= args.config, gui_refresh_interval=args.refresh, polling_interval=args.polling, simulate_environment=False)
    ROOT.mainloop()
