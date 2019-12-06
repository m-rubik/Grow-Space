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

    def __init__(self, master, queue, endCommand):
        self.queue = queue
        self.master = master
        self.master.title("Grow Space")
        self.master.configure(background="Black")

        # Declare constants
        self.configuration_text = StringVar()
        self.configuration_text.set("Current Environment:")
        self.overall_status_text = StringVar()
        self.overall_status_text.set("Environment Status:")
        self.temperature_text = StringVar()
        self.temperature_text.set("Temperature:")
        self.soil_1_text = StringVar()
        self.soil_1_text.set("Soil Moisture Sensor 1:")

        # Declare all variables
        self.configuration_val = StringVar()
        self.overall_status_val = StringVar()
        self.soil_1_val = StringVar()
        self.temperature_val = StringVar()

        # Set initial variable values
        self.configuration_val.set("Basil World 1.0")
        self.overall_status_val.set("Good")
        self.soil_1_val.set("-")
        self.temperature_val.set("-")

        # Add GUI components
        self.stop_button = Button(master, text="EXIT", bg="Red", command=endCommand)
        self.configuration_label = Label(master, bg="Black", fg="White", textvariable=self.configuration_text)
        self.configuration_val_label = Label(master, bg="Black", fg="White", textvariable=self.configuration_val)
        self.overall_status_text_label = Label(master, bg="Black", fg="Green", textvariable=self.overall_status_val)
        self.overall_status_label = Label(master, bg="Black", fg="White", textvariable=self.overall_status_text)
        self.soil_1_label = Label(master, bg="Black", fg="White", textvariable=self.soil_1_text)
        self.soil_1_val_label = Label(master, bg="Black", fg="White", textvariable=self.soil_1_val)
        self.temperature_label = Label(master, bg="Black", fg="White", textvariable=self.temperature_text)
        self.temperature_val_label = Label(master, bg="Black", fg="White", textvariable=self.temperature_val)

        # Layout the GUI components
        self.configuration_label.grid(row=0, column=0, columnspan=1, sticky=W)
        self.configuration_val_label.grid(row=0, column=1, columnspan=1, sticky=W+E)
        self.overall_status_label.grid(row=1, column=0, columnspan=1, sticky=W)
        self.overall_status_text_label.grid(row=1, column=1, columnspan=1, sticky=W+E)

        # self.master.grid_rowconfigure(2, weight=1, minsize=1) # Empty Row

        self.soil_1_label.grid(row=3, column=0, columnspan=1, sticky=W)
        self.soil_1_val_label.grid(row=3, column=1, columnspan=1, sticky=W+E)
        self.temperature_label.grid(row=4, column=0, columnspan=1, sticky=W)
        self.temperature_val_label.grid(row=4, column=1, columnspan=1, sticky=W+E)

        self.button = Button(master, text="Load", command=self.load_file, width=10)
        self.button.grid(row=5, column=0, sticky=W)
        self.button = Button(master, text="Save", command=self.save_file, width=10)
        self.button.grid(row=5, column=1, sticky=E)
        self.stop_button.grid(row=6, column=0, columnspan=2, sticky=W)

        # print(self.grid_info())
        # for column in 
        # grid_columnconfigure(index=i)


        ## TODO: REMOVE THIS. This is just the stuff from the sample GUI
        # self.total = 0
        # self.entered_number = 0
        # self.total_label_text = IntVar()
        # self.total_label_text.set(self.total)
        # self.total_label = Label(master, textvariable=self.total_label_text)
        # self.label = Label(master, text="Total:")
        # vcmd = master.register(self.validate) # we have to wrap the command
        # self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        # self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        # self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        # self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))
        # self.label.grid(row=0, column=0, sticky=W) # Use a grid
        # self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
        # self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        # self.add_button.grid(row=2, column=0)
        # self.subtract_button.grid(row=2, column=1)
        # self.reset_button.grid(row=2, column=2, sticky=W+E)

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

    def processIncoming(self):
        """! 
        If any data is coming back to the main processes,
        receive it here and display it
        """

        warning_flags = {}
        error_flags = {}

        while not self.queue.empty():
            msg = self.queue.get()

            # Print to console whatever it gets
            print("Received from", msg[0] + ":", msg[1])

            # Display the data accordingly
            if msg[0] == "soil_moisture_sensor_1":
                self.soil_1_val.set(str(msg[1])+"%")
                if msg[1] < 65:
                    self.soil_1_val_label.config(fg="Red")
                    warning_flags["soil_moisture_sensor_1"] = "Needs Watering"
                else:
                    self.soil_1_val_label.config(fg="Green")
                    warning_flags.pop('soil_moisture_sensor_1', None)
            if msg[0] == "temperature_sensor":
                self.temperature_val.set(str(msg[1])+"°C")
                if msg[1] < 20:
                    self.temperature_val_label.config(fg="Red")
                    warning_flags["temperature_sensor"] = "Too Cold"
                elif msg[1] > 30:
                    self.temperature_val_label.config(fg="Red")
                    warning_flags["temperature_sensor"] = "Too Hot"
                else:
                    self.temperature_val_label.config(fg="Green")
                    warning_flags.pop('temperature_sensor', None)

            if error_flags:
                self.overall_status_text_label.config(fg="Red")
                self.overall_status_val.set(','.join(str(x) for x in error_flags.values()))
            elif warning_flags:
                self.overall_status_text_label.config(fg="Yellow")
                self.overall_status_val.set(','.join(str(x) for x in warning_flags.values()))
            else:
                self.overall_status_text_label.config(fg="Green")
                self.overall_status_val.set('Good')
            
                


    ## TODO: REMOVE. This is only from the sample GUI
    # def validate(self, new_text):
    #     if not new_text: # the field is being cleared
    #         self.entered_number = 0
    #         return True

    #     try:
    #         self.entered_number = int(new_text)
    #         return True
    #     except ValueError:
    #         return False

    # def update(self, method):
    #     if method == "add":
    #         self.total += self.entered_number
    #     elif method == "subtract":
    #         self.total -= self.entered_number
    #     else: # reset
    #         self.total = 0

    #     self.total_label_text.set(self.total)
    #     self.entry.delete(0, END)
