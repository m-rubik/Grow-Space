# Imports
    # General
import time
import board
from busio import I2C

    # ADC/Moisture Sensors
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn 
    # Environment Sensor
#from src.utilities.sensor_template import Sensor
import adafruit_bme680
from datetime import datetime

import importlib
moduleName = 'src.utilities.sensor_template'
importlib.import_module(moduleName)

    # RGB LED
from rpi_ws281x import * # TODO: Fix this wildcard import

    # UV LED
import RPi.GPIO as io

# TODO: Can't run motor, lights, and fan all at the same time
# TODO: Can run the motor and the fan at the same time
# TODO: Can run the motor with 18.75Ohm, fan with 23.5Ohm, UV LEDs with 11.75Ohm, LEDs at 125 brightness.  This draws approx 4.2A total.  Preferably we would not run the motor, it does drop the brightness of the LEDS and drop the voltage to approx 11.2V.
# TODO: cont. Preferably we would run the fan and the motor separately, they can operate at the same time as the lights but the motor and fan should be separate.

if __name__ == "__main__":
    
    # RGB
    print("\n\n====================================")
    print("Testing RGB LED...")
    LED_COUNT = 144
    LED_PIN = 18
    LED_FREQ_HQ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 125
    # Brightness {75, 1.60A}, {100, 2.11A}, {125, 2.61A}
    LED_INVERT = False
    LED_CHANNEL = 0

    def adjust_color(strip, red_content=255, green_content=255, blue_content=255):
        for x in range(0, LED_COUNT):
            strip.setPixelColor(x, Color(red_content, green_content, blue_content))
            strip.show()
            
    def party_light(strip):
        import random
        for _ in range(10):
            for x in range(0, LED_COUNT):
                strip.setPixelColor(x, Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                strip.show()
            time.sleep(1)

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    adjust_color(strip, 0, 0, 0)
    #party_light(strip)
        # Relay
    print("\n\n====================================")
    print("Testing Relay...")
    in1 = 17
    in2 = 27
    in3 = 22

    io.setmode(io.BCM)
    io.setup(in1, io.OUT)  # Fan tested with a series of two 47ohms (in parrallel), so an effective 23.5Ohms
    io.setup(in2, io.OUT)  # UV LEDs draw 1.08A at 12.1V. With 12.5ohms (8 100ohms //) draw 840 mA
    io.setup(in3, io.OUT)  # Pump has current limiting 25ohms w/ back-emf resistance 200ohms

    io.output(in1, True)
    io.output(in2, True)
    io.output(in3, True)
    
    adjust_color(strip, 255, 255, 255)
    time.sleep(5)
    
    for input in [in2, in1]:
        io.output(input, False)
        time.sleep(5)
        #io.output(input, True)
    
    #io.output(in1, True)
    io.output(in2, True)
    io.output(in1, True)


    # Moisture Sensor Testing Block
    print("\n\n====================================")
    print("Testing Moisture Sensors/ADC...")
    i2c = I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    current_time = datetime.now()
    # tests for 10 seconds
    for _ in range(1):
    #while (datetime.now()-current_time) < d.seconds(10):
        time.sleep(0.5)
        print("====================================")
        print("SENSOR 1")
        print("{:>5}\t{:>5.3f}".format(chan0.value, chan0.voltage))
        time.sleep(0.5)
        print("====================================")
        print("SENSOR 2")
        print("{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))

    # Multifunction Sensor
    print("\n\n====================================")
    print("Testing environment sensor...")
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
    bme680.sea_level_pressure = 1013.25
    current_time = datetime.now()
    # tests for 10 seconds
    for _ in range(1):
    #while (datetime.now()-current_time) < 10:
        print("\nTemperature: %0.1f C" % bme680.temperature)
        print("\nGas: %d ohm" % bme680.gas)
        print("\nHumidity: %0.1f %%" % bme680.humidity)
        print("\nPressure: %0.3f hPa" % bme680.pressure)
        print("\nAltitude = %0.2f meters" % bme680.altitude)
        time.sleep(1)


    io.output(in1, True)
    io.output(in2, True)
    io.output(in3, True)

    current_time = datetime.now()
#    for input in [in1, in2, in3]:
#        io.output(input, False)
#        time.sleep(5)
#        io.output(input, True)

    io.cleanup()  # cleanup all GPIO
    print("Testing Complete")
    adjust_color(strip, 0, 0, 0)

