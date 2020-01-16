"""!
This code is for ADC
"""

import time
import board
from busio import I2C
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn 
import adafruit_bme680

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)
print("{:>5}\t{:>5}".format('raw','v'))

# Create library object using our Bus I2C port
i2c2 = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c2, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25


while True:
    print("{:>5}\t{:>5.3f}".format(chan.value,chan.voltage))
    print("\nTemperature: %0.1f C" % bme680.temperature)
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)
    time.sleep(0.5)
