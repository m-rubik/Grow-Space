"""!
This is the Graphical User Interface (GUI) that the user can use.
The GUI is based on a Tkinter widget.
"""


import sys
import math
from multiprocessing import Queue
from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter import colorchooser
from tkinter import messagebox
from src.utilities.json_utilities import load_from_json, save_as_json
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
        self.createfile_window_open = False
        self.environment_condition_issue = [False, False, False, False, False, False, False, False]

        self.logger = get_logger(name="GUI")
        self.logger.debug("GUI start up.")

        self.master.title("Grow Space")
        self.master.configure(background="Black")
        #self.master.iconbitmap('./icons/Grow-Space-Icon.ico')

        ############################### Declare Labels ####################################################

        self.Title = Label(self.master, bg = "Black", fg = "White", text = "Grow Space", font = "Helvetica 24 bold italic")

        self.EnvironmentalConditionHeader = Label(self.master, bg = "Black", fg = "White", text = "Environmental Conditions", font="Helvetica 24 bold")
        self.SoilMoistureCondition = Label(self.master, bg = "Black", fg = "White", text= "Soil Moisture:",  font = "Helvetica 22")
        self.TemperatureCondition = Label(self.master, bg = "Black", fg = "White", text= "Temperature:",  font = "Helvetica 22")
        self.HumidityCondition = Label(self.master, bg = "Black", fg = "White", text= "Humidity:", font = "Helvetica 22")
        self.VOCCondition = Label(self.master, bg = "Black", fg = "White", text="VOC:",font = "Helvetica 22")

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
        self.SoilMoistureCondition_value = Label(self.master, bg="Black", fg="White", width=7, text=None, font="Helvetica 22")
        self.TemperatureCondition_value  = Label(self.master, bg="Black", fg="White", width=7, text=None, font="Helvetica 22")
        self.HumidityCondition_value  = Label(self.master, bg="Black", fg="White", width=7, text=None, font="Helvetica 22")
        self.VOCCondition_value  = Label(self.master, bg="Black", fg="White", width=7, text=None, font="Helvetica 22")

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
        self.LoadButton = HoverButton(self.master, bg="White", activebackground='grey', fg="Black", text="LOAD", width=7, font="Helvetica 24 bold", command=self.load_file)
        self.PowerButton = HoverButton(self.master, bg="White", activebackground='red', fg="Black", text="\u23FB", font="Helvetica 24 bold", command=endCommand)
        self.CreateFileButton = HoverButton(self.master, bg="White", activebackground='grey', fg="Black", text="CREATE FILE", font="Helvetica 24 bold", command=self.createfile_window)
        self.ControlButton = HoverButton(self.master, bg="White", activebackground='grey', fg="Black", text="CONTROL", font="Helvetica 24 bold", command=self.control_window)

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
        self.LoadButton.grid(row=45, column=10, columnspan=3, sticky=W)
        self.PowerButton.grid(row=45, column=5, columnspan=1, sticky=W+E, padx=(40, 40))
        self.CreateFileButton.grid(row=45, column=22, columnspan=1)
        self.ControlButton.grid(row=45, column=29, columnspan=1)

    ##################### FUNCTIONS ################################################################

    def load_file(self):
        files = [("JSON files", "*.json")]
        config_file = askopenfile(filetypes=files, defaultextension = files)
        if config_file is None: # User closes the dialog with "cancel"
            self.logger.warning("User did not chose a configuration file to load")
        else:
            self.queue_out.put(["RELOAD", (config_file.name.split(".json")[0]).split("configuration_files/")[1]])

    def loadfile_into_config(self):

        files = [("JSON files", "*.json")]
        config_file = askopenfile(filetypes=files, defaultextension = files)
        print(config_file.name)

        if config_file is None: # User closes the dialog with "cancel"
            self.logger.warning("User did not chose a configuration file to load")
        else:
            self.loaded_file = (config_file.name.split(".json")[0]).split("configuration_files/")[1]
            configuration_dict = load_from_json("./configuration_files/" + self.loaded_file)

            # Transfer configuration file data into temporary GUI database
            for item, value in configuration_dict.items():
                self.db_GUI[item] = value




    def save_file(self):
        files = [("JSON files", "*.json")]
        config_file = asksaveasfile(filetypes = files, defaultextension = files)
        if config_file is None: # User closes the dialog with "cancel"
            self.logger.warning("User cancelled configuration file save")
        else:
            # TODO: Obtain the data that they entered in the Entry boxes (that are yet to be made), and format it as
            # a dictionnary (see the main call in src.utilities.json_utilities as an example of how the data should be structured).
            RGB_data = {}
            RGB_data['0'] = {"R": int(self.createfile_win.RedList[0]), "G": int(self.createfile_win.GreenList[0]), "B": int(self.createfile_win.BlueList[0])}
            RGB_data['1'] = {"R": int(self.createfile_win.RedList[1]), "G": int(self.createfile_win.GreenList[1]), "B": int(self.createfile_win.BlueList[1])}
            RGB_data['2'] = {"R": int(self.createfile_win.RedList[2]), "G": int(self.createfile_win.GreenList[2]), "B": int(self.createfile_win.BlueList[2])}
            RGB_data['3'] = {"R": int(self.createfile_win.RedList[3]), "G": int(self.createfile_win.GreenList[3]), "B": int(self.createfile_win.BlueList[3])}
            RGB_data['4'] = {"R": int(self.createfile_win.RedList[4]), "G": int(self.createfile_win.GreenList[4]), "B": int(self.createfile_win.BlueList[4])}
            RGB_data['5'] = {"R": int(self.createfile_win.RedList[5]), "G": int(self.createfile_win.GreenList[5]), "B": int(self.createfile_win.BlueList[5])}
            RGB_data['6'] = {"R": int(self.createfile_win.RedList[6]), "G": int(self.createfile_win.GreenList[6]), "B": int(self.createfile_win.BlueList[6])}
            RGB_data['7'] = {"R": int(self.createfile_win.RedList[7]), "G": int(self.createfile_win.GreenList[7]), "B": int(self.createfile_win.BlueList[7])}
            RGB_data['8'] = {"R": int(self.createfile_win.RedList[8]), "G": int(self.createfile_win.GreenList[8]), "B": int(self.createfile_win.BlueList[8])}
            RGB_data['9'] = {"R": int(self.createfile_win.RedList[9]), "G": int(self.createfile_win.GreenList[9]), "B": int(self.createfile_win.BlueList[9])}
            RGB_data['10'] = {"R": int(self.createfile_win.RedList[10]), "G": int(self.createfile_win.GreenList[10]), "B": int(self.createfile_win.BlueList[10])}
            RGB_data['11'] = {"R": int(self.createfile_win.RedList[11]), "G": int(self.createfile_win.GreenList[11]), "B": int(self.createfile_win.BlueList[11])}
            RGB_data['12'] = {"R": int(self.createfile_win.RedList[12]), "G": int(self.createfile_win.GreenList[12]), "B": int(self.createfile_win.BlueList[12])}
            RGB_data['13'] = {"R": int(self.createfile_win.RedList[13]), "G": int(self.createfile_win.GreenList[13]), "B": int(self.createfile_win.BlueList[13])}
            RGB_data['14'] = {"R": int(self.createfile_win.RedList[14]), "G": int(self.createfile_win.GreenList[14]), "B": int(self.createfile_win.BlueList[14])}
            RGB_data['15'] = {"R": int(self.createfile_win.RedList[15]), "G": int(self.createfile_win.GreenList[15]), "B": int(self.createfile_win.BlueList[15])}
            RGB_data['16'] = {"R": int(self.createfile_win.RedList[16]), "G": int(self.createfile_win.GreenList[16]), "B": int(self.createfile_win.BlueList[16])}
            RGB_data['17'] = {"R": int(self.createfile_win.RedList[17]), "G": int(self.createfile_win.GreenList[17]), "B": int(self.createfile_win.BlueList[17])}
            RGB_data['18'] = {"R": int(self.createfile_win.RedList[18]), "G": int(self.createfile_win.GreenList[18]), "B": int(self.createfile_win.BlueList[18])}
            RGB_data['19'] = {"R": int(self.createfile_win.RedList[19]), "G": int(self.createfile_win.GreenList[19]), "B": int(self.createfile_win.BlueList[19])}
            RGB_data['20'] = {"R": int(self.createfile_win.RedList[20]), "G": int(self.createfile_win.GreenList[20]), "B": int(self.createfile_win.BlueList[20])}
            RGB_data['21'] = {"R": int(self.createfile_win.RedList[21]), "G": int(self.createfile_win.GreenList[21]), "B": int(self.createfile_win.BlueList[21])}
            RGB_data['22'] = {"R": int(self.createfile_win.RedList[22]), "G": int(self.createfile_win.GreenList[22]), "B": int(self.createfile_win.BlueList[22])}
            RGB_data['23'] = {"R": int(self.createfile_win.RedList[23]), "G": int(self.createfile_win.GreenList[23]), "B": int(self.createfile_win.BlueList[23])}


            UV_data = {}
            UV_data['0'] = int(self.createfile_win.UVList[0])
            UV_data['1'] = int(self.createfile_win.UVList[1])
            UV_data['2'] = int(self.createfile_win.UVList[2])
            UV_data['3'] = int(self.createfile_win.UVList[3])
            UV_data['4'] = int(self.createfile_win.UVList[4])
            UV_data['5'] = int(self.createfile_win.UVList[5])
            UV_data['6'] = int(self.createfile_win.UVList[6])
            UV_data['7'] = int(self.createfile_win.UVList[7])
            UV_data['8'] = int(self.createfile_win.UVList[8])
            UV_data['9'] = int(self.createfile_win.UVList[9])
            UV_data['10'] = int(self.createfile_win.UVList[10])
            UV_data['11'] = int(self.createfile_win.UVList[11])
            UV_data['12'] = int(self.createfile_win.UVList[12])
            UV_data['13'] = int(self.createfile_win.UVList[13])
            UV_data['14'] = int(self.createfile_win.UVList[14])
            UV_data['15'] = int(self.createfile_win.UVList[15])
            UV_data['16'] = int(self.createfile_win.UVList[16])
            UV_data['17'] = int(self.createfile_win.UVList[17])
            UV_data['18'] = int(self.createfile_win.UVList[18])
            UV_data['19'] = int(self.createfile_win.UVList[19])
            UV_data['20'] = int(self.createfile_win.UVList[20])
            UV_data['21'] = int(self.createfile_win.UVList[21])
            UV_data['22'] = int(self.createfile_win.UVList[22])
            UV_data['23'] = int(self.createfile_win.UVList[23])


            data = {}
            data['Temperature_Low'] = int(self.createfile_win.TemperatureList[0])
            data['Temperature_High'] = int(self.createfile_win.TemperatureList[1])
            data['Moisture_Low'] = int(self.createfile_win.SoilMoistureList[0])
            data['Moisture_High'] = int(self.createfile_win.SoilMoistureList[1])
            data['Humidity_Low'] = int(self.createfile_win.HumidityList[0])
            data['Humidity_High'] = int(self.createfile_win.HumidityList[1])
            data['VOC_Low'] = int(self.createfile_win.VOCList[0])
            data['VOC_High'] = int(self.createfile_win.VOCList[1])
            data['RGB_data'] = RGB_data
            data['UV_data'] = UV_data
            data['Soak_Minutes'] = 0.5

            filename = "./configuration_files/"+(config_file.name.split(".json")[0]).split("configuration_files/")[1]
            save_as_json(filename, data)

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
            #self.control_win.iconbitmap('./icons/Grow-Space-Icon.ico')


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
            self.control_win.RGBLED_Set = HoverButton(self.control_win, bg = "White", fg="Black", activebackground='grey', text = "SET",font="Helvetica 16 bold", command=lambda: self.queue_out.put([self.control_win.Red_Entry.get(),self.control_win.Green_Entry.get(),self.control_win.Blue_Entry.get()]))
            self.control_win.RGBLED_OFF = HoverButton(self.control_win, bg="White", fg="Black", activebackground='grey', text="OFF", font="Helvetica 16 bold", command=lambda: self.queue_out.put(["0","0","0"]))
            self.control_win.UV_OFF = HoverButton(self.control_win, bg="White", fg="Black", activebackground='grey', text="OFF", font="Helvetica 16 bold", command=lambda: self.queue_out.put("UV OFF"))
            self.control_win.UV_ON = HoverButton(self.control_win, bg="White", fg="Black", activebackground='grey', text="ON",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("UV ON"))
            self.control_win.Fan_OFF = HoverButton(self.control_win, bg="White", fg="Black", activebackground='grey', text="OFF",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("Fan OFF"))
            self.control_win.Fan_ON = HoverButton(self.control_win, bg="White", fg="Black", activebackground='grey', text="ON",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("Fan ON"))
            self.control_win.Pump_OFF = HoverButton(self.control_win, bg="White", fg="Black", activebackground='grey', text="OFF",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("Pump OFF"))
            self.control_win.Pump_ON = HoverButton(self.control_win, bg="White", fg="Black", activebackground='grey', text="ON",  font="Helvetica 16 bold", command=lambda: self.queue_out.put("Pump ON"))
            self.control_win.ExitButton = HoverButton(self.control_win, bg="White", fg="Black", activebackground='red', text="BACK",font="Helvetica 16 bold", command=lambda: (self.queue_out.put("END"), on_closing()))
            self.control_win.ColorWheelButton = HoverButton(self.control_win, bg="White", fg="Black", activebackground='pink', text="Choose",font="Helvetica 16 bold", command=lambda: self.browse_color_wheel())

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
            self.control_win.ColorWheelButton.grid(row=5, column=0, pady=(0,0))

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
            
            
    def browse_color_wheel(self):
        rgb_color, _ = colorchooser.askcolor(parent=self.master, initialcolor=(255, 0, 0))
        if rgb_color is not None:

            self.control_win.Red_Entry.delete(0,END)
            red_value = math.floor(rgb_color[0])
            if red_value == 256:
                red_value == 255
            self.control_win.Red_Entry.insert(0,red_value)

            self.control_win.Green_Entry.delete(0,END)
            green_value = math.floor(rgb_color[1])
            if green_value == 256:
                green_value == 255
            self.control_win.Green_Entry.insert(0,green_value)

            self.control_win.Blue_Entry.delete(0,END)
            blue_value = math.floor(rgb_color[2])
            if blue_value == 256:
                blue_value == 255
            self.control_win.Blue_Entry.insert(0,blue_value)

    def load_into_configuration(self):

        ## Deleting previous entries ##

        self.createfile_win.SoilMoistureMinEntry.delete(0, END)
        self.createfile_win.SoilMoistureMaxEntry.delete(0, END)
        self.createfile_win.TemperatureMinEntry.delete(0, END)
        self.createfile_win.TemperatureMaxEntry.delete(0, END)
        self.createfile_win.HumidityMinEntry.delete(0, END)
        self.createfile_win.HumidityMaxEntry.delete(0, END)
        self.createfile_win.VOCMinEntry.delete(0, END)
        self.createfile_win.VOCMaxEntry.delete(0, END)

        self.createfile_win.UVEntry00.delete(0, END)
        self.createfile_win.UVEntry01.delete(0, END)
        self.createfile_win.UVEntry02.delete(0, END)
        self.createfile_win.UVEntry03.delete(0, END)
        self.createfile_win.UVEntry04.delete(0, END)
        self.createfile_win.UVEntry05.delete(0, END)
        self.createfile_win.UVEntry06.delete(0, END)
        self.createfile_win.UVEntry07.delete(0, END)
        self.createfile_win.UVEntry08.delete(0, END)
        self.createfile_win.UVEntry09.delete(0, END)
        self.createfile_win.UVEntry10.delete(0, END)
        self.createfile_win.UVEntry11.delete(0, END)
        self.createfile_win.UVEntry12.delete(0, END)
        self.createfile_win.UVEntry13.delete(0, END)
        self.createfile_win.UVEntry14.delete(0, END)
        self.createfile_win.UVEntry15.delete(0, END)
        self.createfile_win.UVEntry16.delete(0, END)
        self.createfile_win.UVEntry17.delete(0, END)
        self.createfile_win.UVEntry18.delete(0, END)
        self.createfile_win.UVEntry19.delete(0, END)
        self.createfile_win.UVEntry20.delete(0, END)
        self.createfile_win.UVEntry21.delete(0, END)
        self.createfile_win.UVEntry22.delete(0, END)
        self.createfile_win.UVEntry23.delete(0, END)

        self.createfile_win.RedEntry00.delete(0, END)
        self.createfile_win.RedEntry01.delete(0, END)
        self.createfile_win.RedEntry02.delete(0, END)
        self.createfile_win.RedEntry03.delete(0, END)
        self.createfile_win.RedEntry04.delete(0, END)
        self.createfile_win.RedEntry05.delete(0, END)
        self.createfile_win.RedEntry06.delete(0, END)
        self.createfile_win.RedEntry07.delete(0, END)
        self.createfile_win.RedEntry08.delete(0, END)
        self.createfile_win.RedEntry09.delete(0, END)
        self.createfile_win.RedEntry10.delete(0, END)
        self.createfile_win.RedEntry11.delete(0, END)
        self.createfile_win.RedEntry12.delete(0, END)
        self.createfile_win.RedEntry13.delete(0, END)
        self.createfile_win.RedEntry14.delete(0, END)
        self.createfile_win.RedEntry15.delete(0, END)
        self.createfile_win.RedEntry16.delete(0, END)
        self.createfile_win.RedEntry17.delete(0, END)
        self.createfile_win.RedEntry18.delete(0, END)
        self.createfile_win.RedEntry19.delete(0, END)
        self.createfile_win.RedEntry20.delete(0, END)
        self.createfile_win.RedEntry21.delete(0, END)
        self.createfile_win.RedEntry22.delete(0, END)
        self.createfile_win.RedEntry23.delete(0, END)

        self.createfile_win.GreenEntry00.delete(0, END)
        self.createfile_win.GreenEntry01.delete(0, END)
        self.createfile_win.GreenEntry02.delete(0, END)
        self.createfile_win.GreenEntry03.delete(0, END)
        self.createfile_win.GreenEntry04.delete(0, END)
        self.createfile_win.GreenEntry05.delete(0, END)
        self.createfile_win.GreenEntry06.delete(0, END)
        self.createfile_win.GreenEntry07.delete(0, END)
        self.createfile_win.GreenEntry08.delete(0, END)
        self.createfile_win.GreenEntry09.delete(0, END)
        self.createfile_win.GreenEntry10.delete(0, END)
        self.createfile_win.GreenEntry11.delete(0, END)
        self.createfile_win.GreenEntry12.delete(0, END)
        self.createfile_win.GreenEntry13.delete(0, END)
        self.createfile_win.GreenEntry14.delete(0, END)
        self.createfile_win.GreenEntry15.delete(0, END)
        self.createfile_win.GreenEntry16.delete(0, END)
        self.createfile_win.GreenEntry17.delete(0, END)
        self.createfile_win.GreenEntry18.delete(0, END)
        self.createfile_win.GreenEntry19.delete(0, END)
        self.createfile_win.GreenEntry20.delete(0, END)
        self.createfile_win.GreenEntry21.delete(0, END)
        self.createfile_win.GreenEntry22.delete(0, END)
        self.createfile_win.GreenEntry23.delete(0, END)

        self.createfile_win.BlueEntry00.delete(0, END)
        self.createfile_win.BlueEntry01.delete(0, END)
        self.createfile_win.BlueEntry02.delete(0, END)
        self.createfile_win.BlueEntry03.delete(0, END)
        self.createfile_win.BlueEntry04.delete(0, END)
        self.createfile_win.BlueEntry05.delete(0, END)
        self.createfile_win.BlueEntry06.delete(0, END)
        self.createfile_win.BlueEntry07.delete(0, END)
        self.createfile_win.BlueEntry08.delete(0, END)
        self.createfile_win.BlueEntry09.delete(0, END)
        self.createfile_win.BlueEntry10.delete(0, END)
        self.createfile_win.BlueEntry11.delete(0, END)
        self.createfile_win.BlueEntry12.delete(0, END)
        self.createfile_win.BlueEntry13.delete(0, END)
        self.createfile_win.BlueEntry14.delete(0, END)
        self.createfile_win.BlueEntry15.delete(0, END)
        self.createfile_win.BlueEntry16.delete(0, END)
        self.createfile_win.BlueEntry17.delete(0, END)
        self.createfile_win.BlueEntry18.delete(0, END)
        self.createfile_win.BlueEntry19.delete(0, END)
        self.createfile_win.BlueEntry20.delete(0, END)
        self.createfile_win.BlueEntry21.delete(0, END)
        self.createfile_win.BlueEntry22.delete(0, END)
        self.createfile_win.BlueEntry23.delete(0, END)

        ## Loading appropriate file into GUI database ##

        self.loadfile_into_config()

        ## Inserting values into entries ##

        print(self.db_GUI)




    
    def saving_configuration(self):

        ## Setting lists to equal entries ##

        self.createfile_win.SoilMoistureList = []
        self.createfile_win.TemperatureList = []
        self.createfile_win.HumidityList = []
        self.createfile_win.VOCList = []
        self.createfile_win.RedList = []
        self.createfile_win.GreenList = []
        self.createfile_win.BlueList = []
        self.createfile_win.UVList = []

        self.createfile_win.SoilMoistureList.append(self.createfile_win.SoilMoistureMinEntry.get())
        self.createfile_win.SoilMoistureList.append(self.createfile_win.SoilMoistureMaxEntry.get())
        self.createfile_win.TemperatureList.append(self.createfile_win.TemperatureMinEntry.get())
        self.createfile_win.TemperatureList.append(self.createfile_win.TemperatureMaxEntry.get())
        self.createfile_win.HumidityList.append(self.createfile_win.HumidityMinEntry.get())
        self.createfile_win.HumidityList.append(self.createfile_win.HumidityMaxEntry.get())
        self.createfile_win.VOCList.append(self.createfile_win.VOCMinEntry.get())
        self.createfile_win.VOCList.append(self.createfile_win.VOCMaxEntry.get())

        self.createfile_win.UVList.append(self.createfile_win.UVEntry00.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry01.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry02.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry03.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry04.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry05.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry06.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry07.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry08.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry09.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry10.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry11.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry12.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry13.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry14.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry15.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry16.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry17.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry18.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry19.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry20.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry21.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry22.get())
        self.createfile_win.UVList.append(self.createfile_win.UVEntry23.get())

        self.createfile_win.RedList.append(self.createfile_win.RedEntry00.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry01.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry02.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry03.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry04.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry05.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry06.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry07.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry08.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry09.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry10.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry11.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry12.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry13.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry14.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry15.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry16.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry17.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry18.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry19.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry20.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry21.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry22.get())
        self.createfile_win.RedList.append(self.createfile_win.RedEntry23.get())

        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry00.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry01.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry02.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry03.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry04.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry05.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry06.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry07.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry08.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry09.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry10.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry11.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry12.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry13.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry14.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry15.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry16.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry17.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry18.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry19.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry20.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry21.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry22.get())
        self.createfile_win.GreenList.append(self.createfile_win.GreenEntry23.get())

        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry00.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry01.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry02.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry03.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry04.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry05.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry06.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry07.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry08.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry09.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry10.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry11.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry12.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry13.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry14.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry15.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry16.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry17.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry18.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry19.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry20.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry21.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry22.get())
        self.createfile_win.BlueList.append(self.createfile_win.BlueEntry23.get())

        print(self.createfile_win.SoilMoistureList)

        ## Ensuring all values are correctly inputted ##

        for i in self.createfile_win.SoilMoistureList:
            if i == '' or i.isdigit() == False:
                messagebox.showerror(title="Error - Soil Moisture Values", message="Please enter an integer from 0 to 100 for the soil moisture thresholds", icon="error")
                return

        if any(i > 100 for i in list(map(int, self.createfile_win.SoilMoistureList)))  or any( i < 0 for i in list(map(int, self.createfile_win.SoilMoistureList))):
            messagebox.showerror(title="Error - Soil Moisture Values", message="Please enter an integer from 0 to 100 for the soil moisture thresholds", icon="error")
            return

        if int(self.createfile_win.SoilMoistureList[0]) >= int(self.createfile_win.SoilMoistureList[1]):
            messagebox.showerror(title="Error - Soil Moisture Values", message="Please ensure the soil moisture maximum is greater than the soil moisture minimum", icon="error")
            return


        for i in self.createfile_win.TemperatureList:
            if i == '' or i.isdigit() == False:
                messagebox.showerror(title="Error - Temperature Values", message="Please enter a positive integer for the temperature thresholds", icon="error")
                return

        if  any(i < 0 for i in list(map(int, self.createfile_win.TemperatureList))) < 0:
            messagebox.showerror(title="Error - Temperature Values", message="Please enter a positive integer for the temperature thresholds", icon="error")
            return

        if int(self.createfile_win.TemperatureList[0]) >= int(self.createfile_win.TemperatureList[1]):
            messagebox.showerror(title="Error - Temperature Values", message="Please ensure the temperature maximum is greater than the temperature minimum", icon="error")
            return


        for i in self.createfile_win.HumidityList:
            if i == '' or i.isdigit() == False:
                messagebox.showerror(title="Error - Humidity Values",message="Please enter an integer from 0 to 100 for the humidity thresholds", icon="error")
                return

        if any(i > 100 for i in list(map(int, self.createfile_win.HumidityList))) or any( i < 0 for i in list(map(int, self.createfile_win.HumidityList))):
            messagebox.showerror(title="Error - Humidity Values", message="Please enter an integer from 0 to 100 for the humidity thresholds", icon="error")
            return

        if int(self.createfile_win.HumidityList[0] >= self.createfile_win.HumidityList[1]):
            messagebox.showerror(title="Error - Humidity Values", message="Please ensure the humidity maximum is greater than the humidity minimum", icon="error")
            return

        for i in self.createfile_win.VOCList:
            if i == '' or i.isdigit() == False:
                messagebox.showerror(title="Error - VOC Values", message="Please enter a positive integer for the VOC thresholds", icon="error")
                return

        if  any(i < 0 for i in list(map(int, self.createfile_win.VOCList))):
            messagebox.showerror(title="Error - VOC Values", message="Please enter a positive integer for the VOC thresholds", icon="error")
            return

        if int(self.createfile_win.VOCList[0]) >= int(self.createfile_win.VOCList[1]):
            messagebox.showerror(title="Error - VOC Values", message="Please ensure the VOC maximum is greater than the VOC minimum", icon="error")
            return

        for i in self.createfile_win.UVList:
            if i == '' or i.isdigit() == False:
                messagebox.showerror(title="Error - UV Values", message="Please ensure the UV values are 0 (off) or 1 (on)", icon="error")
                return

        if any(i > 1 for i in list(map(int, self.createfile_win.UVList))) or any(i < 0 for i in list(map(int, self.createfile_win.UVList))):
            messagebox.showerror(title="Error - UV Values", message="Please ensure the UV values are 0 (off) or 1 (on)", icon="error")
            return

        for i in self.createfile_win.RedList:
            if i == '' or i.isdigit() == False:
                messagebox.showerror(title="Error - Red LED Values",message="Please enter an integer from 0 to 255 for the red LED intensities", icon="error")
                return

        if any( i > 255 for i in list(map(int, self.createfile_win.RedList))) or any(i < 0 for i in list(map(int, self.createfile_win.RedList))):
            messagebox.showerror(title="Error - Red LED Values",message="Please enter an integer from 0 to 255 for the red LED intensities", icon="error")
            return

        for i in self.createfile_win.GreenList:
            if i == '' or i.isdigit() == False:
                messagebox.showerror(title="Error - Green LED Values",message="Please enter an integer from 0 to 255 for the green LED intensities", icon="error")
                return

        if any(i > 255 for i in list(map(int, self.createfile_win.GreenList))) or any(i < 0 for i in list(map(int, self.createfile_win.GreenList))):
            messagebox.showerror(title="Error - Green LED Values", message="Please enter an integer from 0 to 255 for the green LED intensities", icon="error")
            return

        for i in self.createfile_win.BlueList:
            if i == '' or i.isdigit() == False:
                messagebox.showerror(title="Error - Blue LED Values",message="Please enter an integer from 0 to 255 for the blue LED intensities", icon="error")
                return

        if any(i > 255 for i in list(map(int, self.createfile_win.BlueList))) or any(i < 0 for i in list(map(int, self.createfile_win.BlueList))):
            messagebox.showerror(title="Error - Blue LED Values",message="Please enter an integer from 0 to 255 for the blue LED intensities", icon="error")
            return

        ##### Verification Box ######
        self.createfile_win.verify = messagebox.askyesno(title="Verify your settings", message= "Are you sure you want to save the above configuration settings?")

        if self.createfile_win.verify == True:
            self.save_file()

        else:
            return


    def createfile_window(self):

        def on_closing_configure():
            try:
                self.createfile_win.destroy()
                self.createfile_window_open = False
            except Exception as e:
                self.logger.error(str(e))

        if not self.createfile_window_open:

            self.createfile_win = Tk()
            self.createfile_window_open = True
            self.createfile_win.title("Configuration File Editor")
            self.createfile_win.configure(bg="Black")
            self.createfile_win.geometry("1024x600")
            self.createfile_win.protocol("WM_DELETE_WINDOW", on_closing_configure)
            #self.createfile_win.iconbitmap('./icons/Grow-Space-Icon.ico')


            self.createfile_win.SoilMoisture_thresholds = [StringVar(), StringVar()]
            self.createfile_win.Temperature_thresholds = [StringVar(), StringVar()]
            self.createfile_win.Humidity_thresholds = [StringVar(), StringVar()]
            self.createfile_win.VOC_thresholds = [StringVar(), StringVar()]
            self.createfile_win.UV_settings = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(),  StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
            self.createfile_win.Red_settings = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
            self.createfile_win.Green_settings = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
            self.createfile_win.Blue_settings = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]

            self.createfile_win.GrowSpaceTitle = Label(self.createfile_win, bg="Black", fg="White", text="Grow Space", font="Helvetica 18 bold italic")


            ## Environmental Parameter Labels and Entries ##


            self.createfile_win.EnvironmentalParametersHeader = Label(self.createfile_win, bg="Black", fg="White", text="Environmental Parameters", font="Helvetica 18 bold")
            self.createfile_win.SoilMoistureConfigureLabel = Label(self.createfile_win, bg="Black", fg="White", text="Soil Moisture [%]", font="Helvetica 18")
            self.createfile_win.TemperatureConfigureLabel = Label(self.createfile_win, bg="Black", fg="White", text="Temperature [°C]", font="Helvetica 18")
            self.createfile_win.HumidityConfigureLabel = Label(self.createfile_win, bg="Black", fg="White", text="Humidity [%]", font="Helvetica 18")
            self.createfile_win.VOCConfigureLabel = Label(self.createfile_win, bg="Black", fg="White", text="VOC [kΩ]", font="Helvetica 18")
            self.createfile_win.MinimumValue = Label(self.createfile_win, bg="Black", fg="White", text="Minimum", font="Helvetica 18")
            self.createfile_win.MaximumValue = Label(self.createfile_win, bg="Black", fg="White", text="Maximum", font="Helvetica 18")

            self.createfile_win.SoilMoistureMinEntry = Entry(self.createfile_win, width = 4, bg="Gray85",textvariable=self.createfile_win.SoilMoisture_thresholds[0])
            self.createfile_win.SoilMoistureMaxEntry = Entry(self.createfile_win, width = 4, bg="Gray85",textvariable=self.createfile_win.SoilMoisture_thresholds[1])
            self.createfile_win.TemperatureMinEntry = Entry(self.createfile_win, width = 4, bg="Gray85",textvariable=self.createfile_win.Temperature_thresholds[0])
            self.createfile_win.TemperatureMaxEntry = Entry(self.createfile_win, width = 4, bg="Gray85",textvariable=self.createfile_win.Temperature_thresholds[1])
            self.createfile_win.HumidityMinEntry = Entry(self.createfile_win, width = 4, bg="Gray85",textvariable=self.createfile_win.Humidity_thresholds[0])
            self.createfile_win.HumidityMaxEntry = Entry(self.createfile_win, width = 4, bg="Gray85",textvariable=self.createfile_win.Humidity_thresholds[1])
            self.createfile_win.VOCMinEntry = Entry(self.createfile_win, width = 4, bg="Gray85",textvariable=self.createfile_win.VOC_thresholds[0])
            self.createfile_win.VOCMaxEntry = Entry(self.createfile_win, width = 4, bg="Gray85",textvariable=self.createfile_win.VOC_thresholds[1])

            ## Lighting Labels and Entries ##

            self.createfile_win.LightingParametersHeader = Label(self.createfile_win, bg="Black", fg="White", text="Lighting Intensities", font="Helvetica 18 bold")
            self.createfile_win.HourLabel = Label(self.createfile_win, bg="Black", fg="White", text="Hour", font="Helvetica 18 bold")
            self.createfile_win.UVConfigureLabel = Label(self.createfile_win, bg="Black", fg="MediumPurple1", text="UV", font="Helvetica 18 bold")
            self.createfile_win.RedConfigureLabel = Label(self.createfile_win, bg="Black", fg="Red", text="R", font="Helvetica 18 bold")
            self.createfile_win.GreenConfigureLabel = Label(self.createfile_win, bg="Black", fg="Green2", text="G", font="Helvetica 18 bold")
            self.createfile_win.BlueConfigureLabel = Label(self.createfile_win, bg="Black", fg="Deep Sky Blue", text="B", font="Helvetica 18 bold")

            self.createfile_win.Hour00Label = Label(self.createfile_win, bg="Black", fg="White", text="00", font="Helvetica 18")
            self.createfile_win.Hour01Label = Label(self.createfile_win, bg="Black", fg="White", text="01", font="Helvetica 18")
            self.createfile_win.Hour02Label = Label(self.createfile_win, bg="Black", fg="White", text="02", font="Helvetica 18")
            self.createfile_win.Hour03Label = Label(self.createfile_win, bg="Black", fg="White", text="03", font="Helvetica 18")
            self.createfile_win.Hour04Label = Label(self.createfile_win, bg="Black", fg="White", text="04", font="Helvetica 18")
            self.createfile_win.Hour05Label = Label(self.createfile_win, bg="Black", fg="White", text="05", font="Helvetica 18")
            self.createfile_win.Hour06Label = Label(self.createfile_win, bg="Black", fg="White", text="06", font="Helvetica 18")
            self.createfile_win.Hour07Label = Label(self.createfile_win, bg="Black", fg="White", text="07", font="Helvetica 18")
            self.createfile_win.Hour08Label = Label(self.createfile_win, bg="Black", fg="White", text="08", font="Helvetica 18")
            self.createfile_win.Hour09Label = Label(self.createfile_win, bg="Black", fg="White", text="09", font="Helvetica 18")
            self.createfile_win.Hour10Label = Label(self.createfile_win, bg="Black", fg="White", text="10", font="Helvetica 18")
            self.createfile_win.Hour11Label = Label(self.createfile_win, bg="Black", fg="White", text="11", font="Helvetica 18")
            self.createfile_win.Hour12Label = Label(self.createfile_win, bg="Black", fg="White", text="12", font="Helvetica 18")
            self.createfile_win.Hour13Label = Label(self.createfile_win, bg="Black", fg="White", text="13", font="Helvetica 18")
            self.createfile_win.Hour14Label = Label(self.createfile_win, bg="Black", fg="White", text="14", font="Helvetica 18")
            self.createfile_win.Hour15Label = Label(self.createfile_win, bg="Black", fg="White", text="15", font="Helvetica 18")
            self.createfile_win.Hour16Label = Label(self.createfile_win, bg="Black", fg="White", text="16", font="Helvetica 18")
            self.createfile_win.Hour17Label = Label(self.createfile_win, bg="Black", fg="White", text="17", font="Helvetica 18")
            self.createfile_win.Hour18Label = Label(self.createfile_win, bg="Black", fg="White", text="18", font="Helvetica 18")
            self.createfile_win.Hour19Label = Label(self.createfile_win, bg="Black", fg="White", text="19", font="Helvetica 18")
            self.createfile_win.Hour20Label = Label(self.createfile_win, bg="Black", fg="White", text="20", font="Helvetica 18")
            self.createfile_win.Hour21Label = Label(self.createfile_win, bg="Black", fg="White", text="21", font="Helvetica 18")
            self.createfile_win.Hour22Label = Label(self.createfile_win, bg="Black", fg="White", text="22", font="Helvetica 18")
            self.createfile_win.Hour23Label = Label(self.createfile_win, bg="Black", fg="White", text="23", font="Helvetica 18")



            self.createfile_win.UVEntry00 = Entry(self.createfile_win, width = 3, bg="Gray85", textvariable=self.createfile_win.UV_settings[0])
            self.createfile_win.UVEntry01 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[1])
            self.createfile_win.UVEntry02 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[2])
            self.createfile_win.UVEntry03 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[3])
            self.createfile_win.UVEntry04 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[4])
            self.createfile_win.UVEntry05 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[5])
            self.createfile_win.UVEntry06 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[6])
            self.createfile_win.UVEntry07 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[7])
            self.createfile_win.UVEntry08 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[8])
            self.createfile_win.UVEntry09 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[9])
            self.createfile_win.UVEntry10 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[10])
            self.createfile_win.UVEntry11 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[11])
            self.createfile_win.UVEntry12 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[12])
            self.createfile_win.UVEntry13 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[13])
            self.createfile_win.UVEntry14 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[14])
            self.createfile_win.UVEntry15 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[15])
            self.createfile_win.UVEntry16 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[16])
            self.createfile_win.UVEntry17 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[17])
            self.createfile_win.UVEntry18 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[18])
            self.createfile_win.UVEntry19 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[19])
            self.createfile_win.UVEntry20 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[20])
            self.createfile_win.UVEntry21 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[21])
            self.createfile_win.UVEntry22 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[22])
            self.createfile_win.UVEntry23 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.UV_settings[23])

            self.createfile_win.RedEntry00 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[0])
            self.createfile_win.RedEntry01 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[1])
            self.createfile_win.RedEntry02 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[2])
            self.createfile_win.RedEntry03 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[3])
            self.createfile_win.RedEntry04 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[4])
            self.createfile_win.RedEntry05 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[5])
            self.createfile_win.RedEntry06 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[6])
            self.createfile_win.RedEntry07 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[7])
            self.createfile_win.RedEntry08 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[8])
            self.createfile_win.RedEntry09 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[9])
            self.createfile_win.RedEntry10 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[10])
            self.createfile_win.RedEntry11 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[11])
            self.createfile_win.RedEntry12 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[12])
            self.createfile_win.RedEntry13 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[13])
            self.createfile_win.RedEntry14 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[14])
            self.createfile_win.RedEntry15 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[15])
            self.createfile_win.RedEntry16 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[16])
            self.createfile_win.RedEntry17 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[17])
            self.createfile_win.RedEntry18 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[18])
            self.createfile_win.RedEntry19 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[19])
            self.createfile_win.RedEntry20 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[20])
            self.createfile_win.RedEntry21 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[21])
            self.createfile_win.RedEntry22 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[22])
            self.createfile_win.RedEntry23 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Red_settings[23])

            self.createfile_win.GreenEntry00 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[0])
            self.createfile_win.GreenEntry01 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[1])
            self.createfile_win.GreenEntry02 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[2])
            self.createfile_win.GreenEntry03 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[3])
            self.createfile_win.GreenEntry04 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[4])
            self.createfile_win.GreenEntry05 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[5])
            self.createfile_win.GreenEntry06 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[6])
            self.createfile_win.GreenEntry07 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[7])
            self.createfile_win.GreenEntry08 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[8])
            self.createfile_win.GreenEntry09 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[9])
            self.createfile_win.GreenEntry10 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[10])
            self.createfile_win.GreenEntry11 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[11])
            self.createfile_win.GreenEntry12 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[12])
            self.createfile_win.GreenEntry13 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[13])
            self.createfile_win.GreenEntry14 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[14])
            self.createfile_win.GreenEntry15 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[15])
            self.createfile_win.GreenEntry16 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[16])
            self.createfile_win.GreenEntry17 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[17])
            self.createfile_win.GreenEntry18 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[18])
            self.createfile_win.GreenEntry19 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[19])
            self.createfile_win.GreenEntry20 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[20])
            self.createfile_win.GreenEntry21 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[21])
            self.createfile_win.GreenEntry22 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[22])
            self.createfile_win.GreenEntry23 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Green_settings[23])

            self.createfile_win.BlueEntry00 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[0])
            self.createfile_win.BlueEntry01 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[1])
            self.createfile_win.BlueEntry02 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[2])
            self.createfile_win.BlueEntry03 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[3])
            self.createfile_win.BlueEntry04 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[4])
            self.createfile_win.BlueEntry05 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[5])
            self.createfile_win.BlueEntry06 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[6])
            self.createfile_win.BlueEntry07 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[7])
            self.createfile_win.BlueEntry08 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[8])
            self.createfile_win.BlueEntry09 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[9])
            self.createfile_win.BlueEntry10 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[10])
            self.createfile_win.BlueEntry11 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[11])
            self.createfile_win.BlueEntry12 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[12])
            self.createfile_win.BlueEntry13 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[13])
            self.createfile_win.BlueEntry14 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[14])
            self.createfile_win.BlueEntry15 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[15])
            self.createfile_win.BlueEntry16 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[16])
            self.createfile_win.BlueEntry17 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[17])
            self.createfile_win.BlueEntry18 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[18])
            self.createfile_win.BlueEntry19 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[19])
            self.createfile_win.BlueEntry20 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[20])
            self.createfile_win.BlueEntry21 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[21])
            self.createfile_win.BlueEntry22 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[22])
            self.createfile_win.BlueEntry23 = Entry(self.createfile_win, width = 3, bg="Gray85",textvariable=self.createfile_win.Blue_settings[23])

            #####################Defining Buttons###############################

            self.createfile_win.BackButton = HoverButton(self.createfile_win, bg="White", fg="Black", activebackground='grey', text="BACK", font="Helvetica 16 bold", command=on_closing_configure)
            self.createfile_win.LoadButton = HoverButton(self.createfile_win, bg="White", fg="Black", activebackground='yellow', text = "LOAD FILE", font="Helvetica 16 bold", command=self.load_into_configuration)
            self.createfile_win.SaveButton = HoverButton(self.createfile_win, bg="White", fg="Black", activebackground='yellow', text="SAVE", font="Helvetica 16 bold", command=self.saving_configuration)
            ####################Placing Widgets##################################

            self.createfile_win.GrowSpaceTitle.grid(row=1, column=0, columnspan=12, padx=(10,0), sticky=W)

            self.createfile_win.EnvironmentalParametersHeader.grid(row=4, column=0, columnspan=12, padx=(10,0), pady=(10,10), sticky=W)

            # Placing Environmental Labels
            self.createfile_win.MinimumValue.grid(row=9, column=12, columnspan=4, padx=(20,0), sticky=W+E)
            self.createfile_win.MaximumValue.grid(row=9, column=17, columnspan=4, padx=(20,0), sticky=W+E)
            self.createfile_win.SoilMoistureConfigureLabel.grid(row=10, column=5, columnspan=6, sticky=E)
            self.createfile_win.TemperatureConfigureLabel.grid(row=11, column=5, columnspan=6, sticky=E)
            self.createfile_win.HumidityConfigureLabel.grid(row=12, column=5, columnspan=6, sticky=E)
            self.createfile_win.VOCConfigureLabel.grid(row=13, column=5, columnspan=6, pady=(0,10), sticky=E)

            #Placing Environmental Entries
            self.createfile_win.SoilMoistureMinEntry.grid(row=10, column=13, columnspan=2, sticky= E)
            self.createfile_win.TemperatureMinEntry.grid(row=11, column=13, columnspan=2, sticky=E)
            self.createfile_win.HumidityMinEntry.grid(row=12, column=13, columnspan=2, sticky=E)
            self.createfile_win.VOCMinEntry.grid(row=13, column=13, columnspan=2, pady=(0,10), sticky=E)

            self.createfile_win.SoilMoistureMaxEntry.grid(row=10, column=18, columnspan=2, sticky=E)
            self.createfile_win.TemperatureMaxEntry.grid(row=11, column=18, columnspan=2, sticky=E)
            self.createfile_win.HumidityMaxEntry.grid(row=12, column=18, columnspan=2, sticky=E)
            self.createfile_win.VOCMaxEntry.grid(row=13, column=18, columnspan=2, pady=(0, 10), sticky=E)

            # Placing Lighting Labels
            self.createfile_win.LightingParametersHeader.grid(row=20, column=0, columnspan=12, padx=(10,0), pady=(0,10), sticky=W)
            self.createfile_win.UVConfigureLabel.grid(row=22, column=0, padx=(10,80),sticky=W+E)
            self.createfile_win.RedConfigureLabel.grid(row=23, column=0, padx=(10,80), sticky=W+E)
            self.createfile_win.GreenConfigureLabel.grid(row=24, column=0, padx=(10,80), sticky=W+E)
            self.createfile_win.BlueConfigureLabel.grid(row=25, column=0, padx=(10,80), sticky=W+E)
            self.createfile_win.HourLabel.grid(row=21, column=0, padx=(10,80),sticky=W+E)

            x=3
            self.createfile_win.Hour00Label.grid(row=21, column=x, sticky=W+E)
            self.createfile_win.Hour01Label.grid(row=21, column=x+1, sticky=W+E)
            self.createfile_win.Hour02Label.grid(row=21, column=x+2, sticky=W+E)
            self.createfile_win.Hour03Label.grid(row=21, column=x+3, sticky=W+E)
            self.createfile_win.Hour04Label.grid(row=21, column=x+4, sticky=W+E)
            self.createfile_win.Hour05Label.grid(row=21, column=x+5, sticky=W+E)
            self.createfile_win.Hour06Label.grid(row=21, column=x+6, sticky=W+E)
            self.createfile_win.Hour07Label.grid(row=21, column=x+7, sticky=W+E)
            self.createfile_win.Hour08Label.grid(row=21, column=x+8, sticky=W+E)
            self.createfile_win.Hour09Label.grid(row=21, column=x+9, sticky=W+E)
            self.createfile_win.Hour10Label.grid(row=21, column=x+10, sticky=W+E)
            self.createfile_win.Hour11Label.grid(row=21, column=x+11, sticky=W+E)
            self.createfile_win.Hour12Label.grid(row=21, column=x+12, sticky=W+E)
            self.createfile_win.Hour13Label.grid(row=21, column=x+13, sticky=W+E)
            self.createfile_win.Hour14Label.grid(row=21, column=x+14, sticky=W+E)
            self.createfile_win.Hour15Label.grid(row=21, column=x+15, sticky=W+E)
            self.createfile_win.Hour16Label.grid(row=21, column=x+16, sticky=W+E)
            self.createfile_win.Hour17Label.grid(row=21, column=x+17, sticky=W+E)
            self.createfile_win.Hour18Label.grid(row=21, column=x+18, sticky=W+E)
            self.createfile_win.Hour19Label.grid(row=21, column=x+19, sticky=W+E)
            self.createfile_win.Hour20Label.grid(row=21, column=x+20, sticky=W+E)
            self.createfile_win.Hour21Label.grid(row=21, column=x+21, sticky=W+E)
            self.createfile_win.Hour22Label.grid(row=21, column=x+22, sticky=W+E)
            self.createfile_win.Hour23Label.grid(row=21, column=x+23, sticky=W+E)

            #Placing Lighting Entries
            self.createfile_win.UVEntry00.grid(row=22, column=x, sticky=W)
            self.createfile_win.UVEntry01.grid(row=22, column=x+1, sticky=W)
            self.createfile_win.UVEntry02.grid(row=22, column=x+2, sticky=W)
            self.createfile_win.UVEntry03.grid(row=22, column=x+3, sticky=W)
            self.createfile_win.UVEntry04.grid(row=22, column=x+4, sticky=W)
            self.createfile_win.UVEntry05.grid(row=22, column=x+5,sticky=W)
            self.createfile_win.UVEntry06.grid(row=22, column=x+6, sticky=W)
            self.createfile_win.UVEntry07.grid(row=22, column=x+7, sticky=W)
            self.createfile_win.UVEntry08.grid(row=22, column=x+8, sticky=W)
            self.createfile_win.UVEntry09.grid(row=22, column=x+9, sticky=W)
            self.createfile_win.UVEntry10.grid(row=22, column=x+10, sticky=W)
            self.createfile_win.UVEntry11.grid(row=22, column=x+11, sticky=W)
            self.createfile_win.UVEntry12.grid(row=22, column=x+12, sticky=W)
            self.createfile_win.UVEntry13.grid(row=22, column=x+13, sticky=W)
            self.createfile_win.UVEntry14.grid(row=22, column=x+14, sticky=W)
            self.createfile_win.UVEntry15.grid(row=22, column=x+15, sticky=W)
            self.createfile_win.UVEntry16.grid(row=22, column=x+16, sticky=W)
            self.createfile_win.UVEntry17.grid(row=22, column=x+17, sticky=W)
            self.createfile_win.UVEntry18.grid(row=22, column=x+18, sticky=W)
            self.createfile_win.UVEntry19.grid(row=22, column=x+19, sticky=W)
            self.createfile_win.UVEntry20.grid(row=22, column=x+20, sticky=W)
            self.createfile_win.UVEntry21.grid(row=22, column=x+21, sticky=W)
            self.createfile_win.UVEntry22.grid(row=22, column=x+22, sticky=W)
            self.createfile_win.UVEntry23.grid(row=22, column=x+23, sticky=W)

            self.createfile_win.RedEntry00.grid(row=23, column=x, sticky=W)
            self.createfile_win.RedEntry01.grid(row=23, column=x + 1, sticky=W)
            self.createfile_win.RedEntry02.grid(row=23, column=x + 2, sticky=W)
            self.createfile_win.RedEntry03.grid(row=23, column=x + 3, sticky=W)
            self.createfile_win.RedEntry04.grid(row=23, column=x + 4, sticky=W)
            self.createfile_win.RedEntry05.grid(row=23, column=x + 5, sticky=W)
            self.createfile_win.RedEntry06.grid(row=23, column=x + 6, sticky=W)
            self.createfile_win.RedEntry07.grid(row=23, column=x + 7, sticky=W)
            self.createfile_win.RedEntry08.grid(row=23, column=x + 8, sticky=W)
            self.createfile_win.RedEntry09.grid(row=23, column=x + 9, sticky=W)
            self.createfile_win.RedEntry10.grid(row=23, column=x + 10, sticky=W)
            self.createfile_win.RedEntry11.grid(row=23, column=x + 11, sticky=W)
            self.createfile_win.RedEntry12.grid(row=23, column=x + 12, sticky=W)
            self.createfile_win.RedEntry13.grid(row=23, column=x + 13, sticky=W)
            self.createfile_win.RedEntry14.grid(row=23, column=x + 14, sticky=W)
            self.createfile_win.RedEntry15.grid(row=23, column=x + 15, sticky=W)
            self.createfile_win.RedEntry16.grid(row=23, column=x + 16, sticky=W)
            self.createfile_win.RedEntry17.grid(row=23, column=x + 17, sticky=W)
            self.createfile_win.RedEntry18.grid(row=23, column=x + 18, sticky=W)
            self.createfile_win.RedEntry19.grid(row=23, column=x + 19, sticky=W)
            self.createfile_win.RedEntry20.grid(row=23, column=x + 20, sticky=W)
            self.createfile_win.RedEntry21.grid(row=23, column=x + 21, sticky=W)
            self.createfile_win.RedEntry22.grid(row=23, column=x + 22, sticky=W)
            self.createfile_win.RedEntry23.grid(row=23, column=x + 23, sticky=W)

            self.createfile_win.GreenEntry00.grid(row=24, column=x, sticky=W)
            self.createfile_win.GreenEntry01.grid(row=24, column=x + 1, sticky=W)
            self.createfile_win.GreenEntry02.grid(row=24, column=x + 2, sticky=W)
            self.createfile_win.GreenEntry03.grid(row=24, column=x + 3, sticky=W)
            self.createfile_win.GreenEntry04.grid(row=24, column=x + 4, sticky=W)
            self.createfile_win.GreenEntry05.grid(row=24, column=x + 5, sticky=W)
            self.createfile_win.GreenEntry06.grid(row=24, column=x + 6, sticky=W)
            self.createfile_win.GreenEntry07.grid(row=24, column=x + 7, sticky=W)
            self.createfile_win.GreenEntry08.grid(row=24, column=x + 8, sticky=W)
            self.createfile_win.GreenEntry09.grid(row=24, column=x + 9, sticky=W)
            self.createfile_win.GreenEntry10.grid(row=24, column=x + 10, sticky=W)
            self.createfile_win.GreenEntry11.grid(row=24, column=x + 11, sticky=W)
            self.createfile_win.GreenEntry12.grid(row=24, column=x + 12, sticky=W)
            self.createfile_win.GreenEntry13.grid(row=24, column=x + 13, sticky=W)
            self.createfile_win.GreenEntry14.grid(row=24, column=x + 14, sticky=W)
            self.createfile_win.GreenEntry15.grid(row=24, column=x + 15, sticky=W)
            self.createfile_win.GreenEntry16.grid(row=24, column=x + 16, sticky=W)
            self.createfile_win.GreenEntry17.grid(row=24, column=x + 17, sticky=W)
            self.createfile_win.GreenEntry18.grid(row=24, column=x + 18, sticky=W)
            self.createfile_win.GreenEntry19.grid(row=24, column=x + 19, sticky=W)
            self.createfile_win.GreenEntry20.grid(row=24, column=x + 20, sticky=W)
            self.createfile_win.GreenEntry21.grid(row=24, column=x + 21, sticky=W)
            self.createfile_win.GreenEntry22.grid(row=24, column=x + 22, sticky=W)
            self.createfile_win.GreenEntry23.grid(row=24, column=x + 23, sticky=W)

            self.createfile_win.BlueEntry00.grid(row=25, column=x, sticky=W)
            self.createfile_win.BlueEntry01.grid(row=25, column=x + 1, sticky=W)
            self.createfile_win.BlueEntry02.grid(row=25, column=x + 2, sticky=W)
            self.createfile_win.BlueEntry03.grid(row=25, column=x + 3, sticky=W)
            self.createfile_win.BlueEntry04.grid(row=25, column=x + 4, sticky=W)
            self.createfile_win.BlueEntry05.grid(row=25, column=x + 5, sticky=W)
            self.createfile_win.BlueEntry06.grid(row=25, column=x + 6, sticky=W)
            self.createfile_win.BlueEntry07.grid(row=25, column=x + 7, sticky=W)
            self.createfile_win.BlueEntry08.grid(row=25, column=x + 8, sticky=W)
            self.createfile_win.BlueEntry09.grid(row=25, column=x + 9, sticky=W)
            self.createfile_win.BlueEntry10.grid(row=25, column=x + 10, sticky=W)
            self.createfile_win.BlueEntry11.grid(row=25, column=x + 11, sticky=W)
            self.createfile_win.BlueEntry12.grid(row=25, column=x + 12, sticky=W)
            self.createfile_win.BlueEntry13.grid(row=25, column=x + 13, sticky=W)
            self.createfile_win.BlueEntry14.grid(row=25, column=x + 14, sticky=W)
            self.createfile_win.BlueEntry15.grid(row=25, column=x + 15, sticky=W)
            self.createfile_win.BlueEntry16.grid(row=25, column=x + 16, sticky=W)
            self.createfile_win.BlueEntry17.grid(row=25, column=x + 17, sticky=W)
            self.createfile_win.BlueEntry18.grid(row=25, column=x + 18, sticky=W)
            self.createfile_win.BlueEntry19.grid(row=25, column=x + 19, sticky=W)
            self.createfile_win.BlueEntry20.grid(row=25, column=x + 20, sticky=W)
            self.createfile_win.BlueEntry21.grid(row=25, column=x + 21, sticky=W)
            self.createfile_win.BlueEntry22.grid(row=25, column=x + 22, sticky=W)
            self.createfile_win.BlueEntry23.grid(row=25, column=x + 23, sticky=W)


            self.createfile_win.BackButton.grid(row = 26, column = 8, columnspan=7, pady=(20,0))
            self.createfile_win.LoadButton.grid(row = 26, column = 12, columnspan = 7, pady=(20,0))
            self.createfile_win.SaveButton.grid(row=26, column=16, columnspan=7, pady=(20, 0))



    def process_incoming(self):
        """!
        Receive data from the incoming queue (from the main process)
        """

        while not self.queue_in.empty():
            msg = self.queue_in.get()

            # Log received data
            self.logger.info("GUI: Received data from " +str(msg[0]) + ": " + str(msg[1]))

            if isinstance(msg[0], str):
                # Update the GUI widgets to display the data accordingly
                if msg[0] == "soil_moisture_sensor":
                    self.SoilMoistureCondition_value.configure(text=str(msg[1])+"%")
                    if msg[2] is not None:
                        self.SoilMoistureCondition_value.config(fg="Red")
                        self.SoilMoistureStatus_value.configure(text=msg[2])
                    else:
                        self.SoilMoistureCondition_value.config(fg="Green")
                        self.SoilMoistureStatus_value.configure(text="OK")

                elif msg[0] == "environment_sensor":
                    received_temp = round(msg[1]['temperature']['value'], 2)
                    self.TemperatureCondition_value.configure(text=str(received_temp)+"°C")
                    if msg[1]['temperature']['flag'] is not None:
                        self.TemperatureCondition_value.config(fg="Red")
                        self.TemperatureStatus_value.configure(text=msg[1]['temperature']['flag'])
                    else:
                        self.TemperatureCondition_value.config(fg="Green")
                        self.TemperatureStatus_value.configure(text="OK")

                    received_humidity = round(msg[1]['humidity']['value'], 2)
                    self.HumidityCondition_value.configure(text=str(received_humidity)+"%")
                    if msg[1]['humidity']['flag'] is not None:
                        self.HumidityCondition_value.config(fg="Red")
                        self.HumidityStatus_value.configure(text=msg[1]['humidity']['flag'])
                    else:
                        self.HumidityCondition_value.config(fg="Green")
                        self.HumidityStatus_value.configure(text="OK")

                    received_gas = int(round(msg[1]['gas']['value']))
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

class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

if __name__ == "__main__":
    ROOT = Tk()
    ROOT.geometry("1024x600")
    endCommand = lambda: sys.exit(0)
    app = GrowSpaceGUI(ROOT, Queue(), Queue(), endCommand)
    ROOT.mainloop() # Blocking!