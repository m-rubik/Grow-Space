# Imports
    # General
import time
import board
from busio import I2C

    # ADC/Moisture Sensors
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

    # Environment Sensor
from src.utilities.sensor_template import Sensor
import adafruit_bme680
from datetime import datetime

    # RGB LED
from rpi_ws281x import * # TODO: Fix this wildcard import

    # UV LED
import RPi.GPIO as io

if __name__ == "__main__":

    # Moisture Sensor Testing Block
    print("\n\n====================================")
    print("Testing Moisture Sensors/ADC...")
    i2c = I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    current_time = datetime.now()
    # tests for 10 seconds
    while (datetime.now()-current_time) < 10.0:
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
    while (datetime.now()-current_time) < 10.0:
        print("\nTemperature: %0.1f C" % bme680.temperature)
        print("\nGas: %d ohm" % bme680.gas)
        print("\nHumidity: %0.1f %%" % bme680.humidity)
        print("\nPressure: %0.3f hPa" % bme680.pressure)
        print("\nAltitude = %0.2f meters" % bme680.altitude)
        time.sleep(1)

    # RGB
    print("\n\n====================================")
    print("Testing RGB LED...")
    LED_COUNT = 144
    LED_PIN = 18
    LED_FREQ_HQ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 10
    # Brightness {75, 1.60A}, {100, 2.11A}, {125, 2.61A}
    LED_INVERT = False
    LED_CHANNEL = 0

    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow_cycle(strip, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)

    def adjust_color(strip, red_content=255, green_content=255, blue_content=255):
        for x in range(0, LED_COUNT):
            strip.setPixelColor(x, Color(red_content, green_content, blue_content))
            strip.show()


    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HQ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    current_time = datetime.now()
    # tests for 10 seconds
    while (datetime.now()-current_time) < 10.0:
        rainbow_cycle(strip)
    adjust_color(strip, 0, 0, 0)

    # Relay
    print("\n\n====================================")
    print("Testing Relay...")
    in1 = 11
    in2 = 13
    in3 = 15

    io.setmode(io.BOARD)
    io.setup(in1, io.OUT)
    io.setup(in2, io.OUT)  # UV LEDs draw 1.08A at 12.1V. With 12.5ohms (8 100ohms //) draw 840 mA
    io.setup(in3, io.OUT)  # Pump has current limiting 25ohms w/ back-emf resistance 200ohms

    io.output(in1, True)
    io.output(in2, True)
    io.output(in3, True)

    current_time = datetime.now()
    for input in [in1, in2, in3]:
        io.output(input, False)
        time.sleep(10)
        io.output(input, True)

    io.cleanup()  # cleanup all GPIO
    print("Testing Complete")

