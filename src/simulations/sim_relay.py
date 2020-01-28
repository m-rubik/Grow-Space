"""!
This code is for the simulation of relays
"""

import atexit


class Relay():
    """!
    This is the class for all relay devices
    @param pin: The RPi pin that acts as the signal pin to the relay
    @param name: The name of the relay.
    @param is_off: The current state of the relay
    """

    pin: int
    name: str = "default"
    is_off: int = False

    def __init__(self, pin, name="default", is_off=False):
        """!
        Standard initialization.
        @param pin: The RPi pin that acts as the signal pin to the relay
        @param name: The name of the relay.
        @param is_off: The current state of the relay
        """

        self.pin = pin
        self.name = name
        self.is_off = is_off
        atexit.register(self.shutdown)

    def toggle(self):
        if self.is_off:
            self.turn_on()
        else:
            self.turn_off()

    def turn_on(self):
        print("Turning on", self.name)
        self.is_off = False

    def turn_off(self):
        print("Turning off", self.name)
        self.is_off = True

    def shutdown(self):
        print(self.name, "shutting down.")
        self.is_off = True
