from drivers.spincoater_driver import SpinCoater
from drivers.controlboard_driver import ControlBoard
from drivers.dac_driver import DAC


from time import sleep
from inspect import signature
import logging


MAX_TEMPERATURE = 540 # TODO move to constants later

class Dispatcher():
    def __init__(self, logger: logging.Logger, control_board: ControlBoard, spincoater: SpinCoater, dac: DAC):
        self.logger = logger
        self.control_board = control_board
        self.spincoater = spincoater
        self.dac = dac

        self.move_dict = {
            "log": self.log,
            "wait": self.wait,
            "goto": self.move_toolhead,
            "echo": self.echo_controlboard,
            "gcode": self.control_board.send_message,
            "set_temp": self.set_temperature,
            "wait_for_temp": self.wait_for_temperature
        }
    
    def validate_moves(self, moves: list) -> bool:
        """Validates a list of moves by checking if the move exists in the dispatcher.
        Also checks if the number of args is correct

        ### Args:
            moves (list): _description_

        ### Returns:
            bool: returns True if all moves are valid, False otherwise
        """
        valid = True

        if not moves:
            self.logger.error("No moves found")
            return False

        for index, move in enumerate(moves):
            func_name = move[0]
            func_args = move[1:]

            if func_name not in self.move_dict:
                self.logger.error(f"Function #{index},{func_name} not found in dispatcher")
                valid = False

            func = self.move_dict[func_name]
            try:
                sig = signature(func)
                sig.bind(*func_args)
            except TypeError as e:
                self.logger.error(f"Function #{index}, \"{func_name}\" has incorrect arguments: {e}")  
                valid = False

        return valid
    
    
    # controlboard tasks
    def move_toolhead(self, x: float, y: float, z: float, speed: int = 1000):
        """Move the toolhead to the specified coordiantes """
        self.control_board.send_message(f"G0 X{x} Y{y} Z{z} F{speed}")
        self.control_board.finish_move()
    
    def echo_controlboard(self, message: str):
        """ Make the control board echo a message """
        self.control_board.send_message(f"M118 {message}")
    
    # hotplate tasks
    def set_temperature(self, temperature: int):
        """ Set the hotplate to the specified temperature in degrees celcius"""
        
        if temperature > MAX_TEMPERATURE:
            temperature = MAX_TEMPERATURE
        if temperature < 0:
            temperature = 0
            
        level = float(temperature/MAX_TEMPERATURE)
        self.dac.setVoltageLevel(level)
    
    def wait_for_temperature(self, target_temperature: int, threshold: int = 1):
        """Waits until target temperature is met within the threshold"""
        
        while abs(self.control_board.get_temperature - target_temperature) > threshold:
            self.logger.debug(f"Waiting to reach {target_temperature}C")
            sleep(1)
            
    # TODO add spincoater tasks
    def add_spincoater_step(self, rpm: int, spin_time_seconds: int):
        """ Command the spincoater to spin at a specified speed for a specified time"""
        
        self.spincoater.send_message(f"spc add step {rpm} {spin_time_seconds}")
    
    
    # TODO add vial carousel tasks
    
    # TODO add kill commands
    
    # general tasks
    def log(self, message: str):
        """ Log the specified message"""
        self.logger.info(message)

    def wait(self, wait_time_seconds: int):
        """ Wait for the specified amount of time"""
        self.logger.info(f"Waiting for {wait_time_seconds} seconds")
        sleep(wait_time_seconds)

