"""!
This code is for the simulation of a ws281 LED strip.
"""


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
    LED_PIN: int = 18
    LED_FREQ_HQ: int = 800000
    LED_DMA: int = 10
    LED_BRIGHTNESS: int = 100
    LED_INVERT: bool = False
    LED_CHANNEL: int = 0
    strip = None

    def __init__(self, LED_PIN, name="Default", LED_COUNT=144, LED_FREQ_HQ=800000, LED_DMA=10, LED_BRIGHTNESS=100, LED_INVERT=False):

        if LED_BRIGHTNESS < 0:
            self.LED_BRIGHTNESS = 0
        elif LED_BRIGHTNESS > 255:
            self.LED_BRIGHTNESS = 255
        else:
            self.LED_BRIGHTNESS = LED_BRIGHTNESS

        if LED_PIN in [13, 19, 41, 45, 53]:
            self.LED_CHANNEL = 1
        else:
            self.LED_CHANNEL = 0

        self.LED_PIN = LED_PIN
        self.LED_COUNT = LED_COUNT
        self.LED_FREQ_HQ = LED_FREQ_HQ
        self.LED_DMA = LED_DMA
        self.LED_BRIGHTNESS = LED_BRIGHTNESS
        self.LED_INVERT = LED_INVERT

    def adjust_color(self, pixel_range="All", red_content=255, green_content=255, blue_content=255):
        pass

if __name__ == "__main__":
    s = LEDStrip(18)
    s.adjust_color(range(0,4))