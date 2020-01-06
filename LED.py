"""
Be aware that to get this to work, you need to be able to access
/dev/mem which is usually locked access only to root.

Solutions to this are apparently to do:
sudo groupadd gpio <--- if the group doesn't already exist. Find it first in /dev
sudo usermod -a -G gpio pi <-- or replace "pi" with the user name
sudo grep gpio /etc/group
sudo chown root.gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem

My current settings are:
gpiomem is owned by root:gpio with permissions crw-rw----
and mem is owned by root:kmem with permissions crw-r-----

I still have to run the code as root. This could be a problem!
Perhaps if all else fails:
sudo chmod 777 /dev/mem

Possibly add yourself to kmem group with sudo usermod -g kmem pi
"""

from rpi_ws281x import *
import time

LED_COUNT = 144
LED_PIN = 18
LED_FREQ_HQ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100
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
    
def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        
def adjust_color(strip, red_content=255, green_content=255, blue_content=255):
    for x in range(0, LED_COUNT):
        strip.setPixelColor(x, Color(red_content,green_content,blue_content))
        strip.show()
        
strip = Adafruit_NeoPixel(LED_COUNT,LED_PIN,LED_FREQ_HQ,LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
     
adjust_color(strip, 10, 0, 10)

print("DONE")