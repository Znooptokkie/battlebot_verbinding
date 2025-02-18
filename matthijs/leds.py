from gpiozero import LED

class Leds:
    pin_leds = [17, 27, 22, 23]
    leds = {}
    threshold_on = 1502
    threshold_off = 1498

    @classmethod
    def setupLeds(cls):
        for pin in cls.pin_leds:
            print(f"leds {pin}")
            cls.leds[pin] = LED(pin)
    
    @classmethod
    def controlLeds(cls, channel_values):
        cls.setupLeds()
        for key, pin in enumerate(cls.pin_leds):
            led = cls.leds[pin]
            value = channel_values[key]
            # print(f"leds {cls.leds}")
            if value > cls.threshold_on:
                led.on()
                # print(value)
            elif value < cls.threshold_off:
                led.off()