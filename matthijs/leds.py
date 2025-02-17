from gpiozero import LED

class Leds:
    pin_leds = [17, 27, 22, 23]
    leds = {}
    threshold_on = 1502
    threshold_off = 1498

    @classmethod
    def setup_leds(cls):
        for pin in cls.pin_leds:
            cls.leds[pin] = LED(pin)
    
    @staticmethod
    def control_leds(channel_values):
        for key, pin in enumerate(Leds.pin_leds):
            led = Leds.leds[pin]
            value = channel_values[key]
            if value > Leds.threshold_on:
                led.on()
            elif value < Leds.threshold_off:
                led.off()
