
from controlboard_driver import ControlBoard
from servo_driver import mServo
from dataclasses import dataclass
from time import sleep

# TODO add data class representing each pippete? max volume, max dispense distance, full eject distance, last used fluid? etc
@dataclass
class Pipette:
    MAX_VOLUME_UL: int
    ul_dispensed_per_mm: int
    last_fluid: str = None
    

class PipetteHandler():
    
    def __init__(self, control_board: ControlBoard, tip_eject_servo: mServo, hold_pipette_servo: mServo, pipettes: list):
        self.control_board = control_board
        self.tip_eject_servo = tip_eject_servo
        self.hold_pipette_servo = hold_pipette_servo
        self.pipettes = pipettes
        
        
        self.pipette = None
        self.volume_ul
        
    def extract(self, volume_ul: int):
        # assuming actuyator is right at plunger without depressing
        # press plunger to volume_ul
        # lower?
        # depress plunger and raise
        pass
    
    def dispense_all(self, duration_seconds: float):
        # assuming actuyator is right at plunger without depressing
        # press plunger to max volume
        # go past to ensre all fluid is out
        pass
    
    def dock_pipette(self):
        pass
    
    def eject_tip(self):
        self.tip_eject_servo.set_angle(30)
        sleep(0.5)
        self.tip_eject_servo.set_angle(0)
        
        

        
if __name__ == "__main__":
    
    # ph = PipetteHandler(None, None, None, 5)
    p = Pipette(5, 5, "been")
    print(p)
    p.MAX_VOLUME_UL = 4
    
    print(p)