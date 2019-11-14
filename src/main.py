"""!
This is the main thread.

This thread will periodically call the sensor worker threads to 
poll for their data. This data is returned here, so it can be analysed
and control signals can be generated.
"""

import sys
from tkinter import Tk
from src.GUI.GUI import GrowSpaceGUI
from multiprocessing import Queue
import threading
from src.utilities.sensor_template import Sensor

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for each sensor (I/O worker).
        """
        self.master = master

        self.soil_queue = Queue()
        self.soil = Sensor(name="soil moisture sensor #1", queue=self.soil_queue)

        self.queue = Queue()
        # Set up the GUI part
        self.gui = GrowSpaceGUI(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.soil.run)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # Cleanup time!
            # For each thread, pass it a STOP signal
            self.soil_queue.put("STOP")

            # Brutal system exit. Make sure everything is cleaned up first!
            sys.exit(0)

        # For each sensor thread, check if it has data
        if not self.soil_queue.empty():
            msg = self.soil_queue.get()

            # Do stuff with the data
            # ...

            # Relay the data to the GUI so the user can see it
            self.queue.put(msg)

        # Wait 200ms
        self.master.after(200, self.periodicCall)

    def endApplication(self):
        self.running = 0

if __name__ == "__main__":
    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    client = ThreadedClient(root)
    root.mainloop()