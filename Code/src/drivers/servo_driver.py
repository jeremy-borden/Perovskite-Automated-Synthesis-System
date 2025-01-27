from gpiozero import Servo

class mServo():
    def __init__(self, pin: int, min_pulse_width: int, max_pulse_width: int, max_angle: int):
        self.max_angle = max_angle
        #self.servo = Servo(pin=pin, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width, max_angle=max_angle)
        
        
        
        
    def set_angle(self, angle: int):
        """Sets the servo angle. Clamps values below 0 and above max angle"""
        
        value=angle* (2/self.max_angle) -1
        
        # clamp value
        if value < -1:
            value=-1
        if value > 1:
            value = 1
        
        print(value)
        #self.servo.value = value
        
    def set_value(self, value: float):
        
        # convert 0-1 range into -1 to 1 range
        value = value*2 -1
        
        # clamp value
        if value < -1:
            value=-1
        if value > 1:
            value = 1
        
        #self.servo.value=value

if __name__ == "__main__":
    servo = mServo(1, 1, 1, 180)
    servo.set_angle(181)
       
        