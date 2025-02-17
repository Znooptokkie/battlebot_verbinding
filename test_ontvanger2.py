from gpiozero import LED, Servo
import serial  
import struct
from time import sleep  

pins_leds = [
     {"pin": 17,}, 
     {"pin": 27,},
     {"pin": 22,},
     {"pin": 23,},
]

pin_servo = 6

THRESHOLD_ON = 1502   
THRESHOLD_OFF = 1498  


ser = serial.Serial("/dev/serial0", 115200, timeout=1)


def control_leds(channel_values):
    for channel, data in enumerate(pins_leds):
        led = LED(data["pin"])
        print(f"{channel_values }") 

        value = channel_values[channel] 

        if value > THRESHOLD_ON:
            led.on()
        elif value < THRESHOLD_OFF:
            led.off()


def read_ibus():
    while True:
        if ser.in_waiting >= 32:  
            data = ser.read(32)  

            if data[0] == 0x20 and data[1] == 0x40:
                channel_values = struct.unpack('<14H', data[2:30])
                
                control_leds(channel_values)
                



try:
    read_ibus()
except KeyboardInterrupt:
    ser.close()  
    print("\nSerial connection closed.")


# ----------------------------------------------
# def control_servo(channel_values) -> any:

#         servo = Servo(pin_servo)
#         value = channel_values[3]
#         print(f"{value}")

#         if value > THRESHOLD_ON:
#             servo.max()
#         elif value < THRESHOLD_OFF:
#             servo.detach()

