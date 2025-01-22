
from controlboard_driver import ControlBoard
from servo_driver import mServo
from dataclasses import dataclass

# TODO add data class representing each pippete? max volume, max dispense distance, full eject distance, last used fluid? etc
@dataclass
class Pipette:
    max_volume_ul: int
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
        
    def dispense(self, volume_ul: int):
        pass
    
    def dock_pipette(self):
        pass
        
        
        
        
if __name__ == "__main__":
    
    ph = PipetteHandler(None, None, None, 5)
        
        