from led import Led
import serial
import struct
import time


class ReceiverData:

    # Initialisatie van de ReceiverData-klasse.
    # Deze klasse leest gegevens van een iBUS-ontvanger via de seriële poort.
    def __init__(self, url="/dev/serial0", baudrate=115200, timeout=1):
        # Sla de seriële configuratie op
        self.url = url  # Seriële poort, standaard voor Raspberry Pi is /dev/serial0
        self.baudrate = baudrate  # Baudrate voor iBUS, altijd 115200
        self.timeout = timeout  # Timeout voor seriële verbinding, stopt lezen na 1 seconde als er geen data is
        
        # Initialisatie van de LED-controller
        self.led = Led()
        # self.min_byte_waarde = 1000
        # self.max_byte_waarde = 2000

        # Probeer de seriële poort te openen en te initialiseren
        try:
            self.serial = serial.Serial(self.url, self.baudrate, timeout=self.timeout)
            print(f"Verbonden met {self.url} op {self.baudrate} baud")
            self.serial.reset_input_buffer()  # Leeg de invoerbuffer om oude data te verwijderen

        except serial.SerialException as e:
            # Foutmelding als de verbinding niet tot stand komt
            print(f"Kan seriële verbinding niet openen: {e}")
            self.serial = None  # Zorg ervoor dat de verbinding als mislukt wordt gemarkeerd

    # Methode om data te lezen van de iBUS-ontvanger
    def readData(self):
        # Controleer of er een geldige seriële verbinding is
        if self.serial is None:
            print("Geen actieve seriële verbinding. Stoppen...")
            return

        # Blijvende lus om continu data van de ontvanger te lezen
        while True:
            try:
                # Wacht tot er minstens 32 bytes in de buffer zitten (iBUS-pakketgrootte)
                while self.serial.in_waiting < 32:
                    time.sleep(0.01)  # Korte pauze om CPU-belasting te verminderen

                # Lees 32 bytes uit de seriële poort
                data = self.serial.read(32)

                # Controleer of het ontvangen pakket geldig is: 32 bytes en start met 0x20 0x40
                if data[0] == 0x20 and data[1] == 0x40 and len(data) == 32:
                    # Pak de 14 kanalen uit het pakket (2 bytes per kanaal, little-endian volgorde)
                    channels = struct.unpack("<14H", data[2:30])
                    # print(f"Channels: {channels}")
                    print(f"\033[91mCH1: {channels[0]}\033[0m, \033[94mCH2: {channels[1]}\033[0m")

                    # Zet de LED aan of uit op basis van de kanaalwaarden
                    self.led.zetLedAan(channels)
                else:
                    # Als het pakket ongeldig is, leeg dan de buffer en probeer opnieuw
                    print("Ongeldige iBUS data ontvangen of verkeerde lengte")
                    self.serial.reset_input_buffer()

                # Zeer korte pauze om CPU-belasting te verminderen, zonder pakketten te missen
                time.sleep(0.001)

            except Exception as e:
                # Foutafhandeling: toon foutmelding, reset de buffer en probeer opnieuw
                print(f"Fout tijdens uitlezen van iBUS data: {e}")
                self.serial.reset_input_buffer()
                time.sleep(1)  # Wacht 1 seconde voordat opnieuw geprobeerd wordt

    # Placeholder voor toekomstige schrijffunctionaliteit
    def writeData(self):
        pass


# Zorg dat het script zelfstandig kan worden uitgevoerd
if __name__ == "__main__":
    try:
        # Maak een object aan en start het leesproces
        get_ibus_data = ReceiverData()
        channels = get_ibus_data.readData()
    except Exception as e:
        # Toon een foutmelding als het script crasht
        print(f"Error: {e}")
