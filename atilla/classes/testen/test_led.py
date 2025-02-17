from gpiozero import LED

class Led:
    def __init__(self, gpio_led_pin=27):
        self.led_pin = gpio_led_pin
        self.led = LED(gpio_led_pin)
        self.threshold = 1500

    def zetLedAan(self, channels):
        try:
            if channels and len(channels) > 4:
                # print(f"{channels[1]}")
                if channels[1] > self.threshold:
                    self.led.on()
                    # print("LED is AAN")

                else:
                    self.led.off()
                    # print("LED is UIT!")

        except Exception as e:
            print(f"Fout bij het schakelen van de LED: {e}")

if __name__ == "__main__":
     pass
