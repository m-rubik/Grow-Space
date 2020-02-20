"""!
This code is for the intialization and control of relays through
RPi GPIO pins.
"""

import RPi.GPIO as GPIO
from abc import ABC, abstractmethod
import atexit


class Relay(ABC):
    """!
    This is the class for all relay devices
    @param pin: The RPi pin that acts as the signal pin to the relay
    @param name: The name of the relay.
    @param is_off: The current state of the relay
    """

    pin: int
    name: str = "default"
    is_off: int = False

    def __init__(self, pin, name="default", is_off=True):
        """!
        Standard initialization.
        @param pin: The RPi pin that acts as the signal pin to the relay
        @param name: The name of the relay.
        @param is_off: The current state of the relay
        """

        self.pin = pin
        self.name = name
        self.is_off = is_off

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT) 
        GPIO.output(self.pin, self.is_off)
        atexit.register(self.shutdown)

    def toggle(self):
        if self.is_off:
            self.turn_on()
            self.is_off = False
        else:
            self.turn_off()

    def turn_on(self):
        self.is_off = False
        GPIO.output(self.pin, self.is_off)
        print("Turning on", self.name)

    def turn_off(self):
        self.is_off = True
        GPIO.output(self.pin, self.is_off)
        print("Turning off", self.name)

    def shutdown(self):
        print(self.name, "shutting down.")
        self.is_off = True
        GPIO.output(self.pin, self.is_off)


if __name__ == "__main__":
    import time

    in1 = 17
    in2 = 27
    in3 = 22

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT) # FAN
    GPIO.setup(in2, GPIO.OUT) # UV LED
    GPIO.setup(in3, GPIO.OUT) # PUMP

    GPIO.output(in1, True)
    GPIO.output(in2, True)
    GPIO.output(in3, True)

    time.sleep(1)

    GPIO.output(in1, False)
    GPIO.output(in2, False)
    GPIO.output(in3, False)

    time.sleep(5)

    GPIO.output(in1, True)
    GPIO.output(in2, True)
    GPIO.output(in3, True)

