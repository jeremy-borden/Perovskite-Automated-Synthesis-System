from gpiozero import AngularServo

class Gripper():
    def __init__(self, arm_servo: AngularServo, finger_servo:AngularServo):
        self.arm_servo = arm_servo
        self.finger_servo = finger_servo
        
    def open(self):
        self.finger_servo.angle = 22
    
    def close(self):
        self.finger_servo.angle = 2
    
    def set_arm_angle(self, angle_degrees: int):
        self.arm_servo.angle = angle_degrees
        
    def set_finger_angle(self, angle_degrees: int):
        self.finger_servo.angle=angle_degrees
        
    def detatch_servos(self):
        self.arm_servo.detach()
        self.finger_servo.detach()
        