from time import sleep
from inspect import signature
import logging

from objects.toolhead import Toolhead
from objects.hotplate import Hotplate
from objects.gripper import Gripper
from objects.infeed import Infeed
from objects.pippete import PipetteHandler
from objects.vial_carousel import VialCarousel

from drivers.camera_driver import Camera
from drivers.spincoater_driver import SpinCoater
from drivers.spectrometer_driver import Spectrometer

from image_processing import ImageProcessor

class Dispatcher():
    def __init__(self, spin_coater: SpinCoater, hotplate: Hotplate, 
                 camera: Camera, gripper: Gripper, infeed: Infeed, pippete_handler: PipetteHandler,
                 toolhead: Toolhead, vial_carousel: VialCarousel, spectrometer: Spectrometer):
        self.logger = logging.getLogger("Main Logger")
        
        self.toolhead = toolhead
        self.infeed = infeed
        self.pippete_handler = pippete_handler
        self.spin_coater = spin_coater
        self.camera = camera
        self.gripper = gripper
        self.hotplate = hotplate
        self.vial_carousel = vial_carousel
        self.spectrometer = spectrometer
        
        ImageProcessor.set_detector()

        self.move_dict = {
            "log": self.log,
            "wait": self.wait,
            "home": self.home,
            
            "move_toolhead": self.move_toolhead,
            
            "set_temperature": self.set_temperature,
            "wait_for_temperature": self.wait_for_temperature,
            
            "align_gripper": self.align_gripper,
            "open_gripper": self.open_gripper,
            "close_gripper": self.close_gripper,
            
            "set_angle_gripper": self.set_gripper_angle,
            
            "spin": self.spin,
            
            "open_infeed": self.open_infeed,
            "close_infeed": self.close_infeed,
            
            "extract": self.extract,

            "measure_spectrum": self.measure_spectrum,
            "automated_measurement": self.automated_measurement,
        }
        
        
        # procedure coordination info
        
        self.vial = 0
        
    
    def validate_moves(self, moves: list) -> bool:
        """Validates a list of moves by checking if the move exists in the dispatcher.
        Also checks if the number of args is correct
        ### Args:
            moves (list):
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

# --------- GENERAL MOVES --------
    def home(self):
        self.control_board.send_message("G28")
        self.gripper.open()
        
    def kill(self):
        self.control_board.kill()
        self.spin_coater.stop()
        self.spin_coater.clear_steps()
        self.gripper.detatch_servos()
        
    def log(self, message: str):
        """ Log the specified message"""
        self.logger.info(message)

    def wait(self, wait_time_seconds: int):
        """ Wait for the specified amount of time"""
        self.logger.info(f"Waiting for {wait_time_seconds} seconds")
        sleep(wait_time_seconds)
    
    #  --------- HOTPLATE MOVES --------
    def set_temperature(self, temperature_c: int):
        self.hotplate.set_temperature(temperature_c)
    
    def wait_for_temperature(self, target_temperature: int, threshold: int):
        while abs(self.hotplate.current_temperature_c - target_temperature) > threshold:
            sleep(1)

    # --------- TOOLHEAD MOVES --------
    def move_toolhead(self, x: float, y: float, z: float, speed: int = 1000):
        """Move the toolhead to the specified coordiantes """
        self.toolhead.set_position(x,y,z)

    # --------- SPIN COATER MOVES --------
    def spin(self, timelist, speedlist):
        self.spin_coater.clear_steps()
        for time, speed in zip(timelist, speedlist):
            self.spin_coater.add_step(speed, time)
        self.spin_coater.run() 
        
    def add_spincoater_step(self, rpm: int, spin_time_seconds: int):
        """ Command the spincoater to spin at a specified speed for a specified time"""
        
        self.spin_coater.add_step(rpm, spin_time_seconds)
        
    # --------- GRIPPER MOVES --------
    def open_gripper(self):
        self.gripper.open()
        
    def close_gripper(self):
        self.gripper.close()
    
    def set_gripper_angle(self, angle):
        self.gripper.set_arm_angle(angle)
    
    def align_gripper(self):
        frame = self.camera.get_frame()
        
        angle0 = None
        angle1 = None
        
        while(angle0 is None or angle1 is None) or abs(angle1-angle0) > 5:
            self.logger.debug("Getting first angle")
            frame = self.camera.get_frame()
            angle0 = ImageProcessor.get_marker_angles(image=frame, marker_id=7) % 90
            self.logger.info(f"Got Angle0: {int(angle0)}")
            sleep(1)
            self.logger.debug("Getting second angle")
            frame = self.camera.get_frame()
            angle1 = ImageProcessor.get_marker_angles(image=frame, marker_id=7) % 90
            self.logger.info(f"Got Angle1: {int(angle1)}")
            sleep(1)
            
        self.logger.info(int(angle0))
        self.gripper.set_arm_angle(int(angle0))
        
    def working_slide_to(self, location):
        """ pick up the slide currently being worked on and move it to the specified location"""
        
        
    # -------- PIPPETE MOVES --------
    def extract(self, volume_ul: int):
            """ Assuming we are at the vial carousel, the system will extract fluid.
            The gantry will "dip" into the vial by the amount specified"""
            #TODO add a current location and check if thats possible
            
            self.vial_carousel.remove_fluid(self.vial, volume_ul)
            
            self.toolhead.move_axis("Y", -10, relative=True)
            self.pippete_handler.draw_ul(volume_ul)
            self.toolhead.move_axis("Y", 10, relative=True)
            
    def extract_from_vial(self, volume_ul, vial_num: int):
        self.toolhead.move_axis("Z", 150) # move to top
        
        # TODO move over vial carousel opening
        self.toolhead.move_axis("X", None)
        self.toolhead.move_axis("Y", None)
        self.toolhead.move_axis("Z", None)
        
        self.vial_carousel.set_vial(vial_num)

        self.vial_carousel.remove_fluid(self.vial, volume_ul)
            
        self.toolhead.move_axis("Y", -10, relative=True)
        self.pippete_handler.draw_ul(volume_ul)
        self.toolhead.move_axis("Y", 10, relative=True)
        pass
            
    def dispense_to_vial(self, vial_num: int):
        self.toolhead.move_axis("Z", 150) # move to top
        
        # TODO move over vial carousel opening
        self.toolhead.move_axis("X", None)
        self.toolhead.move_axis("Y", None)
        self.toolhead.move_axis("Z", None)
        
        self.vial_carousel.add_fluid()
        self.vial_carousel.set_vial(vial_num)
        self.toolhead.move_axis("Y", -10, relative=True)
        self.pippete_handler.dispense_all(2)
        self.toolhead.move_axis("Y", 10, relative=True)
        
        
    def dispense(self, duration_s):
        """ Dispense all fluid in pippete, assuming there is any"""
        # calculate feedrate
        self.pippete_handler.dispense_all(duration_s)
        
    def get_pippete(self, pippete_num: int):
        self.toolhead.set_position(900, 100, 50)

    # -------- SPECTROMETER MOVES --------

    def measure_spectrum(self, measurement_type: str):
        """
        Captures a spectrum using the spectrometer and stores the data.
        
        Args:
            measurement_type (str): Label for the measurement (e.g., 'Background', 'Reference', 'Sample')
        """
        if not self.spectrometer:
            self.logger.error("Spectrometer is not initialized.")
            return

        self.logger.info(f"Starting spectrometer measurement: {measurement_type}")

        # Request wavelengths if not already retrieved
        if not hasattr(self, "wavelengths") or not self.wavelengths:
            self.logger.info("Retrieving wavelength data...")
            self.spectrometer.send_command("<wavs?>")
            self.wavelengths = self.spectrometer.read_wavelengths()

        # Capture intensity data
        self.logger.info("Capturing spectrum intensity data...")
        self.spectrometer.send_command("<read:1>")
        intensities = self.spectrometer.read_spectrum()

        # Store the measurement
        if not hasattr(self, "measurements"):
            self.measurements = {}

        self.measurements[measurement_type] = {
            "wavelengths": self.wavelengths,
            "intensities": intensities
        }

        self.logger.info(f"Measurement '{measurement_type}' captured successfully.")

    def automated_measurement(self):
        """Runs the full spectrometer measurement process."""
        measurement_types = ["Background", "Reference", "Sample"]
        
        for measurement in measurement_types:
            self.measure_spectrum(measurement)

        self.logger.info("All spectrometer measurements completed successfully.")
    
    # -------- VIAL CAROUSEL MOVES --------
    def set_vial(self, vial_num):
        self.vial_carousel.set_vial(vial_num)
        
    # -------- INFEED MOVES --------
    def open_infeed(self):
        pass
     
    def close_infeed(self):
        pass
    
