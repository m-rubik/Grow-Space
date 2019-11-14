from multiprocessing import Queue
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, StringVar

class GrowSpaceGUI:

    queue:Queue = None
    master = None

    def __init__(self, master, queue, endCommand):
        self.queue = queue
        self.master = master
        master.title("Grow Space")

        # Add features to the GUI
        self.stop_button = Button(master, text="EXIT", command=endCommand)
        self.soil_1_text = StringVar()
        self.soil_1_text.set("No data yet")
        self.soil_1_label = Label(master, textvariable=self.soil_1_text)

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

        # LAYOUT
        self.label.grid(row=0, column=0, sticky=W)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        self.add_button.grid(row=2, column=0)
        self.subtract_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2, sticky=W+E)
        self.stop_button.grid(row=3, column=1, columnspan=1, sticky=E)
        self.soil_1_label.grid(row=4, column=1, columnspan=2, sticky=E)


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
            if msg[0] == "soil moisture sensor #1":
                self.soil_1_text.set(msg[1])