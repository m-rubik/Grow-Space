"""!
This is a template class for any sensor input.
Each sensor will be inherit this class, and override/add any methods as required.
Therefore, each sensor is a worker class of this template.

This will run as a seperate process from the main thread.
"""

class Sensor():

    name:str = "Default"
    last_val:int = None
    current_val:int = None

    def __init__(self, name="default"):
        pass

    def run(self):
        """!
        This is the main loop for any sensor.
        It will read the value and report it back to the main 
        """

        # Read the sensor input
        # Update current/last val
        # Log val 
        # (Do other stuff)
        pass

    def poll(self):
        """!
        This is a manualy triggered capture & reporting of data.
        """
        # Read sensor value
        # Update current/last val
        # Log val 
        # (Do other stuff)
        # Report to main thread
        pass