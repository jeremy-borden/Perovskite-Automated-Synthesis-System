from objects.gripper import Gripper
from drivers.camera_driver import Camera
from drivers.spincoater_driver import SpinCoater
from drivers.controlboard_driver import ControlBoard
from drivers.dac_driver import DAC
from image_processing import ImageProcessor

from time import sleep
from inspect import signature
import logging


MAX_TEMPERATURE = 540 # TODO move to constants later

class Dispatcher():
    def __init__(self, logger: logging.Logger, control_board: ControlBoard, spincoater: SpinCoater, hotplate, camera: Camera, gripper: Gripper):
        self.logger = logger
        self.control_board = control_board
        self.spincoater = spincoater
        self.camera = camera
        self.gripper = gripper
        self.hotplate = hotplate
        
        ImageProcessor.set_detector()

        self.move_dict = {
            "log": self.log,
            "wait": self.wait,
            "goto": self.move_toolhead,
            "gcode": self.control_board.send_message,
            "set_temp": self.hotplate.set_temperature,
            "wait_for_temp": self.hotplate.wait_for_temperature,
            "align_gripper": self.align_gripper,
            "open_gripper": self.gripper.open,
            "close_gripper": self.gripper.close,
            "set_angle_gripper": self.gripper.set_arm_angle
            
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
    
    
    def kill(self):
        self.control_board.kill()
        self.spincoater.stop()
        self.spincoater.clear_steps()
        self.gripper.detatch_servos()
    
    # controlboard tasks
    def move_toolhead(self, x: float, y: float, z: float, speed: int = 1000):
        """Move the toolhead to the specified coordiantes """
        self.control_board.send_message(f"G0 X{x} Y{y} Z{z} F{speed}")
        self.control_board.finish_move()

    # TODO add spincoater tasks
    def add_spincoater_step(self, rpm: int, spin_time_seconds: int):
        """ Command the spincoater to spin at a specified speed for a specified time"""
        
        self.spincoater.add_step(rpm, spin_time_seconds)
    
    def align_gripper(self):
        sleep(1) # wait for machine to settle
        
        frame = self.camera.get_frame()
        angle = ImageProcessor.get_marker_angles(image=frame, marker_id=3)
        self.gripper.set_arm_angle(angle)
    
    # TODO add vial carousel tasks
    
    # general tasks
    def log(self, message: str):
        """ Log the specified message"""
        self.logger.info(message)

    def wait(self, wait_time_seconds: int):
        """ Wait for the specified amount of time"""
        self.logger.info(f"Waiting for {wait_time_seconds} seconds")
        sleep(wait_time_seconds)
