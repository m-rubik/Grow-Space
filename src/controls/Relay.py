"""
Example code from: https://www.electronicshub.org/control-a-relay-using-raspberry-pi/
"""

import RPi.GPIO as GPIO
import time

in1 = 16
in2 = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

GPIO.output(in1, False)
GPIO.output(in2, False)

try:
    while True:
      for x in range(5):
            GPIO.output(in1, True)
            time.sleep(1)
            GPIO.output(in1, False)
            GPIO.output(in2, True)
            time.sleep(1)
            GPIO.output(in2, False)
      
      GPIO.output(in1,True)
      GPIO.output(in2,True)

      for x in range(4):
            GPIO.output(in1, True)
            time.sleep(1)
            GPIO.output(in1, False)
            time.sleep(1)
      GPIO.output(in1,True)

      for x in range(4):
            GPIO.output(in2, True)
            time.sleep(1)
            GPIO.output(in2, False)
            time.sleep(1)
      GPIO.output(in2,True)



except KeyboardInterrupt:
    GPIO.cleanup()