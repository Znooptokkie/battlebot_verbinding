from receiver import Receiver
from leds import Leds
from servo_motor import ServoMotor

class Controller:
    def __init__(self):
        self.receiver = Receiver
        self.leds = Leds
        self.servo_motor = ServoMotor

    def run(self):
        Leds.setup_leds()
        
        while True:
            channel_values = Receiver.read_ibus()
            print(f"{channel_values}")
            if channel_values:
                Leds.control_leds(channel_values)
                ServoMotor.control_servo(channel_values)
