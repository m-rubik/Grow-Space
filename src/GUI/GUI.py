"""!
This is the Graphical User Interface (GUI) that the user can use.
The GUI is based on a Tkinter widget.
"""


from multiprocessing import Queue
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, N, S, StringVar
from tkinter.filedialog import askopenfile, asksaveasfile


class GrowSpaceGUI:
    """!
    GUI class for any grow space box.
    @param queue: The queue to communicate to the main thread.
    @param master: The root (instance) of a Tkinter top-level widget
    """

    queue:Queue = None
    master = None
    control_win = None

    def __init__(self, master, queue, endCommand):
        self.queue = queue
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
        self.SoilMoistureCondition_value = Label(self.master, bg="Black", fg="White", text="50%", font="Helvetica 22")
        self.TemperatureCondition_value  = Label(self.master, bg="Black", fg="White", text="100%", font="Helvetica 22")
        self.HumidityCondition_value  = Label(self.master, bg="Black", fg="White", text="0%", font="Helvetica 22")
        self.VOCCondition_value  = Label(self.master, bg="Black", fg="White", text="10%", font="Helvetica 22")

        self.SoilMoistureStatus_value = Label(self.master, bg="Black", fg="White", text="HIGH", font="Helvetica 22")
        self.TemperatureStatus_value = Label(self.master, bg="Black", fg="White", text="LOW", font="Helvetica 22")
        self.HumidityStatus_value = Label(self.master, bg="Black", fg="White", text="OK", font="Helvetica 22")
        self.VOCStatus_value = Label(self.master, bg="Black", fg="White", text="OK", font="Helvetica 22")

        self.SoilMoistureRange_value = Label(self.master, bg="Black", fg="White", text="20% - 40%", font="Helvetica 22")
        self.TemperatureRange_value = Label(self.master, bg="Black", fg="White", text="20" + u"\u00b0" + "C" + " - 25" + u"\u00b0" + "C", font="Helvetica 22")
        self.HumidityRange_value = Label(self.master, bg="Black", fg="White", text="30% - 35%", font="Helvetica 22")
        self.VOCRange_value = Label(self.master, bg="Black", fg="White", text="50% - 60%", font="Helvetica 22")

        self.PumpStatus_value = Label(self.master, bg="Black", fg="White", text="OFF", font="Helvetica 22")
        self.FanStatus_value = Label(self.master, bg="Black", fg="White", text="ON", font="Helvetica 22")
        self.RGBLEDIntensity_value = Label(self.master, bg="Black", fg="White", text="10% - 20% - 30%", font="Helvetica 22")
        self.UVLEDIntensity_value = Label(self.master, bg="Black", fg="White", text="10%", font="Helvetica 22")


        #Creating Buttons

        self.LoadButton = Button(self.master, bg = "White", fg="Black", text="LOAD", font="Helvetica 24 bold", command=self.load_file)
        self.SaveButton = Button(self.master, bg="White", fg="Black", text="SAVE", font="Helvetica 24 bold", command=self.save_file)
        self.PowerButton = Button(self.master, bg="White", fg="Black", text=u"\u23FB", font="Helvetica 24 bold", command=None)
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

        # Condition Headers
        self.EnvironmentalConditionHeader.grid(row=5, column=5, columnspan=10, sticky=W)
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
        self.ParameterRangeHeader.grid(row=5, column=22, columnspan=10, sticky=W)
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
        config_file = askopenfile(filetypes=(("Configuration files", "*.cfg"), ("All files", "*.*")))
        print(config_file)

    def save_file(self):
        files = [("Configuration files", "*.cfg"), ('All Files', '*.*')]
        f = asksaveasfile(filetypes = files, defaultextension = files)
        if f is None: # User closes the dialog with "cancel"
            return
        text2save = "UHHHHHH"
        f.write(text2save)
        f.close()

    def control_window(self):
        self.control_win = Tk()
        self.control_win.title("Control Devices")
        self.control_win.configure(bg="Black")
        self.control_win.geometry("1024x600")

        self.control_win.RGBLEDButton = Button(self.control_win, bg = "White", fg="Black", text = "RGB LED",font="Helvetica 24 bold", command=None)
        self.control_win.UVLEDButton = Button(self.control_win, bg="White", fg="Black", text="UV LED",font="Helvetica 24 bold", command=None)
        self.control_win.FanButton = Button(self.control_win, bg="White", fg="Black", text="Fan",font="Helvetica 24 bold", command=None)
        self.control_win.PumpButton = Button(self.control_win, bg="White", fg="Black", text="Pump",font="Helvetica 24 bold", command=None)
        self.control_win.ExitButton = Button(self.control_win, bg="White", fg="Black", text="Pump",font="Helvetica 24 bold", command=None)

        self.control_win.RGBLEDButton.grid(row=2, column=6)
        self.control_win.UVLEDButton.grid(row=10, column=6)
        self.control_win.FanButton.grid(row=15, column=6)
        self.control_win.PumpButton.grid(row=20, column=6)


    # def processIncoming(self):
    #     """!
    #     If any data is coming back to the main processes,
    #     receive it here and display it
    #     """
    #
    #     warning_flags = {}
    #     error_flags = {}
    #
    #     while not self.queue.empty():
    #         msg = self.queue.get()
    #
    #         # Print to console whatever it gets
    #         print("Received from", msg[0] + ":", msg[1])
    #
    #         if isinstance(msg[0], str):
    #             # Display the data accordingly
    #             if msg[0] == "soil_moisture_sensor_1":
    #                 self.soil_1_val.set(str(msg[1])+"%")
    #                 if int(msg[1]) < 65:
    #                     self.soil_1_val_label.config(fg="Red")
    #                     warning_flags["soil_moisture_sensor_1"] = "Needs Watering"
    #                 else:
    #                     self.soil_1_val_label.config(fg="Green")
    #                     warning_flags.pop('soil_moisture_sensor_1', None)
    #
    #             elif msg[0] == "environment_sensor":
    #                 received_temp = round(msg[1]['temperature'], 2)
    #                 self.temperature_val.set(str(received_temp)+"°C")
    #                 if received_temp < 20:
    #                     self.temperature_val_label.config(fg="Red")
    #                     warning_flags["temperature_sensor"] = "Too Cold"
    #                 elif received_temp > 30:
    #                     self.temperature_val_label.config(fg="Red")
    #                     warning_flags["temperature_sensor"] = "Too Hot"
    #                 else:
    #                     self.temperature_val_label.config(fg="Green")
    #                     warning_flags.pop('temperature_sensor', None)
    #
    #             if error_flags:
    #                 self.overall_status_text_label.config(fg="Red")
    #                 self.overall_status_val.set(','.join(str(x) for x in error_flags.values()))
    #             elif warning_flags:
    #                 self.overall_status_text_label.config(fg="Yellow")
    #                 self.overall_status_val.set(','.join(str(x) for x in warning_flags.values()))
    #             else:
    #                 self.overall_status_text_label.config(fg="Green")
    #                 self.overall_status_val.set('Good')
    #



if __name__ == "__main__":
    from multiprocessing import Queue
    import sys
    ROOT = Tk()
    # WIDTH, HEIGHT = ROOT.winfo_screenwidth(), ROOT.winfo_screenheight()
    # ROOT.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
    ROOT.resizable()
    ROOT.geometry("1024x600")
    endCommand = lambda: sys.exit(0)
    app = GrowSpaceGUI(ROOT, Queue(), endCommand)
    ROOT.mainloop() # Blocking!