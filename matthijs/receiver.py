import struct
import serial
from time import sleep

class ReceiverInit:
    def __init__(self, url="/dev/serial0", baudrate=115200, timeout=1):
        self.url = url  
        self.baudrate = baudrate  
        self.timeout = timeout

        try:
            self.serial = serial.Serial(self.url, self.baudrate, timeout=self.timeout)
            print(f"Verbonden met {self.url} op {self.baudrate} baud")
            self.serial.reset_input_buffer() 

        except serial.SerialException as e:
            print(f"Kan seriële verbinding niet openen: {e}")
            self.serial = None

    def getSerialConnection(self):
        return self.serial

class Receiver:
    serial_init = ReceiverInit()
    serial = serial_init.getSerialConnection()

    @classmethod
    def readData(cls, control_instance):
        while True:
            try:
    
                if cls.serial.in_waiting >= 32:
                    data = cls.serial.read(32)
                    
                    if len(data) == 32 and data[0] == 0x20 and data[1] == 0x40:
                        channels = struct.unpack('<14H', data[2:30])
                        # print(f"Channels: {channels}")
                        control_instance.run(channels)

                    else:
                        print(f"Header mismatch: {data[0] if len(data) > 0 else 'N/A'} {data[1] if len(data) > 1 else 'N/A'}")
                        cls.serial.reset_input_buffer()
                    
                    sleep(0.001)
    
            except Exception as e:
                print(f"Error in readData: {e}")
                cls.serial.reset_input_buffer()
                sleep(1)

if __name__ == "__main__":
    try:
        # get_data = Receiver.read_ibus()

        call_receiver = Receiver()
        get_data = call_receiver.readData()
    except Exception as e:
        print(f"Error in main block: {e}")
