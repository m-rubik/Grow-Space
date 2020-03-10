"""!
This is the Graphical User Interface (GUI) that the user can use.
The GUI is based on a Tkinter widget.
"""


import sys
from multiprocessing import Queue
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, N, S, StringVar
from tkinter.filedialog import askopenfile, asksaveasfile
from src.utilities.json_utilities import save_as_json
from src.utilities.logger_utilities import get_logger


class GrowSpaceGUI:
    """!
    GUI class for any grow space box.
    @param queue_in: Uni-directional queue going FROM the main process TO this process
    @param queue_out: Uni-directional queue going FROM this process TO the main process
    @param master: The root (instance) of a Tkinter top-level widget
    """

    queue_in: Queue = None
    queue_out: Queue = None
    master = None


    def __init__(self, master, queue_in, queue_out, endCommand):
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.master = master
        self.control_window_open = False
        self.configure_window_open = False

        self.logger = get_logger(name="GUI")
        self.logger.debug("GUI start up.")

        self.master.title("Grow Space")
        self.master.configure(background="Black")

        ############################### Declare Labels ####################################################

        self.Title = Label(self.master, bg = "Black", fg = "White", text = "Grow Space", font = "Helvetica 24 bold italic")

        self.EnvironmentalConditionHeader = Label(self.master, bg = "Black", fg = "White", text = "Environmental Conditions", font="Helvetica 24 bold")
        self.SoilMoistureCondition = Label(self.master, bg = "Black", fg = "White", text= "Soil Moisture:", font = "Helvetica 22")
        self.TemperatureCondition = Label(self.master, bg = "Black", fg = "White", text= "Temperature:", font = "Helvetica 22")
        self.HumidityCondition = Label(self.master, bg = "Black", fg = "White", text= "Humidity:", font = "Helvetica 22")
        self.VOCCondition = Label(self.master, bg = "Black", fg = "White", text="VOC:", font = "Helvetica 22")

        self.ParameterRangeHeader = Label(self.master, bg = "Black", fg = "White", text = "Parameter Ranges", font="Helvetica 24 bold")
        self.SoilMoistureRange= Label(self.master, bg="Black", fg="White", text="Soil Moisture:", font="Helvetica 22")
        self.TemperatureRange = Label(self.master, bg="Black", fg="White", text="Temperature:", font="Helvetica 22")
        self.HumidityRange = Label(self.master, bg="Black", fg="White", text="Humidity:", font="Helvetica 22")
        self.VOCRange = Label(self.master, bg="Black", fg="White", text="VOC:", font="Helvetica 22")

        self.EnvironmentalStatusHeader = Label(self.master, bg = "Black",  fg = "White", text="Environmental Statuses", font="Helvetica 24 bold")
        self.SoilMoistureStatus = Label(self.master, bg="Black", fg="White", text="Soil Moisture:", font="Helvetica 22")
        self.TemperatureStatus = Label(self.master, bg="Black", fg="White", text="Temperature:", font="Helvetica 22")
        self.HumidityStatus = Label(self.master, bg="Black", fg="White", text="Humidity:", font="Helvetica 22")
        self.VOCStatus = Label(self.master, bg="Black", fg="White", text="VOC:", font="Helvetica 22")

        self.DeviceStatusHeader = Label(self.master, bg = "Black", fg = "White", text="Device Statuses", font="Helvetica 24 bold")
        self.PumpStatus = Label(self.master, bg = "Black", fg = "White", text="Pump:", font="Helvetica 22")
        self.FanStatus = Label(self.master, bg="Black", fg="White", text="Fan:", font="Helvetica 22")
        self.RGBLEDIntensity = Label(self.master, bg="Black", fg="White", text="RGB LEDs:", font="Helvetica 22")
        self.UVLEDIntensity = Label(self.master, bg="Black", fg="White", text="UV LEDs:", font="Helvetica 22")


        #Creating Label Values
        self.SoilMoistureCondition_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.TemperatureCondition_value  = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.HumidityCondition_value  = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.VOCCondition_value  = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")

        self.SoilMoistureStatus_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.TemperatureStatus_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.HumidityStatus_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.VOCStatus_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")

        self.SoilMoistureRange_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.TemperatureRange_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.HumidityRange_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.VOCRange_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")

        self.PumpStatus_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.FanStatus_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.RGBLEDIntensity_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")
        self.UVLEDIntensity_value = Label(self.master, bg="Black", fg="White", text=None, font="Helvetica 22")


        #Creating Buttons
        self.LoadButton = Button(self.master, bg = "White", fg="Black", text="LOAD", font="Helvetica 24 bold", command=self.load_file)
        self.SaveButton = Button(self.master, bg="White", fg="Black", text="SAVE", font="Helvetica 24 bold", command=self.save_file)
        self.PowerButton = Button(self.master, bg="White", fg="Black", text="\u23FB", font="Helvetica 24 bold", command=endCommand)
        self.ConfigureButton = Button(self.master, bg="White", fg="Black", text="CONFIGURE", font="Helvetica 24 bold", command=self.configure_window)
        self.ControlButton = Button(self.master, bg="White", fg="Black", text="CONTROL", font="Helvetica 24 bold", command=self.control_window)

        # creates a grid 50 x 50 in the main window
        rows = 0
        while rows < 50:
            self.master.grid_rowconfigure(rows, weight=1, minsize=1)  # Empty Row
            self.master.grid_columnconfigure(rows, weight=1, minsize=1)  # Empty column
            rows += 1

        ##### Positioning elements within the grid ###################

        self.Title.grid(row=0, column=5, columnspan=5, sticky=W)

        #Environmental Conditions
        self.EnvironmentalConditionHeader.grid(row=6, column=5, columnspan=10, sticky=W)
        self.SoilMoistureCondition.grid(row=8, column=5, sticky=W)
        self.TemperatureCondition.grid(row=10, column=5, sticky=W)
        self.HumidityCondition.grid(row=12, column=5, sticky=W)
        self.VOCCondition.grid(row=14, column=5, sticky=W)

        # Condition Values
        self.SoilMoistureCondition_value.grid(row=8, column=6,  sticky=W+E)
        self.TemperatureCondition_value.grid(row=10, column=6,  sticky=W+E)
        self.HumidityCondition_value.grid(row=12, column=6,  sticky=W+E)
        self.VOCCondition_value.grid(row=14, column=6, sticky=W+E)

        # Range Headers
        self.ParameterRangeHeader.grid(row=6, column=22, columnspan=10, sticky=W)
        self.SoilMoistureRange.grid(row=8, column=22, sticky=W)
        self.TemperatureRange.grid(row=10, column=22, sticky=W)
        self.HumidityRange.grid(row=12, column=22, sticky=W)
        self.VOCRange.grid(row=14, column=22, sticky=W)

        #Range Values
        self.SoilMoistureRange_value.grid(row=8, column=29, sticky=W+E)
        self.TemperatureRange_value.grid(row=10, column=29, sticky=W+E)
        self.HumidityRange_value.grid(row=12, column=29, sticky=W+E)
        self.VOCRange_value.grid(row=14, column=29, sticky=W+E)

        # Environmental Status Headers
        self.EnvironmentalStatusHeader.grid(row=24, column=5, columnspan=10, sticky=W)
        self.SoilMoistureStatus.grid(row=26, column=5, sticky=W)
        self.TemperatureStatus.grid(row=28, column=5, sticky=W)
        self.HumidityStatus.grid(row=30, column=5, sticky=W)
        self.VOCStatus.grid(row=32, column=5, sticky=W)

        #Environmental Status Values
        self.SoilMoistureStatus_value.grid(row=26, column=6, sticky=W+E)
        self.TemperatureStatus_value.grid(row=28, column=6, sticky=W+E)
        self.HumidityStatus_value.grid(row=30, column=6, sticky=W+E)
        self.VOCStatus_value.grid(row=32, column=6, sticky=W+E)

        #Device Status Headers
        self.DeviceStatusHeader.grid(row=24, column=22, columnspan=10, sticky=W)
        self.PumpStatus.grid(row=26, column=22, sticky=W)
        self.FanStatus.grid(row=28, column=22, sticky=W)
        self.RGBLEDIntensity.grid(row=30, column=22, sticky=W)
        self.UVLEDIntensity.grid(row=32, column=22, sticky=W)

        #Device Status Values
        self.PumpStatus_value.grid(row=26, column=29, sticky=W+E)
        self.FanStatus_value.grid(row=28, column=29, sticky=W+E)
        self.RGBLEDIntensity_value.grid(row=30, column=29, sticky=W+E)
        self.UVLEDIntensity_value.grid(row=32, column=29, sticky=W+E)

        #Button Locations
        self.LoadButton.grid(row=45, column=6, columnspan=3, sticky=W)
        self.SaveButton.grid(row=45, column=9, columnspan=3, sticky=E)
        self.PowerButton.grid(row=45, column=5, columnspan=1, sticky=W+E, padx=(40, 40))
        self.ConfigureButton.grid(row=45, column=22, columnspan=1)
        self.ControlButton.grid(row=45, column=29, columnspan=1)

    ##################### FUNCTIONS ################################################################

    def load_file(self):
        files = [("JSON files", "*.json")]
        config_file = askopenfile(filetypes=files, defaultextension = files)
        if config_file is None: # User closes the dialog with "cancel"
            self.logger.warning("User did not chose a configuration file to load")
        else:
            self.queue_out.put(["RELOAD", (config_file.name.split(".json")[0]).split("configuration_files/")[1]])
           
    def save_file(self): 
        files = [("JSON files", "*.json")] 
        config_file = asksaveasfile(filetypes = files, defaultextension = files)
        if config_file is None: # User closes the dialog with "cancel"
            self.logger.warning("User cancelled configuration file save")
        else:
            # TODO: Obtain the data that they entered in the Entry boxes (that are yet to be made), and format it as
            # a dictionnary (see the main call in src.utilities.json_utilities as an example of how the data should be structured). 
            data = {}
            data['Temperature_Low'] = 1
            data['Temperature_High'] = 1
            data['Moisture_Low'] = 1
            data['Moisture_High'] = 1
            data['Humidity_Low'] = 1
            data['Humidity_High'] = 1
            data['VOC_Low'] = 1
            data['VOC_High'] = 1

            save_as_json((config_file.name.split(".json")[0]).split("configuration_files/")[1], data)

    def control_window(self):

        def on_closing():
            self.queue_out.put("END")
            try:
                self.control_win.destroy()
                self.control_window_open = False
            except Exception as e:
                self.logger.error(str(e))

        if not self.control_window_open:

            self.control_win = Tk()
            self.control_window_open = True
            self.control_win.title("Control Devices")
            self.control_win.configure(bg="Slate Gray")
            self.control_win.geometry("400x600")
            self.control_win.protocol("WM_DELETE_WINDOW", on_closing)


            self.Red_val = StringVar()
            self.Green_val = StringVar()
            self.Blue_val = StringVar()

            #Defining Labels
            self.control_win.GrowSpaceTitle = Label(self.control_win, bg="Slate Gray", fg="White", text="Grow Space", font="Helvetica 20 bold italic")
            self.control_win.RGB_Label = Label(self.control_win, bg="Slate Gray", fg = "White", text="RGB LEDs", font="Helvetica 18 bold")
            self.control_win.Red_Entry_Label = Label(self.control_win, fg="Red", bg="Slate Gray", text="RED", font="Helvetica 18 bold")
            self.control_win.Green_Entry_Label = Label(self.control_win, fg="Green2", bg="Slate Gray", text="GREEN", font="Helvetica 18 bold")
            self.control_win.Blue_Entry_Label = Label(self.control_win, fg="DeepSkyBlue", bg="Slate Gray", text="BLUE",font="Helvetica 18 bold")
            self.control_win.UV_Label = Label(self.control_win, bg="Slate Gray", fg = "White", text="UV LEDs", font="Helvetica 18 bold")
            self.control_win.Fan_Label = Label(self.control_win, bg="Slate Gray", fg = "White", text="Fan", font="Helvetica 18 bold")
            self.control_win.Pump_Label = Label(self.control_win, bg="Slate Gray", fg = "White", text="Pump", font="Helvetica 18 bold")

            #Defining Entries
            self.control_win.Red_Entry = Entry(self.control_win, width=4, textvariable=self.Red_val)
            self.control_win.Green_Entry = Entry(self.control_win, width=4, textvariable=self.Green_val)
            self.control_win.Blue_Entry = Entry(self.control_win, width=4, textvariable=self.Blue_val)

            # Defining Control Window Buttons
            self.control_win.RGBLED_Set = Button(self.control_win, bg = "White", fg="Black", text = "SET",font="Helvetica 16 bold", command=lambda: self.queue_out.put([self.control_win.Red_Entry.get(),self.control_win.Green_Entry.get(),self.control_win.Blue_Entry.get()]))
            self.control_win.RGBLED_OFF = Button(self.control_win, bg="White", fg="Black", text="OFF", font="Helvetica 16 bold", command=lambda: self.queue_out.put(["0","0","0"]))
            self.control_win.UV_OFF = Button(self.control_win, bg="White", fg="Black", text="OFF", font="Helvetica 16 bold", command=lambda: self.queue_out.put("UV OFF"))
            self.control_win.UV_ON = Button(self.control_win, bg="White", fg="Black", text="ON",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("UV ON"))
            self.control_win.Fan_OFF = Button(self.control_win, bg="White", fg="Black", text="OFF",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("Fan OFF"))
            self.control_win.Fan_ON = Button(self.control_win, bg="White", fg="Black", text="ON",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("Fan ON"))
            self.control_win.Pump_OFF = Button(self.control_win, bg="White", fg="Black", text="OFF",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("Pump OFF"))
            self.control_win.Pump_ON = Button(self.control_win, bg="White", fg="Black", text="ON",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("Pump ON"))
            self.control_win.ExitButton = Button(self.control_win, bg="White", fg="Black", text="BACK",font="Helvetica 16 bold", command=lambda: (self.queue_out.put("END"), on_closing()))


            self.control_win.GrowSpaceTitle.grid(row=0, column=0, pady=(0,20))
            self.control_win.RGB_Label.grid(row=1,column=0,  pady=(0,10), sticky=W)
            self.control_win.Red_Entry_Label.grid(row=2, column=0, pady=(0,10), sticky=W)
            self.control_win.Red_Entry.grid(row=2, column=1, columnspan=2, pady=(0,10), sticky=W+E)
            self.control_win.Green_Entry_Label.grid(row=3, column=0, pady=(0,10), sticky=W)
            self.control_win.Green_Entry.grid(row=3,column=1, columnspan=2, pady=(0,10), sticky=W+E)
            self.control_win.Blue_Entry_Label.grid(row=4, column=0, pady=(0,10), sticky=W)
            self.control_win.Blue_Entry.grid(row=4, column=1, columnspan=2, pady=(0,10), sticky=W + E)
            self.control_win.RGBLED_Set.grid(row=5, column=1, pady=(10,20), sticky=W + E)
            self.control_win.RGBLED_OFF.grid(row=5, column=2, padx=(20,0), pady=(10,20), sticky=E)

            self.control_win.UV_Label.grid(row=6, column=0, pady=(0,10), sticky=W)
            self.control_win.UV_OFF.grid(row=6, column=1,  pady=(0,10), sticky=W+E)
            self.control_win.UV_ON.grid(row=6, column=2, padx=(20,0), pady=(0, 10), sticky=W + E)

            self.control_win.Fan_Label.grid(row=7, column=0, pady=(0, 10), sticky=W)
            self.control_win.Fan_OFF.grid(row=7, column=1, pady=(0, 10),  sticky=W + E)
            self.control_win.Fan_ON.grid(row=7, column=2, padx=(20,0),  pady=(0, 10), sticky=W + E)

            self.control_win.Pump_Label.grid(row=8, column=0, pady=(0, 10), sticky=W)
            self.control_win.Pump_OFF.grid(row=8, column=1,  pady=(0, 10), sticky=W + E)
            self.control_win.Pump_ON.grid(row=8, column=2, padx=(20,0), pady=(0, 10), sticky=W + E)

            self.control_win.ExitButton.grid(row=9, column=1, pady=(20,0))



    def configure_window(self):


        def on_closing_configure():
            self.queue_out.put("END")
            try:
                self.configure_win.destroy()
                self.configure_window_open = False
            except Exception as e:
                self.logger.error(str(e))

        if not self.configure_window_open:

            self.configure_win = Tk()
            self.configure_window_open = True
            self.configure_win.title("Configure System Parameters")
            self.configure_win.configure(bg="Black")
            self.configure_win.geometry("1024x600")
            self.configure_win.protocol("WM_DELETE_WINDOW", on_closing_configure)


            self.configure_win.Soilmoisture_thresholds = [None, None]
            self.configure_win.Temperature_thresholds = [None, None]
            self.configure_win.Humidity_thresholds = [None, None]
            self.configure_win.VOC_thresholds = [None, None]
            self.configure_win.UV_settings = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,  None, None, None, None, None, None, None, None, None]
            self.configure_win.Red_settings = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
            self.configure_win.Green_settings = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
            self.configure_win.Blue_settings = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

            self.configure_win.GrowSpaceTitle = Label(self.configure_win, bg="Black", fg="White", text="Grow Space", font="Helvetica 24 bold italic")


            #Environmental Parameter Labels and Entries


            self.configure_win.EnvironmentalParametersHeader = Label(self.configure_win, bg="Black", fg="White", text="Environmental Parameters", font="Helvetica 18 bold")
            self.configure_win.SoilMoistureConfigureLabel = Label(self.configure_win, bg="Black", fg="White", text="Soil Moisture [%]", font="Helvetica 18")
            self.configure_win.TemperatureConfigureLabel = Label(self.configure_win, bg="Black", fg="White", text="Temperature [°C] ", font="Helvetica 18")
            self.configure_win.HumidityConfigureLabel = Label(self.configure_win, bg="Black", fg="White", text="Humidity [%]", font="Helvetica 18")
            self.configure_win.VOCConfigureLabel = Label(self.configure_win, bg="Black", fg="White", text="VOC [kΩ]", font="Helvetica 18")
            self.configure_win.MinimumValue = Label(self.configure_win, bg="Black", fg="White", text="Minimum", font="Helvetica 18")
            self.configure_win.MaximumValue = Label(self.configure_win, bg="Black", fg="White", text="Maximum", font="Helvetica 18")

            self.configure_win.SoilMoistureMinEntry = Entry(self.configure_win, width = 4, bg="Gray85",textvariable=self.configure_win.Soilmoisture_thresholds[0])
            self.configure_win.SoilMoistureMaxEntry = Entry(self.configure_win, width = 4, bg="Gray85",textvariable=self.configure_win.Soilmoisture_thresholds[1])
            self.configure_win.TemperatureMinEntry = Entry(self.configure_win, width = 4, bg="Gray85",textvariable=self.configure_win.Temperature_thresholds[0])
            self.configure_win.TemperatureMaxEntry = Entry(self.configure_win, width = 4, bg="Gray85",textvariable=self.configure_win.Temperature_thresholds[1])
            self.configure_win.HumidityMinEntry = Entry(self.configure_win, width = 4, bg="Gray85",textvariable=self.configure_win.Humidity_thresholds[0])
            self.configure_win.HumidityMaxEntry = Entry(self.configure_win, width = 4, bg="Gray85",textvariable=self.configure_win.Humidity_thresholds[1])
            self.configure_win.VOCMinEntry = Entry(self.configure_win, width = 4, bg="Gray85",textvariable=self.configure_win.VOC_thresholds[0])
            self.configure_win.VOCMaxEntry = Entry(self.configure_win, width = 4, bg="Gray85",textvariable=self.configure_win.VOC_thresholds[1])

            # Lighting Labels and Entries

            self.configure_win.LightingParametersHeader = Label(self.configure_win, bg="Black", fg="White", text="Lighting Levels", font="Helvetica 18 bold")
            self.configure_win.UVConfigureLabel = Label(self.configure_win, bg="Black", fg="MediumPurple1", text="UV", font="Helvetica 18 bold")
            self.configure_win.RedConfigureLabel = Label(self.configure_win, bg="Black", fg="Red", text="R", font="Helvetica 18 bold")
            self.configure_win.GreenConfigureLabel = Label(self.configure_win, bg="Black", fg="Green2", text="G", font="Helvetica 18 bold")
            self.configure_win.BlueConfigureLabel = Label(self.configure_win, bg="Black", fg="Deep Sky Blue", text="B", font="Helvetica 18 bold")

            self.configure_win.Hour00Label = Label(self.configure_win, bg="Black", fg="White", text="00", font="Helvetica 18")
            self.configure_win.Hour01Label = Label(self.configure_win, bg="Black", fg="White", text="01", font="Helvetica 18")
            self.configure_win.Hour02Label = Label(self.configure_win, bg="Black", fg="White", text="02", font="Helvetica 18")
            self.configure_win.Hour03Label = Label(self.configure_win, bg="Black", fg="White", text="03", font="Helvetica 18")
            self.configure_win.Hour04Label = Label(self.configure_win, bg="Black", fg="White", text="04", font="Helvetica 18")
            self.configure_win.Hour05Label = Label(self.configure_win, bg="Black", fg="White", text="05", font="Helvetica 18")
            self.configure_win.Hour06Label = Label(self.configure_win, bg="Black", fg="White", text="06", font="Helvetica 18")
            self.configure_win.Hour07Label = Label(self.configure_win, bg="Black", fg="White", text="07", font="Helvetica 18")
            self.configure_win.Hour08Label = Label(self.configure_win, bg="Black", fg="White", text="08", font="Helvetica 18")
            self.configure_win.Hour09Label = Label(self.configure_win, bg="Black", fg="White", text="09", font="Helvetica 18")
            self.configure_win.Hour10Label = Label(self.configure_win, bg="Black", fg="White", text="10", font="Helvetica 18")
            self.configure_win.Hour11Label = Label(self.configure_win, bg="Black", fg="White", text="11", font="Helvetica 18")
            self.configure_win.Hour12Label = Label(self.configure_win, bg="Black", fg="White", text="12", font="Helvetica 18")
            self.configure_win.Hour13Label = Label(self.configure_win, bg="Black", fg="White", text="13", font="Helvetica 18")
            self.configure_win.Hour14Label = Label(self.configure_win, bg="Black", fg="White", text="14", font="Helvetica 18")
            self.configure_win.Hour15Label = Label(self.configure_win, bg="Black", fg="White", text="15", font="Helvetica 18")
            self.configure_win.Hour16Label = Label(self.configure_win, bg="Black", fg="White", text="16", font="Helvetica 18")
            self.configure_win.Hour17Label = Label(self.configure_win, bg="Black", fg="White", text="17", font="Helvetica 18")
            self.configure_win.Hour18Label = Label(self.configure_win, bg="Black", fg="White", text="18", font="Helvetica 18")
            self.configure_win.Hour19Label = Label(self.configure_win, bg="Black", fg="White", text="19", font="Helvetica 18")
            self.configure_win.Hour20Label = Label(self.configure_win, bg="Black", fg="White", text="20", font="Helvetica 18")
            self.configure_win.Hour21Label = Label(self.configure_win, bg="Black", fg="White", text="21", font="Helvetica 18")
            self.configure_win.Hour22Label = Label(self.configure_win, bg="Black", fg="White", text="22", font="Helvetica 18")
            self.configure_win.Hour23Label = Label(self.configure_win, bg="Black", fg="White", text="23", font="Helvetica 18")



            self.configure_win.UVEntry00 = Entry(self.configure_win, width = 3, bg="Gray85", textvariable=self.configure_win.UV_settings[0])
            self.configure_win.UVEntry01 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[1])
            self.configure_win.UVEntry02 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[2])
            self.configure_win.UVEntry03 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[3])
            self.configure_win.UVEntry04 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[4])
            self.configure_win.UVEntry05 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[5])
            self.configure_win.UVEntry06 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[6])
            self.configure_win.UVEntry07 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[7])
            self.configure_win.UVEntry08 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[8])
            self.configure_win.UVEntry09 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[9])
            self.configure_win.UVEntry10 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[10])
            self.configure_win.UVEntry11 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[11])
            self.configure_win.UVEntry12 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[12])
            self.configure_win.UVEntry13 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[13])
            self.configure_win.UVEntry14 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[14])
            self.configure_win.UVEntry15 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[15])
            self.configure_win.UVEntry16 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[16])
            self.configure_win.UVEntry17 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[17])
            self.configure_win.UVEntry18 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[18])
            self.configure_win.UVEntry19 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[19])
            self.configure_win.UVEntry20 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[20])
            self.configure_win.UVEntry21 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[21])
            self.configure_win.UVEntry22 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[22])
            self.configure_win.UVEntry23 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.UV_settings[23])

            self.configure_win.RedEntry00 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[0])
            self.configure_win.RedEntry01 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[1])
            self.configure_win.RedEntry02 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[2])
            self.configure_win.RedEntry03 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[3])
            self.configure_win.RedEntry04 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[4])
            self.configure_win.RedEntry05 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[5])
            self.configure_win.RedEntry06 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[6])
            self.configure_win.RedEntry07 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[7])
            self.configure_win.RedEntry08 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[8])
            self.configure_win.RedEntry09 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[9])
            self.configure_win.RedEntry10 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[10])
            self.configure_win.RedEntry11 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[11])
            self.configure_win.RedEntry12 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[12])
            self.configure_win.RedEntry13 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[13])
            self.configure_win.RedEntry14 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[14])
            self.configure_win.RedEntry15 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[15])
            self.configure_win.RedEntry16 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[16])
            self.configure_win.RedEntry17 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[17])
            self.configure_win.RedEntry18 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[18])
            self.configure_win.RedEntry19 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[19])
            self.configure_win.RedEntry20 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[20])
            self.configure_win.RedEntry21 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[21])
            self.configure_win.RedEntry22 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[22])
            self.configure_win.RedEntry23 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Red_settings[23])

            self.configure_win.GreenEntry00 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[0])
            self.configure_win.GreenEntry01 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[1])
            self.configure_win.GreenEntry02 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[2])
            self.configure_win.GreenEntry03 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[3])
            self.configure_win.GreenEntry04 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[4])
            self.configure_win.GreenEntry05 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[5])
            self.configure_win.GreenEntry06 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[6])
            self.configure_win.GreenEntry07 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[7])
            self.configure_win.GreenEntry08 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[8])
            self.configure_win.GreenEntry09 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[9])
            self.configure_win.GreenEntry10 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[10])
            self.configure_win.GreenEntry11 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[11])
            self.configure_win.GreenEntry12 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[12])
            self.configure_win.GreenEntry13 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[13])
            self.configure_win.GreenEntry14 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[14])
            self.configure_win.GreenEntry15 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[15])
            self.configure_win.GreenEntry16 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[16])
            self.configure_win.GreenEntry17 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[17])
            self.configure_win.GreenEntry18 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[18])
            self.configure_win.GreenEntry19 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[19])
            self.configure_win.GreenEntry20 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[20])
            self.configure_win.GreenEntry21 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[21])
            self.configure_win.GreenEntry22 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[22])
            self.configure_win.GreenEntry23 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Green_settings[23])

            self.configure_win.BlueEntry00 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[0])
            self.configure_win.BlueEntry01 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[1])
            self.configure_win.BlueEntry02 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[2])
            self.configure_win.BlueEntry03 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[3])
            self.configure_win.BlueEntry04 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[4])
            self.configure_win.BlueEntry05 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[5])
            self.configure_win.BlueEntry06 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[6])
            self.configure_win.BlueEntry07 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[7])
            self.configure_win.BlueEntry08 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[8])
            self.configure_win.BlueEntry09 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[9])
            self.configure_win.BlueEntry10 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[10])
            self.configure_win.BlueEntry11 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[11])
            self.configure_win.BlueEntry12 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[12])
            self.configure_win.BlueEntry13 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[13])
            self.configure_win.BlueEntry14 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[14])
            self.configure_win.BlueEntry15 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[15])
            self.configure_win.BlueEntry16 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[16])
            self.configure_win.BlueEntry17 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[17])
            self.configure_win.BlueEntry18 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[18])
            self.configure_win.BlueEntry19 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[19])
            self.configure_win.BlueEntry20 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[20])
            self.configure_win.BlueEntry21 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[21])
            self.configure_win.BlueEntry22 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[22])
            self.configure_win.BlueEntry23 = Entry(self.configure_win, width = 3, bg="Gray85",textvariable=self.configure_win.Blue_settings[23])

            #####################Defining Buttons###############################

            self.configure_win.BackButton = Button(self.configure_win, bg="White", fg="Black", text="BACK", font="Helvetica 24 bold", command=on_closing_configure)
            self.configure_win.ConfigureButton = Button(self.configure_win, bg="White", fg="Black", text="CONFIGURE", font="Helvetica 24 bold", command=None)
            ####################Placing Widgets##################################

            self.configure_win.GrowSpaceTitle.grid(row=1, column=0, columnspan=12, padx=(10,0), sticky=W)

            self.configure_win.EnvironmentalParametersHeader.grid(row=4, column=0, columnspan=12, padx=(10,0), pady=(10,20), sticky=W)

            # Placing Environmental Labels
            self.configure_win.MinimumValue.grid(row=9, column=14, columnspan=3, sticky=W+E)
            self.configure_win.MaximumValue.grid(row=9, column=17, columnspan=3, sticky=W+E)
            self.configure_win.SoilMoistureConfigureLabel.grid(row=10, column=9, columnspan=6, sticky=W)
            self.configure_win.TemperatureConfigureLabel.grid(row=11, column=9, columnspan=6, sticky=W)
            self.configure_win.HumidityConfigureLabel.grid(row=12, column=9, columnspan=6, sticky=W)
            self.configure_win.VOCConfigureLabel.grid(row=13, column=9, columnspan=6, pady=(0,20), sticky=W)

            #Placing Environmental Entries
            self.configure_win.SoilMoistureMinEntry.grid(row=10, column=14, columnspan=2, sticky= E)
            self.configure_win.TemperatureMinEntry.grid(row=11, column=14, columnspan=2, sticky=E)
            self.configure_win.HumidityMinEntry.grid(row=12, column=14, columnspan=2, sticky=E)
            self.configure_win.VOCMinEntry.grid(row=13, column=14, columnspan=2, pady=(0,20), sticky=E)

            self.configure_win.SoilMoistureMaxEntry.grid(row=10, column=17, columnspan=2, sticky=E)
            self.configure_win.TemperatureMaxEntry.grid(row=11, column=17, columnspan=2, sticky=E)
            self.configure_win.HumidityMaxEntry.grid(row=12, column=17, columnspan=2, sticky=E)
            self.configure_win.VOCMaxEntry.grid(row=13, column=17, columnspan=2, pady=(0, 20), sticky=E)

            # Placing Lighting Labels
            self.configure_win.LightingParametersHeader.grid(row=20, column=0, columnspan=12, padx=(10,0), pady=(0,10), sticky=W)
            self.configure_win.UVConfigureLabel.grid(row=22, column=1, padx=(10,10),sticky=W+E)
            self.configure_win.RedConfigureLabel.grid(row=23, column=1, padx=(10,10), sticky=W+E)
            self.configure_win.GreenConfigureLabel.grid(row=24, column=1, padx=(10,10), sticky=W+E)
            self.configure_win.BlueConfigureLabel.grid(row=25, column=1, padx=(10,10), sticky=W+E)


            x=3;
            self.configure_win.Hour00Label.grid(row=21, column=x, sticky=W+E)
            self.configure_win.Hour01Label.grid(row=21, column=x+1, sticky=W+E)
            self.configure_win.Hour02Label.grid(row=21, column=x+2, sticky=W+E)
            self.configure_win.Hour03Label.grid(row=21, column=x+3, sticky=W+E)
            self.configure_win.Hour04Label.grid(row=21, column=x+4, sticky=W+E)
            self.configure_win.Hour05Label.grid(row=21, column=x+5, sticky=W+E)
            self.configure_win.Hour06Label.grid(row=21, column=x+6, sticky=W+E)
            self.configure_win.Hour07Label.grid(row=21, column=x+7, sticky=W+E)
            self.configure_win.Hour08Label.grid(row=21, column=x+8, sticky=W+E)
            self.configure_win.Hour09Label.grid(row=21, column=x+9, sticky=W+E)
            self.configure_win.Hour10Label.grid(row=21, column=x+10, sticky=W+E)
            self.configure_win.Hour11Label.grid(row=21, column=x+11, sticky=W+E)
            self.configure_win.Hour12Label.grid(row=21, column=x+12, sticky=W+E)
            self.configure_win.Hour13Label.grid(row=21, column=x+13, sticky=W+E)
            self.configure_win.Hour14Label.grid(row=21, column=x+14, sticky=W+E)
            self.configure_win.Hour15Label.grid(row=21, column=x+15, sticky=W+E)
            self.configure_win.Hour16Label.grid(row=21, column=x+16, sticky=W+E)
            self.configure_win.Hour17Label.grid(row=21, column=x+17, sticky=W+E)
            self.configure_win.Hour18Label.grid(row=21, column=x+18, sticky=W+E)
            self.configure_win.Hour19Label.grid(row=21, column=x+19, sticky=W+E)
            self.configure_win.Hour20Label.grid(row=21, column=x+20, sticky=W+E)
            self.configure_win.Hour21Label.grid(row=21, column=x+21, sticky=W+E)
            self.configure_win.Hour22Label.grid(row=21, column=x+22, sticky=W+E)
            self.configure_win.Hour23Label.grid(row=21, column=x+23, sticky=W+E)

            #Placing Lighting Entries
            self.configure_win.UVEntry00.grid(row=22, column=x, sticky=W)
            self.configure_win.UVEntry01.grid(row=22, column=x+1, sticky=W)
            self.configure_win.UVEntry02.grid(row=22, column=x+2, sticky=W)
            self.configure_win.UVEntry03.grid(row=22, column=x+3, sticky=W)
            self.configure_win.UVEntry04.grid(row=22, column=x+4, sticky=W)
            self.configure_win.UVEntry05.grid(row=22, column=x+5,sticky=W)
            self.configure_win.UVEntry06.grid(row=22, column=x+6, sticky=W)
            self.configure_win.UVEntry07.grid(row=22, column=x+7, sticky=W)
            self.configure_win.UVEntry08.grid(row=22, column=x+8, sticky=W)
            self.configure_win.UVEntry09.grid(row=22, column=x+9, sticky=W)
            self.configure_win.UVEntry10.grid(row=22, column=x+10, sticky=W)
            self.configure_win.UVEntry11.grid(row=22, column=x+11, sticky=W)
            self.configure_win.UVEntry12.grid(row=22, column=x+12, sticky=W)
            self.configure_win.UVEntry13.grid(row=22, column=x+13, sticky=W)
            self.configure_win.UVEntry14.grid(row=22, column=x+14, sticky=W)
            self.configure_win.UVEntry15.grid(row=22, column=x+15, sticky=W)
            self.configure_win.UVEntry16.grid(row=22, column=x+16, sticky=W)
            self.configure_win.UVEntry17.grid(row=22, column=x+17, sticky=W)
            self.configure_win.UVEntry18.grid(row=22, column=x+18, sticky=W)
            self.configure_win.UVEntry19.grid(row=22, column=x+19, sticky=W)
            self.configure_win.UVEntry20.grid(row=22, column=x+20, sticky=W)
            self.configure_win.UVEntry21.grid(row=22, column=x+21, sticky=W)
            self.configure_win.UVEntry22.grid(row=22, column=x+22, sticky=W)
            self.configure_win.UVEntry23.grid(row=22, column=x+23, sticky=W)

            self.configure_win.RedEntry00.grid(row=23, column=x, sticky=W)
            self.configure_win.RedEntry01.grid(row=23, column=x + 1, sticky=W)
            self.configure_win.RedEntry02.grid(row=23, column=x + 2, sticky=W)
            self.configure_win.RedEntry03.grid(row=23, column=x + 3, sticky=W)
            self.configure_win.RedEntry04.grid(row=23, column=x + 4, sticky=W)
            self.configure_win.RedEntry05.grid(row=23, column=x + 5, sticky=W)
            self.configure_win.RedEntry06.grid(row=23, column=x + 6, sticky=W)
            self.configure_win.RedEntry07.grid(row=23, column=x + 7, sticky=W)
            self.configure_win.RedEntry08.grid(row=23, column=x + 8, sticky=W)
            self.configure_win.RedEntry09.grid(row=23, column=x + 9, sticky=W)
            self.configure_win.RedEntry10.grid(row=23, column=x + 10, sticky=W)
            self.configure_win.RedEntry11.grid(row=23, column=x + 11, sticky=W)
            self.configure_win.RedEntry12.grid(row=23, column=x + 12, sticky=W)
            self.configure_win.RedEntry13.grid(row=23, column=x + 13, sticky=W)
            self.configure_win.RedEntry14.grid(row=23, column=x + 14, sticky=W)
            self.configure_win.RedEntry15.grid(row=23, column=x + 15, sticky=W)
            self.configure_win.RedEntry16.grid(row=23, column=x + 16, sticky=W)
            self.configure_win.RedEntry17.grid(row=23, column=x + 17, sticky=W)
            self.configure_win.RedEntry18.grid(row=23, column=x + 18, sticky=W)
            self.configure_win.RedEntry19.grid(row=23, column=x + 19, sticky=W)
            self.configure_win.RedEntry20.grid(row=23, column=x + 20, sticky=W)
            self.configure_win.RedEntry21.grid(row=23, column=x + 21, sticky=W)
            self.configure_win.RedEntry22.grid(row=23, column=x + 22, sticky=W)
            self.configure_win.RedEntry23.grid(row=23, column=x + 23, sticky=W)

            self.configure_win.GreenEntry00.grid(row=24, column=x, sticky=W)
            self.configure_win.GreenEntry01.grid(row=24, column=x + 1, sticky=W)
            self.configure_win.GreenEntry02.grid(row=24, column=x + 2, sticky=W)
            self.configure_win.GreenEntry03.grid(row=24, column=x + 3, sticky=W)
            self.configure_win.GreenEntry04.grid(row=24, column=x + 4, sticky=W)
            self.configure_win.GreenEntry05.grid(row=24, column=x + 5, sticky=W)
            self.configure_win.GreenEntry06.grid(row=24, column=x + 6, sticky=W)
            self.configure_win.GreenEntry07.grid(row=24, column=x + 7, sticky=W)
            self.configure_win.GreenEntry08.grid(row=24, column=x + 8, sticky=W)
            self.configure_win.GreenEntry09.grid(row=24, column=x + 9, sticky=W)
            self.configure_win.GreenEntry10.grid(row=24, column=x + 10, sticky=W)
            self.configure_win.GreenEntry11.grid(row=24, column=x + 11, sticky=W)
            self.configure_win.GreenEntry12.grid(row=24, column=x + 12, sticky=W)
            self.configure_win.GreenEntry13.grid(row=24, column=x + 13, sticky=W)
            self.configure_win.GreenEntry14.grid(row=24, column=x + 14, sticky=W)
            self.configure_win.GreenEntry15.grid(row=24, column=x + 15, sticky=W)
            self.configure_win.GreenEntry16.grid(row=24, column=x + 16, sticky=W)
            self.configure_win.GreenEntry17.grid(row=24, column=x + 17, sticky=W)
            self.configure_win.GreenEntry18.grid(row=24, column=x + 18, sticky=W)
            self.configure_win.GreenEntry19.grid(row=24, column=x + 19, sticky=W)
            self.configure_win.GreenEntry20.grid(row=24, column=x + 20, sticky=W)
            self.configure_win.GreenEntry21.grid(row=24, column=x + 21, sticky=W)
            self.configure_win.GreenEntry22.grid(row=24, column=x + 22, sticky=W)
            self.configure_win.GreenEntry23.grid(row=24, column=x + 23, sticky=W)

            self.configure_win.BlueEntry00.grid(row=25, column=x, sticky=W)
            self.configure_win.BlueEntry01.grid(row=25, column=x + 1, sticky=W)
            self.configure_win.BlueEntry02.grid(row=25, column=x + 2, sticky=W)
            self.configure_win.BlueEntry03.grid(row=25, column=x + 3, sticky=W)
            self.configure_win.BlueEntry04.grid(row=25, column=x + 4, sticky=W)
            self.configure_win.BlueEntry05.grid(row=25, column=x + 5, sticky=W)
            self.configure_win.BlueEntry06.grid(row=25, column=x + 6, sticky=W)
            self.configure_win.BlueEntry07.grid(row=25, column=x + 7, sticky=W)
            self.configure_win.BlueEntry08.grid(row=25, column=x + 8, sticky=W)
            self.configure_win.BlueEntry09.grid(row=25, column=x + 9, sticky=W)
            self.configure_win.BlueEntry10.grid(row=25, column=x + 10, sticky=W)
            self.configure_win.BlueEntry11.grid(row=25, column=x + 11, sticky=W)
            self.configure_win.BlueEntry12.grid(row=25, column=x + 12, sticky=W)
            self.configure_win.BlueEntry13.grid(row=25, column=x + 13, sticky=W)
            self.configure_win.BlueEntry14.grid(row=25, column=x + 14, sticky=W)
            self.configure_win.BlueEntry15.grid(row=25, column=x + 15, sticky=W)
            self.configure_win.BlueEntry16.grid(row=25, column=x + 16, sticky=W)
            self.configure_win.BlueEntry17.grid(row=25, column=x + 17, sticky=W)
            self.configure_win.BlueEntry18.grid(row=25, column=x + 18, sticky=W)
            self.configure_win.BlueEntry19.grid(row=25, column=x + 19, sticky=W)
            self.configure_win.BlueEntry20.grid(row=25, column=x + 20, sticky=W)
            self.configure_win.BlueEntry21.grid(row=25, column=x + 21, sticky=W)
            self.configure_win.BlueEntry22.grid(row=25, column=x + 22, sticky=W)
            self.configure_win.BlueEntry23.grid(row=25, column=x + 23, sticky=W)


            self.configure_win.BackButton.grid(row = 26, column = 11, columnspan=4, pady=(40,0), command=None)
            self.configure_win.ConfigureButton.grid(row=26, column=15, columnspan=4, pady=(40, 0), command=None)





    def process_incoming(self):
        """! 
        Receive data from the incoming queue (from the main process)
        """

        while not self.queue_in.empty():
            msg = self.queue_in.get()

            # Print whatever it receives from the main thread
            self.logger.info("GUI: Received data from " +str(msg[0]) + ": " + str(msg[1]))

            if isinstance(msg[0], str):
                # Display the data accordingly
                if msg[0] == "soil_moisture_sensor":
                    self.SoilMoistureCondition_value.configure(text=str(msg[1])+"%")
                    if msg[2] is not None:
                        self.SoilMoistureCondition_value.config(fg="Red")
                        self.SoilMoistureStatus_value.configure(text=msg[2])
                    else:
                        self.SoilMoistureCondition_value.config(fg="Green")
                        self.SoilMoistureStatus_value.configure(text="OK")

                elif msg[0] == "environment_sensor":
                    # Update temperature
                    received_temp = round(msg[1]['temperature']['value'], 2)
                    self.TemperatureCondition_value.configure(text=str(received_temp)+"°C")
                    if msg[1]['temperature']['flag'] is not None:
                        self.TemperatureCondition_value.config(fg="Red")
                        self.TemperatureStatus_value.configure(text=msg[1]['temperature']['flag'])
                    else:
                        self.TemperatureCondition_value.config(fg="Green")
                        self.TemperatureStatus_value.configure(text="OK")

                    # Update humidity
                    received_humidity = round(msg[1]['humidity']['value'], 2)
                    self.HumidityCondition_value.configure(text=str(received_humidity)+"%")
                    if msg[1]['humidity']['flag'] is not None:
                        self.HumidityCondition_value.config(fg="Red")
                        self.HumidityStatus_value.configure(text=msg[1]['humidity']['flag'])
                    else:
                        self.HumidityCondition_value.config(fg="Green")
                        self.HumidityStatus_value.configure(text="OK")

                    # Update VOC
                    received_gas = round(msg[1]['gas']['value'], 2)
                    self.VOCCondition_value.configure(text=str(received_gas)+"kΩ")
                    if msg[1]['gas']['flag'] is not None:
                        self.VOCCondition_value.config(fg="Red")
                        self.VOCStatus_value.configure(text=msg[1]['gas']['flag'])
                    else:
                        self.VOCCondition_value.config(fg="Green")
                        self.VOCStatus_value.configure(text="OK")

                elif msg[0] == "Pump Status":
                    self.PumpStatus_value.configure(text=msg[1])
                elif msg[0] == "Fan Status":
                    self.FanStatus_value.configure(text=msg[1])
                elif msg[0] == "UV LED Status":
                    self.UVLEDIntensity_value.configure(text=msg[1])
                elif msg[0] == "RGB LED Status":
                    self.RGBLEDIntensity_value.configure(text=str(round(msg[1][0]*(100/255),1)) + "%-" + str(round(msg[1][1]*(100/255),1)) + "%-" + str(round(msg[1][2]*(100/255),1)) + "%")
                else:
                    self.logger.error("Unexpected item passed in main_to_gui queue: " + str(msg))


if __name__ == "__main__":
    ROOT = Tk()
    # ROOT.resizable()
    ROOT.geometry("1024x600")
    endCommand = lambda: sys.exit(0)
    app = GrowSpaceGUI(ROOT, Queue(), Queue(), endCommand)
    ROOT.mainloop() # Blocking!