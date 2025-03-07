import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(pp)

from drivers.controlboard_driver import ControlBoard

class Toolhead():
    def __init__(self, control_board: ControlBoard):
        self.control_board = control_board
        
    def set_position(self, x_mm: float, y_mm: float, z_mm: float):
        self.control_board.move_axis("X", x_mm, 500)
        self.control_board.move_axis("Y", y_mm, 500)
        self.control_board.move_axis("Z", z_mm, 300)
        self.control_board.finish_moves()