from gpiozero import Servo

class ServoMotor:
    pin_servo = 13
    threshold_on = 1502
    threshold_off = 1498

    @staticmethod
    def control_servo(channel_values):
        servo = Servo(ServoMotor.pin_servo)
        value = channel_values[3]

        if value > ServoMotor.threshold_on:
            servo_value = (value - 1500) / 500 
            servo.value = servo_value
            print(f"Setting servo to {servo_value}")
        else:
            servo.detach()
