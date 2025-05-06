import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(pp)
import logging
from drivers.controlboard_driver import ControlBoard
from gpiozero import AngularServo
from dataclasses import dataclass
from time import sleep

# TODO add data class representing each pippete? max volume, max dispense distance, full eject distance, last used fluid? etc
@dataclass
class Pipette:
    MAX_VOLUME_UL: int # the maximum volume the pipette is capable of drawing
    PLUNGER_TOP_MM: float # location where the actuator is just above the plunger
    PLUNGER_BOTTOM_MM: float # location where the actuator presses the plunger to its limit
    PLUNGER_FLUSH_MM: float
    NEEDS_BIG_TIP: bool 
    

class PipetteHandler():
    ACTUATOR_MAX_HEIGHT_MM: int
    STAND_0_Y: float = 85
    STAND_1_Y: float = 151
    def __init__(self, control_board: ControlBoard, tip_eject_servo: AngularServo, grabber_servo: AngularServo, pipettes: list):
        self.logger = logging.getLogger("Main Logger")
        
        self.control_board = control_board
        self.tip_eject_servo = tip_eject_servo
        self.grabber_servo = grabber_servo
        self.pipettes = pipettes
        
        self.current_pipette: Pipette = None
        self.current_fluid_volume_ul = 0
        
    def set_pipette(self, index: int = None):
        """Set the currently held pipette. Use without an index to remove currently held pipette"""
        if index is None:
            self.current_pipette = None
        
        if index > len(self.pipettes):
            return
        
        self.current_pipette = self.pipettes[index]
        
    def get_pippete_index(self):
        """Return the currently held pippete index"""
        if self.current_pipette is not None:
            return self.pipettes.index(self.current_pipette)
        else:
            return None
        
    def home(self):
        self.control_board.send_message("G28 B")
        
    def set_actuator_position(self, position_mm):
        
        self.control_board.move_axis("B", position_mm)
        
    def flush_pippete(self):
        """Presses the pippete beyond its normal limit to ensure all fluid is purged.
            The actuator then returns to the bottom of the plunger"""
        self.control_board.move_axis("B", self.current_pipette.PLUNGER_FLUSH_MM, 300)
        
        self.current_fluid_volume_ul = 0
    
    def dispense_all(self, duration_s: float):
        """Move the actuator to depress the plunger until it reaches the bottom (wihtout flushing)"""
        #calculate feedrate
        current_position = self.control_board.positions["B"]
        feed_rate = 60*(current_position - self.current_pipette.PLUNGER_BOTTOM_MM) / duration_s
        # press plunger down to minimum height, ejecting all fluid
        self.control_board.move_axis("B", self.current_pipette.PLUNGER_BOTTOM_MM, feed_rate)
        self.current_fluid_volume_ul = 0
        
    def draw_ul(self, volume_ul):
        """ Raises the actuator so that the specified volume is drawn. Cannot draw past max volume. 
        Draws are persistant, so when draw_ul is called twice without dispensing, the total fluid is compounded...?"""
        if self.current_fluid_volume_ul + volume_ul > self.current_pipette.MAX_VOLUME_UL:
            self.logger.warning(f"Cannot draw above {self.current_pipette.MAX_VOLUME_UL}, attempted to draw to {self.current_fluid_volume_ul + volume_ul}")
            return
            
        ul_per_mm = self.current_pipette.MAX_VOLUME_UL/(self.current_pipette.PLUNGER_TOP_MM - self.current_pipette.PLUNGER_BOTTOM_MM)
        self.current_fluid_volume_ul += volume_ul
        self.control_board.move_axis("B",  volume_ul*ul_per_mm, relative=True)
        
    def eject_tip(self):
        self.tip_eject_servo.angle = 160
        sleep(1)
        self.tip_eject_servo.angle = 0
         
    def set_eject_angle(self, angle: int):
        self.tip_eject_servo.angle = angle
        
    def set_grabber_angle(self, angle: int):
        self.grabber_servo.angle = angle
    def open_grabber(self):
        self.grabber_servo.angle = 180
        
    def close_grabber(self):
        self.grabber_servo.angle = 80
        
    def detatch_servos(self):
        self.tip_eject_servo.detach()
        self.tip_eject_servo.detach()
        
        
        
class TipHolder():
    def __init__(self):
        self.rows = 5
        self.columns = 10
        

        
if __name__ == "__main__":
    
    # ph = PipetteHandler(None, None, None, 5)
    p = Pipette(
        MAX_VOLUME_UL=1000,
        PLUNGER_TOP_MM=155,
        PLUNGER_BOTTOM_MM=35,
        PLUNGER_BASE_MM=8,
        DISPENSED_UL_PER_MM=5)
    
    tip_eject_servo = None
    pipette_holder_servo = None
    pipette_system = PipetteHandler(None, tip_eject_servo, pipette_holder_servo, [p])
    