import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(pp)

from drivers.controlboard_driver import ControlBoard

class Toolhead():
    def __init__(self, control_board: ControlBoard):
        self.control_board = control_board
        
    def move_axis(self, axis: str, distance_mm: float, relative: bool = False, finish_move: bool = True):
        self.control_board.move_axis(axis, distance_mm, 1000, relative=relative, finish_move=finish_move)
        
    def get_position(self, axis):
        return self.control_board.positions[axis]
    
    def home(self):
        self.control_board.send_message("G28 Z")
        self.control_board.send_message("G28 Y")
        self.control_board.send_message("G28 X")

