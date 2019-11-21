"""!
This is the Graphical User Interface (GUI) that the user can use.
The GUI is based on a Tkinter widget.
"""


from multiprocessing import Queue
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, StringVar

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

        # Declare all variables used by the GUI
        self.total = 0
        self.entered_number = 0

        # Add GUI components
        self.stop_button = Button(master, text="EXIT", bg="Red", command=endCommand)

        self.soil_1_text = StringVar()
        self.soil_1_text.set("Soil Moisture Sensor 1:")
        self.soil_1_label = Label(master, bg="Black", fg="White", textvariable=self.soil_1_text)

        self.soil_1_val = StringVar()
        self.soil_1_val.set("-")
        self.soil_1_val_label = Label(master, bg="Black", textvariable=self.soil_1_val)

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

        # Layout the GUI components
        self.label.grid(row=0, column=0, sticky=W) # Use a grid
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        self.add_button.grid(row=2, column=0)
        self.subtract_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2, sticky=W+E)
        self.stop_button.grid(row=3, column=1, columnspan=1, sticky=E)
        self.soil_1_label.grid(row=4, column=0, columnspan=2, sticky=W)
        self.soil_1_val_label.grid(row=4, column=3, columnspan=1, sticky=E)


    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        else: # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

    def processIncoming(self):
        """! 
        If any data is coming back to the main processes,
        receive it here and display it
        """
        while not self.queue.empty():
            msg = self.queue.get()

            # Print to console whatever it gets
            print("Received from", msg[0] + ":", msg[1])

            # Display the data accordingly
            if msg[0] == "soil_moisture_sensor_1":
                self.soil_1_val.set(msg[1])
                if msg[1] > 0.5:
                    self.soil_1_val_label.config(fg="Red")
                else:
                    self.soil_1_val_label.config(fg="Green")