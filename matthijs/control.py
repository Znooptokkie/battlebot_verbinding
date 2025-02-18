from leds import Leds
from servo_motor import ServoMotor
from receiver import Receiver

class Control:
    def __init__(self):
        self.leds = Leds
        self.servo_motor = ServoMotor

    def run(self, channel_values):    
        if channel_values:
            # print(f"{channel_values}")
            Leds.controlLeds(channel_values)
            # ServoMotor.controlServo(channel_values)

if __name__ == "__main__":
    control = Control()
    Receiver.readData(control) 