from gpiozero import LED
from time import sleep

class Led:
    def __init__(self, gpio_led_pin=27):
        self.led_pin = gpio_led_pin
        self.led = LED(gpio_led_pin)
        self.threshold = 1500

    def zetLedAan(self, channels):
        try:
            # if channels and len(channels) > 4:
                print(f"{channels[3]}")
                if channels[3] > self.threshold:
                    self.led.on()
                    print("LED is AAN")
                else:
                    self.led.off()
                    print("LED is UIT!")
            # else:
                # print("Ongeldige of incomplete kanaaldata ontvangen.")
        except Exception as e:
            print(f"Fout bij het schakelen van de LED: {e}")

if __name__ == "__main__":
     pass
    # try:
    #     get_ibus_data = IBus()
    #     channels = get_ibus_data.readData()
    #     print(f"{channels[4]}")
    #     if channels is None:
    #         print("Geen data ontvangen van IBus.")
    #     else:
    #         call_led_class = Led()
    #         call_led_class.zetLedAan(channels)

    # except Exception as e:
    #     print(f"Error: {e}")
