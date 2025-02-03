
class Toolhead():
    def __init__(self, control_board):
        self.control_board = control_board
        
    def move_to(self, x: float, y: float, z: float, speed: int):
        self.control_board.send_message
