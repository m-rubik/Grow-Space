"""!
This code is for the intialization and control of a
ws281 LED strip.
"""


from rpi_ws281x import * # TODO: Fix this wildcard import
import atexit

class LEDStrip():
    """!
    This is the class for the ws281 LED strip.
    @param LED_COUNT: Number of LEDs in the strip
    @param LED_PIN: GPIO pin connected to the strip. IMPORTANT: THIS IS THE GPIO PIN, NOT THE BOARD PIN
    @param LED_FREQ_HQ: LED signal frequency
    @param LED_DMA: DMA Channel used to generate the signal
    @param LED_BRIGHTNESS: Acceptable range is 0-255
    @param LED_INVERT: Set True only when needed to invert the signal (when using NPN transistor level shift)
    @param LED_CHANNEL: Set to 1 for GPIOs 13, 19, 41, 45 or 53, otherwise set 0
    @param strip: The light strip object
    """

    LED_COUNT: int = 144
    LED_PIN: int = 18 # pin 12
    LED_FREQ_HQ: int = 800000
    LED_DMA: int = 10
    LED_BRIGHTNESS: int = 100 # In testing, for the full strip (before cutting), we find: {75, 1.60A}, {100, 2.11A}, {125, 2.61A}
    LED_INVERT: bool = False
    LED_CHANNEL: int = 0
    strip = None
    name = None

    def __init__(self, LED_PIN, name="Default", LED_COUNT=144, LED_FREQ_HQ=800000, LED_DMA=10, LED_BRIGHTNESS=100, LED_INVERT=False):

        if LED_BRIGHTNESS < 0:
            self.LED_BRIGHTNESS = 0
        elif LED_BRIGHTNESS > 255:
            self.LED_BRIGHTNESS = 255
        else:
            self.LED_BRIGHTNESS = LED_BRIGHTNESS

        if LED_PIN in [13, 19, 41, 45, 53]: # see: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/ 
            self.LED_CHANNEL = 1
        else:
            self.LED_CHANNEL = 0

        self.LED_PIN = LED_PIN
        self.LED_COUNT = LED_COUNT
        self.LED_FREQ_HQ = LED_FREQ_HQ
        self.LED_DMA = LED_DMA
        self.LED_BRIGHTNESS = LED_BRIGHTNESS
        self.LED_INVERT = LED_INVERT

        self.strip = Adafruit_NeoPixel(self.LED_COUNT, 
                                       self.LED_PIN,
                                       self.LED_FREQ_HQ,
                                       self.LED_DMA,
                                       self.LED_INVERT,
                                       self.LED_BRIGHTNESS,
                                       self.LED_CHANNEL)
        self.strip.begin()
        self.name = name
        atexit.register(self.shutdown)

    def adjust_color(self, pixel_range="All", red_content=255, green_content=255, blue_content=255):
        if pixel_range == "All":
            pixel_range = range(0, self.LED_COUNT)
        for LED in pixel_range:
            self.strip.setPixelColor(LED, Color(red_content, green_content, blue_content))
        self.strip.show()
            
    def shutdown(self):
        print(self.name, "shutting down.")
        self.adjust_color(red_content=0, green_content=0, blue_content=0)
        

if __name__ == "__main__":
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

    UPDATE:
    Just run this as sudo. Check the howto.txt
    """

    from rpi_ws281x import * # TODO: Fix this wildcard import
    import time

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
        
    adjust_color(strip, 255, 255, 255)
    #rainbowCycle(strip)

    print("DONE")