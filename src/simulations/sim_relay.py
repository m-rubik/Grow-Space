"""!
This code is for the simulation of relays
"""

class Relay():
    """!
    This is the class for all relay devices
    @param pin: The RPi pin that acts as the signal pin to the relay
    @param name: The name of the relay.
    @param is_conducting: The current state of the relay
    """

    pin: int
    name: str = "default"
    is_conducting: int = False

    def __init__(self, pin, name="default", is_conducting=False):
        """!
        Standard initialization.
        @param pin: The RPi pin that acts as the signal pin to the relay
        @param name: The name of the relay.
        @param is_conducting: The current state of the relay
        """

        self.pin = pin
        self.name = name
        self.is_conducting = is_conducting

    def toggle(self):
        if self.is_conducting:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        self.is_conducting = True

    def turn_off(self):
        self.is_conducting = False
