from tkinter.tix import MAX
from drivers.controlboard_driver import ControlBoard
from drivers.dac_driver import DACDriver

MAX_TEMPERATURE = 540
class Hotplate:
    def __init__(self, dac: DACDriver, control_board: ControlBoard):
        self.dac = dac
        self.control_board = control_board
        
        self.current_temperature = 0
        self.target_temperature = 0
        
        
    def setTemperature(self, temperature):
        if( temperature > MAX_TEMPERATURE or temperature < 0):
            return
        
        self.target_temperature = temperature
        self.dac.setVoltageLevel(temperature / MAX_TEMPERATURE)
        
    def readTemperature(self):
        self.control_board.sendGCode("M105", True)