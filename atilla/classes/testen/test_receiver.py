from test_led import Led
from test_control import Control
import serial
import struct
import time






class ReceiverInit:
    def __init__(self, url="/dev/serial0", baudrate=115200, timeout=1):
        self.url = url  
        self.baudrate = baudrate  
        self.timeout = timeout
        # self.serial = ""

        try:
            self.serial = serial.Serial(self.url, self.baudrate, timeout=self.timeout)
            print(f"Verbonden met {self.url} op {self.baudrate} baud")
            self.serial.reset_input_buffer() 

        except serial.SerialException as e:
            print(f"Kan seriële verbinding niet openen: {e}")
            self.serial = None

    def getSerialConnection(self):
        return self.serial







class ReceiverData:
    serial_init = ReceiverInit()
    serial = serial_init.getSerialConnection()                             
    # led = Led()
    control = Control()

    @classmethod
    def readData(cls):
        if cls.serial is None:
            print("Geen actieve seriële verbinding. Stoppen...")
            return

        while True:
            try:
                while cls.serial.in_waiting < 32:
                    time.sleep(0.01) 

                data = cls.serial.read(32)

                if data[0] == 0x20 and data[1] == 0x40 and len(data) == 32:

                    channels = struct.unpack("<14H", data[2:30])
                    # print(f"Channels: {channels}")
                    # print(f"\033[91mCH1: {channels[0]}\033[0m, \033[94mCH2: {channels[1]}\033[0m")

                    # cls.led.zetLedAan(channels)
                    cls.control.run(channels)
                else:
                    print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                    cls.serial.reset_input_buffer()

                time.sleep(0.001)

            except Exception as e:
                print(f"Fout tijdens uitlezen van iBUS data: {e}")
                cls.serial.reset_input_buffer()
                time.sleep(1) 

    def writeData(self):
        pass

if __name__ == "__main__":
    try:
        get_ibus_data = ReceiverData()
        channels = get_ibus_data.readData()
    except Exception as e:
        print(f"Error: {e}")
