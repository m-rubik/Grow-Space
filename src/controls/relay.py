"""!
This code is for the intialization and control of relays through
RPi GPIO pins.
"""

import RPi.GPIO as GPIO


class Relay:
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

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT) 
        GPIO.output(self.pin, self.is_conducting)

    def toggle(self):
        if self.is_conducting:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        self.is_conducting = True
        GPIO.output(self.pin, self.is_conducting)

    def turn_off(self):
        self.is_conducting = False
        GPIO.output(self.pin, self.is_conducting)


if __name__ == "__main__":
    """
    Example code from: https://www.electronicshub.org/control-a-relay-using-raspberry-pi/
    """

    import RPi.GPIO as io
    import time

    in1 = 11
    in2 = 13
    in3 = 15

    io.setmode(io.BOARD)
    io.setup(in1, io.OUT)
    io.setup(in2, io.OUT)
    io.setup(in3, io.OUT)

    io.output(in1, True)
    io.output(in2, True)
    io.output(in3, True)

    time.sleep(1)

    io.output(in1, False)
    io.output(in2, False)
    io.output(in3, False)

    time.sleep(1)

    io.output(in1, True)
    io.output(in2, True)
    io.output(in3, True)

    # try:
    #     while True:
    #         for x in range(5):
    #             io.output(in1, True)
    #             time.sleep(1)
    #             io.output(in1, False)
    #             io.output(in2, True)
    #             time.sleep(1)
    #             io.output(in2, False)
            
    #         io.output(in1,True)
    #         io.output(in2,True)

    #         for x in range(4):
    #             io.output(in1, True)
    #             time.sleep(1)
    #             io.output(in1, False)
    #             time.sleep(1)
                
    #         io.output(in1,True)

    #         for x in range(4):
    #                 io.output(in2, True)
    #                 time.sleep(1)
    #                 io.output(in2, False)
    #                 time.sleep(1)
    #         io.output(in2,True)
    # except KeyboardInterrupt:
    #     io.cleanup()