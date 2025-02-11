from gpiozero import LED
import serial
import struct
from time import sleep

# GPIO-instellingen
LED_PIN = 18
led = LED(LED_PIN)
THRESHOLD = 1500

# Seriële poort openen
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def read_ibus():
    while True:
        if ser.in_waiting >= 32:  # iBUS-bericht heeft 32 bytes
            data = ser.read(32)
            if data[0] == 0x20 and data[1] == 0x40:  # iBUS-header check
                channels = struct.unpack('<14H', data[2:30])  # 14 kanalen
                print(f"Channels: {channels}")

                # Controleer bijvoorbeeld kanaal 5 (index 4)
                if channels[4] > THRESHOLD:
                    led.on()
                else:
                    led.off()

        sleep(0.05)  # Vermijd overbelasting van CPU

try:
    read_ibus()
except KeyboardInterrupt:
    ser.close()
    print("\nSerial connection closed.")
