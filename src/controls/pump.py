"""!
This code is for the intialization and control of the Pump
"""

from src.utilities.relay_template import Relay


class Pump(Relay):

    def __init__(self, pin, name="default", is_off=False, queue=None):
        super().__init__(pin, name, is_off)
       

if __name__ == "__main__":
    import time
    import RPi.GPIO as GPIO

    in1 = 22

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)

    GPIO.output(in1, True) # Turn it off
    time.sleep(1)
    GPIO.output(in1, False) # Turn it on
    time.sleep(5)
    GPIO.output(in1, True) # Turn it off