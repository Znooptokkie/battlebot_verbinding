from led import Led
import serial
import struct

class IBus: 

    def __init__(self, url="/dev/serial0", baudrate=115200, timeout=0.1):
        self.url = url
        self.baudrate = baudrate
        self.timeout = timeout
        self.led = Led()

        try:
            self.serial = serial.Serial(self.url, self.baudrate, timeout=self.timeout)
            print(f"Verbonden met {self.url} op {self.baudrate} baud")
            self.serial.reset_input_buffer()

        except serial.SerialException as e:
            print(f"Kan seriële verbinding niet openen: {e}")
            self.serial = None

    def readData(self):
        if self.serial is None:
            print("Geen actieve seriële verbinding. Stoppen...")
            return

        while True:
            try:
                if self.serial.in_waiting >= 32:
                    data = self.serial.read(32)

                    if data[0] == 0x20 and data[1] == 0x40 and len(data) == 32:
                        channels = struct.unpack("<14H", data[2:30])
                        print(f"Channels: {channels}")

                    else:
                        print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                    self.led.zetLedAan(channels)
                self.serial.timeout = 0.01

            except Exception as e:
                print(f"Fout tijdens uitlezen van iBUS data: {e}")
                break

    def writeData(self):
        pass

if __name__ == "__main__":
    try:
        get_ibus_data = IBus()
        channels = get_ibus_data.readData()
    except Exception as e:
        print(f"Error: {e}")
    # try:
    #     get_data = IBus()
    #     get_data.readData()

    # except KeyboardInterrupt:
    #     print("\nSerial connection closed.")

    # finally:
    #     if get_data.serial:
    #         get_data.serial.close()
    #         print("Seriële verbinding gesloten.")
