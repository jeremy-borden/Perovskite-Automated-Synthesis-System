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
    last_fluid: str = None
    

class PipetteHandler():
    ACTUATOR_MAX_HEIGHT_MM: int
    
    def __init__(self, logger: logging.Logger, control_board: ControlBoard, tip_eject_servo: AngularServo, grabber_servo: AngularServo, pipettes: list):
        self.control_board = control_board
        self.tip_eject_servo = tip_eject_servo
        self.grabber_servo = grabber_servo
        self.pipettes = pipettes
        self.logger = logger
        
        self.current_pipette: Pipette = None
        self.current_fluid_volume_ul = 0
        
    def set_pipette(self, index: int):
        if index > len(self.pipettes):
            return
        
        self.current_pipette = self.pipettes[index]
        
    def get_pippete(self):
        """Return the currently held pippete"""
        return self.current_pipette
        
    def set_actuator_position(self, position_mm, speed):
        # dont allow actuator to go too far away
        if position_mm > self.ACTUATOR_MAX_HEIGHT_MM:
            return
        # dont allow actuator to go past the flush height if there is a pippete
        if self.current_pipette is not None and position_mm < self.current_pipette.PLUNGER_FLUSH_MM:
            return
        
        self.control_board.move_axis("B", position_mm, speed, False)
        
    # def set_actuator_position_ul(self, position_ul , feedrate):
    #     if position_ul > self.current_pipette.MAX_VOLUME_UL or position_ul < 0:
    #         return
        
        
    #     ul_per_mm = self.current_pipette.MAX_VOLUME_UL/(self.current_pipette.PLUNGER_TOP_MM - self.current_pipette.PLUNGER_BOTTOM_MM)
    #     self.current_fluid_volume_ul += volume_ul
        
    #     self.control_board.move_axis("B",  volume_ul*ul_per_mm, feedrate)
        
    def flush_pippete(self):
        """Presses the pippete beyond its normal limit to ensure all fluid is purged.
            The actuator then returns to the bottom of the plunger"""
        self.control_board.move_axis("B", self.current_pipette.PLUNGER_FLUSH_MM, 300, False)
        self.control_board.move_axis("B", self.current_pipette.PLUNGER_BOTTOM_MM, 300, False)
        self.control_board.finish_moves()
        self.current_fluid_volume_ul = 0
    
    def dispense_all(self, duration_s: float):
        """Move the actuator to depress the plunger until it reaches the bottom (wihtout flushing)"""
        #calculate feedrate
        current_position = self.control_board.positions["B"]
        feed_rate = 60*(current_position - self.current_pipette.PLUNGER_BOTTOM_MM) / duration_s
        # press plunger down to minimum height, ejecting all fluid
        self.control_board.move_axis("B", self.current_pipette.PLUNGER_BOTTOM_MM, feed_rate, False)
        self.current_fluid_volume_ul = 0
        
    def draw_ul(self, volume_ul, feedrate):
        """ Raises the actuator so that the specified volume is drawn. Cannot draw past max volume. 
        Draws are persistant, so when draw_ul is called twice without dispensing, the total fluid is compounded...?"""
        if self.current_fluid_volume_ul + volume_ul > self.current_pipette.MAX_VOLUME_UL:
            self.logger.warning(f"Cannot draw above {self.current_pipette.MAX_VOLUME_UL}, attempted to draw to {self.current_fluid_volume_ul + volume_ul}")
            return
            
        ul_per_mm = self.current_pipette.MAX_VOLUME_UL/(self.current_pipette.PLUNGER_TOP_MM - self.current_pipette.PLUNGER_BOTTOM_MM)
        self.current_fluid_volume_ul += volume_ul
        self.control_board.move_axis("B",  volume_ul*ul_per_mm, feedrate, True)
        
    def eject_tip(self):
        self.tip_eject_servo.angle = 30
        sleep(0.5)
        self.tip_eject_servo.angle = 0
         
    def open_grabber(self):
        self.grabber_servo.angle = 0
        
    def close_grabber(self):
        self.grabber_servo.angle = 180
        
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
    