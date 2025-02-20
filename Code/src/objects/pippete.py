import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(pp)

from drivers.controlboard_driver import ControlBoard
from gpiozero import AngularServo
from dataclasses import dataclass
from time import sleep

# TODO add data class representing each pippete? max volume, max dispense distance, full eject distance, last used fluid? etc
@dataclass
class Pipette:
    MAX_VOLUME_UL: int # the maximum volume the pipette is capable of drawing
    PLUNGER_TOP_MM: int # location where the actuator is just above the plunger
    PLUNGER_BOTTOM_MM: int # location where the actuator presses the plunger to its limit
    DISPENSED_UL_PER_MM: int
    last_fluid: str = None
    

class PipetteHandler():
    
    def __init__(self, control_board: ControlBoard, tip_eject_servo: AngularServo, hold_pipette_servo: AngularServo, pipettes: list):
        self.control_board = control_board
        self.tip_eject_servo = tip_eject_servo
        self.hold_pipette_servo = hold_pipette_servo
        self.pipettes = pipettes
        
        
        
        self.current_pipette: Pipette = None
        self.volume_ul
        self.current_position_mm = 0
        
    def set_pipette(self, index: int):
        if index > len(self.pipettes):
            return
        
        self.current_pipette = self.pipettes[index]
        
    def extract(self, volume_ul: int):
        
        # calculate the distance needed to push out specified volume
        distance_mm = volume_ul / self.current_pipette.DISPENSED_UL_PER_MM
        
        # go to top of plunger
        self.control_board.move_axes(["A"], self.current_pipette.PLUNGER_TOP_MM, 300, False)
        # pre-depress plunger
        self.control_board.move_axes(["A"], -distance_mm, 300, True)
        #lower into vial
        self.control_board.move_axes(["Y"], -10, 300, True)
        #un press plunger
        self.control_board.move_axes(["A"], distance_mm, 300, True)
        #raise out of vial
        self.control_board.move_axes(["Y"], 10, 300, True)
        
        self.current_position_mm = self.current_pipette.PLUNGER_TOP_MM-distance_mm

    
    def dispense_all(self, duration_s: float):
        
        #calculate feedrate
        feed_rate = (self.current_position_mm - self.current_pipette.PLUNGER_BOTTOM_MM) / duration_s
        # press plunger down to minimum height, ejecting all fluid
        self.control_board.move_axes("A", self.current_pipette.PLUNGER_BOTTOM_MM, feed_rate, False)
        # press plunger beyond min height. Our plungers have a function where you can press farther to ensure all fluid is out
        self.control_board.move_axes("A", -10, 300, True)
        
        #return to top of plunger
        self.control_board.move_axes("A", self.current_pipette.PLUNGER_TOP_MM, 300, False)
        
        self.current_position_mm = self.current_pipette.PLUNGER_TOP_MM
    
    def dock_pipette(self):
        pass
    
    def eject_tip(self):
        self.tip_eject_servo.angle = 30
        sleep(0.5)
        self.tip_eject_servo.angle = 0
        
    def detatch_servos(self):
        self.tip_eject_servo.detach()
        self.tip_eject_servo.detach()

        
if __name__ == "__main__":
    
    # ph = PipetteHandler(None, None, None, 5)
    p = Pipette(
        MAX_VOLUME_UL=1000,
        PLUNGER_TOP_MM=155,
        PLUNGER_BOTTOM_MM=35,
        DISPENSED_UL_PER_MM=5)
    
    tip_eject_servo = None
    pipette_holder_servo = None
    pipette_system = PipetteHandler(None, tip_eject_servo, pipette_holder_servo, [p])
    