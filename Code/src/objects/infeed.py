from gpiozero import AngularServo

class Infeed():
    def __init__(self, servo: AngularServo):
        self.servo = servo
        
    def close(self):
        self.servo.angle = 180
        
    def open(self):
        self.servo.angle = 0
    
    def set_angle(self, angle):
        self.servo.angle = angle