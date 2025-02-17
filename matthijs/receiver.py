import struct
import serial

class Receiver:
    channel_values = []
    ser = serial.Serial("/dev/serial0", 115200, timeout=1)
    
    @classmethod
    def read_ibus(cls):
        try:
            available_bytes = cls.ser.in_waiting
            print(f"Bytes available: {available_bytes}")  # Print number of bytes in the buffer
            if available_bytes >= 32:
                data = cls.ser.read(32)
                print(f"Raw data: {data}")  # Debugging line to print raw data
                if data[0] == 0x20 and data[1] == 0x40:
                    cls.channel_values = struct.unpack('<14H', data[2:30])
                    print(f"GELUKYT!!!: {cls.channel_values}")
                else:
                    print(f"Header mismatch: {data[0]} {data[1]}")
            else:
                print("Not enough data")
        except Exception as e:
            print(f"Error in read_ibus: {e}")
        return []

if __name__ == "__main__":
    try:
        get_data = Receiver.read_ibus()
        print(f"T!!!: {Receiver.channel_values}")
    except Exception as e:
        print(f"Error in main block: {e}")
