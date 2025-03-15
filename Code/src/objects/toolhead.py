import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(pp)

from drivers.controlboard_driver import ControlBoard

class Toolhead():
    def __init__(self, control_board: ControlBoard):
        self.control_board = control_board
        
    def move_axis(self, axis: str, distance_mm: float, relative: bool = False, finish_move: bool = True):
        self.control_board.move_axis(axis, distance_mm, 300, relative)
        
        if finish_move:
            self.control_board.finish_moves()
        
    def get_position(self, axis):
        return self.control_board.positions[axis]
    
    
