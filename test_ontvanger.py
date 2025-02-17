from gpiozero import LED 
import serial  
import struct

channel_leds = {
    0: {"pin": 17, "name": "Throttle"},
    1: {"pin": 27, "name": "Aileron"},
    2: {"pin": 22, "name": "Elevator"},
    3: {"pin": 23, "name": "Rudder"},
}

# Maak een nieuwe dictionary dat is gebaseerd op de channel_leds dictionary 
# Dus het pakt de nummer van de pin en zet het weer in een dictionary met { 0: LED(17)}
leds = {}
for channel, data in channel_leds.items():
    leds[channel] = LED(data["pin"])

# THRESHOLD van een rc receiver is tussen de 1000 en de 2000
THRESHOLD_ON = 1510   
THRESHOLD_OFF = 1490  

# Maakt een serial connection om de iBus te lezen met de default BAUD_RATE van 115200
ser = serial.Serial("/dev/serial2", 115200, timeout=0.1)


def control_leds(channel_values):
    for channel, data in channel_leds.items():
        # Deze pakt op basis van de keys van channel_leds de jusite channel van leds
        led = leds[channel]  
        channel_name = data["name"] 
        value = channel_values[channel]  

        if value > THRESHOLD_ON:
            led.on()
            # print(f"Channel {channel + 1} ({channel_name}) is ON (Value: {value})")
        elif value < THRESHOLD_OFF:
            led.off()
            # print(f"Channel {channel + 1} ({channel_name}) is OFF (Value: {value})")


def read_ibus():
    while True:
        # Checked of er wel genoeg data is voor de serial buffer
        # Een iBus-pakket is 32 bytes groot dus kleiner dan dat is het geen ibus pakket
        if ser.in_waiting >= 32:  
            # Nu leest het de 32 bytes van de serial buffer
            data = ser.read(32)  

            # 2 header bytes (0x20 en 0x40) is ook alleen gebruikt in ibus
            # 14 channels (2 bytes per channel) = 28 bytes
            # 2 checksum bytes (voor foutdetectie)
            if data[0] == 0x20 and data[1] == 0x40:
                # 14 waardes van type H (unsigned short, 2 bytes per waarde) en de < voor de volgorde dus het kijkt eerst naar de minste waarde
                channel_values = struct.unpack('<14H', data[2:30])
                print(f"Channel Values: {channel_values}")  

                control_leds(channel_values)

try:
    read_ibus()
except KeyboardInterrupt:
    ser.close()  
    print("\nSerial connection closed.")
