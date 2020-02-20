"""!
This is the Graphical User Interface (GUI) that the user can use.
The GUI is based on a Tkinter widget.
"""


from multiprocessing import Queue
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, N, S, StringVar
from tkinter.filedialog import askopenfile, asksaveasfile
from src.utilities.json_utilities import save_as_json

import sys
import time
import calendar
import random
import datetime


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
        self.SoilMoistureCondition_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.TemperatureCondition_value  = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.HumidityCondition_value  = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.VOCCondition_value  = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")

        self.SoilMoistureStatus_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.TemperatureStatus_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.HumidityStatus_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.VOCStatus_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")

        self.SoilMoistureRange_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.TemperatureRange_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.HumidityRange_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.VOCRange_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")

        self.PumpStatus_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.FanStatus_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.RGBLEDIntensity_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")
        self.UVLEDIntensity_value = Label(self.master, bg="Black", fg="White", text="-", font="Helvetica 22")


        #Creating Buttons
        self.LoadButton = Button(self.master, bg = "White", fg="Black", text="LOAD", font="Helvetica 24 bold", command=self.load_file)
        self.SaveButton = Button(self.master, bg="White", fg="Black", text="SAVE", font="Helvetica 24 bold", command=self.save_file)
        self.PowerButton = Button(self.master, bg="White", fg="Black", text="\u23FB", font="Helvetica 24 bold", command=endCommand)
        self.ConfigureButton = Button(self.master, bg="White", fg="Black", text="CONFIGURE", font="Helvetica 24 bold", command=None)
        self.ControlButton = Button(self.master, bg="White", fg="Black", text="CONTROL", font="Helvetica 24 bold", command=self.control_window)

        # creates a grid 50 x 50 in the main window
        rows = 0
        while rows < 50:
            self.master.grid_rowconfigure(rows, weight=1, minsize=1)  # Empty Row
            self.master.grid_columnconfigure(rows, weight=1, minsize=1)  # Empty column
            rows += 1

        ##### Positioning elements within the grid ###################

        self.Title.grid(row=0, column=0, columnspan=5, sticky=W)

        #Environmental Conditions
        self.EnvironmentalConditionHeader.grid(row=6, column=5, columnspan=10, sticky=W)
        self.SoilMoistureCondition.grid(row=8, column=5, sticky=W)
        self.TemperatureCondition.grid(row=10, column=5, sticky=W)
        self.HumidityCondition.grid(row=12, column=5, sticky=W)
        self.VOCCondition.grid(row=14, column=5, sticky=W)

        # Condition Values
        self.SoilMoistureCondition_value.grid(row=8, column=11,  sticky=W+E)
        self.TemperatureCondition_value.grid(row=10, column=11,  sticky=W+E)
        self.HumidityCondition_value.grid(row=12, column=11,  sticky=W+E)
        self.VOCCondition_value.grid(row=14, column=11, sticky=W+E)

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
        self.SoilMoistureStatus_value.grid(row=26, column=11, sticky=W+E)
        self.TemperatureStatus_value.grid(row=28, column=11, sticky=W+E)
        self.HumidityStatus_value.grid(row=30, column=11, sticky=W+E)
        self.VOCStatus_value.grid(row=32, column=11, sticky=W+E)

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
        self.LoadButton.grid(row=45, column=5, columnspan=1, sticky=W)
        self.SaveButton.grid(row=45, column=9, columnspan=1, sticky=E)
        self.PowerButton.grid(row=45, column=1, columnspan=1, sticky = W+E)
        self.ConfigureButton.grid(row=45, column=22, columnspan=1)
        self.ControlButton.grid(row=45, column=29, columnspan=1)

    ##################### FUNCTIONS ################################################################

    def load_file(self):
        files = [("JSON files", "*.json")]
        config_file = askopenfile(filetypes=files, defaultextension = files)
        if config_file is None: # User closes the dialog with "cancel"
            print("User did not chose a configuration file to load")
        else:
            self.queue_out.put(["RELOAD", config_file.name.split(".json")[0]])
           
    def save_file(self): 
        files = [("JSON files", "*.json")] 
        config_file = asksaveasfile(filetypes = files, defaultextension = files)
        if config_file is None: # User closes the dialog with "cancel"
            print("User cancelled configuration file save")
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

            save_as_json(config_file.name.split(".json")[0], data)

    def control_window(self):
        self.control_win = Tk()
        self.control_win.title("Control Devices")
        self.control_win.configure(bg="Black")
        self.control_win.geometry("1000x500")

        # creates a grid 50 x 50 in the main window
        rows1 = 0
        while rows1 < 20:
            self.control_win.grid_rowconfigure(rows1, weight=1, minsize=1)  # Empty Row
            self.control_win.grid_columnconfigure(rows1, weight=1, minsize=1)  # Empty column
            rows1 += 1

        self.Red_val = StringVar()
        self.Green_val = StringVar()
        self.Blue_val = StringVar()

        self.control_win.Red_Entry = Entry(self.control_win,  textvariable = self.Red_val)
        self.control_win.Red_Entry_Label = Label(self.control_win, fg="Black", bg = "Red", text = "RED", font="Helvetica 24")
        self.control_win.Green_Entry = Entry(self.control_win, textvariable=self.Green_val)
        self.control_win.Green_Entry_Label = Label(self.control_win, fg="Black", bg="Green", text="GREEN", font="Helvetica 24")
        self.control_win.Blue_Entry = Entry(self.control_win,  textvariable=self.Blue_val)
        self.control_win.Blue_Entry_Label = Label(self.control_win, fg="Black", bg="Blue", text="BLUE",font="Helvetica 24")

        self.control_win.RGBLEDButton = Button(self.control_win, bg = "White", fg="Black", text = "RGB LED",font="Helvetica 24 bold", command=lambda: self.queue_out.put([self.control_win.Red_Entry.get(),self.control_win.Green_Entry.get(),self.control_win.Blue_Entry.get()]))
        self.control_win.UVLEDButton = Button(self.control_win, bg="White", fg="Black", text="UV LED",font="Helvetica 24 bold", command=lambda: self.queue_out.put("Toggle UV"))
        self.control_win.FanButton = Button(self.control_win, bg="White", fg="Black", text="Fan",font="Helvetica 24 bold", command=lambda: self.queue_out.put("Toggle Fan"))
        self.control_win.PumpButton = Button(self.control_win, bg="White", fg="Black", text="Pump",font="Helvetica 24 bold", command=lambda: self.queue_out.put("Toggle Pump"))
        self.control_win.ExitButton = Button(self.control_win, bg="White", fg="Black", text="\u23FB",font="Helvetica 24 bold", command=lambda: self.control_win.destroy())

        self.control_win.RGBLEDButton.grid(row=0, column=0)
        self.control_win.UVLEDButton.grid(row=1, column=0)
        self.control_win.FanButton.grid(row=2, column=0)
        self.control_win.PumpButton.grid(row=3, column=0)
        self.control_win.ExitButton.grid(row=4, column=0)

        self.control_win.Red_Entry_Label.grid(row=0, column=2)
        self.control_win.Red_Entry.grid(row=0, column=3)
        self.control_win.Green_Entry_Label.grid(row=0, column=5)
        self.control_win.Green_Entry.grid(row=0, column=6)
        self.control_win.Blue_Entry_Label.grid(row=0, column=8)
        self.control_win.Blue_Entry.grid(row=0, column=9)

    def processIncoming(self):
        """! 
        Receive data from the incoming queue (from the main process)
        """

        while not self.queue_in.empty():
            msg = self.queue_in.get()

            # Print whatever it receives from the main thread
            print("GUI: Received data from", msg[0] + ":", msg[1])

            if isinstance(msg[0], str):
                # Display the data accordingly
                if msg[0] == "soil_moisture_sensor_1":
                    self.SoilMoistureCondition_value.configure(text=str(msg[1])+"%")
                    if msg[2]:
                        self.SoilMoistureCondition_value.config(fg="Red")
                        self.SoilMoistureStatus_value.configure(text=msg[2])
                    else:
                        self.SoilMoistureCondition_value.config(fg="Green")
                        self.SoilMoistureStatus_value.configure(text="OK")

                elif msg[0] == "environment_sensor":
                    # Update temperature
                    print(msg[1])
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
                    self.RGBLEDIntensity_value.configure(text=str(msg[1][0]) + "% - " + str(msg[1][1]) + "% - " + str(msg[1][2]) + "%")
                else:
                    print("Unexpected item passed in main_to_gui queue:", msg)


if __name__ == "__main__":
    import sys
    ROOT = Tk()
    # ROOT.resizable()
    ROOT.geometry("1024x600")
    endCommand = lambda: sys.exit(0)
    app = GrowSpaceGUI(ROOT, Queue(), Queue(), endCommand)
    ROOT.mainloop() # Blocking!