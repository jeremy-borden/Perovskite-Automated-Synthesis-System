from drivers.controlboard_driver import ControlBoard
from gpiozero import AngularServo

class VialCarousel():
    def __init__(self, control_board: ControlBoard, lid_servo: AngularServo):
        self.control_board = control_board
        self.lid_servo = lid_servo
        
        self.current_vial = 0
        self.vial_volumes = [0]*12
        
    def open_lid(self):
        self.lid_servo.value=180
        
    def close_lid(self):
        self.lid_servo.value=0
         
    def set_vial(self, vial_num):
        self.open_lid()
        self.control_board.move_axis("A", 30*(self.current_vial - vial_num), 100)
        
        self.current_vial = vial_num
        self.close_lid()