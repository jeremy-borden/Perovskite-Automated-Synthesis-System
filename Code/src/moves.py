from time import sleep
from inspect import signature
import logging
import numpy as np

from drivers.procedure_file_driver import ProcedureFile
from objects.toolhead import Toolhead
from objects.hotplate import Hotplate
from objects.gripper import Gripper
from objects.infeed import Infeed
from objects.pippete import PipetteHandler
from objects.vial_carousel import VialCarousel
from objects.tip_matrix import TipMatrix
from objects.tip_matrix import SlideMatrix

from drivers.camera_driver import Camera
from drivers.spincoater_driver import SpinCoater
from drivers.spectrometer_driver import Spectrometer
from drivers.procedure_file_driver import ProcedureFile
from image_processing import ImageProcessor

class Dispatcher():
    

    def __init__(self, spin_coater: SpinCoater, hotplate: Hotplate, 
                 camera: Camera, gripper: Gripper, infeed: Infeed, pippete_handler: PipetteHandler,
                 toolhead: Toolhead, vial_carousel: VialCarousel, spectrometer: Spectrometer, tip_matrix: TipMatrix, spectrometer_frame=None):
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
        self.spectrometer_frame = spectrometer_frame
        self.tip_matrix = tip_matrix
        self.slide_matrix = SlideMatrix()
        
        ImageProcessor.set_detector()

        self.move_dict = {
            "example_move": self.example_move,
            
            "log": self.log,
            "wait": self.wait,
            "home": self.home,
            
            "move_toolhead": self.move_toolhead,
            "move_to_location": self.move_to_location,
            
            "set_temperature": self.set_temperature,
            "wait_for_temperature": self.wait_for_temperature,
            
            "align_gripper": self.align_gripper,
            "set_finger_angle": self.set_finger_angle,
            "set_gripper_angle": self.set_gripper_angle,
            "open_gripper": self.open_gripper,
            "close_gripper": self.close_gripper,
            
            
            "add_spin_coater_step": self.add_spin_coater_step,
            "run_spin_coater": self.run_spin_coater,
            
            "set_infeed_angle": self.set_infeed_angle,
            "open_infeed": self.open_infeed,
            "close_infeed": self.close_infeed,

            "set_actuator": self.set_actuator,
            "set_pipette": self.set_pipette,
            "put_away_pipette": self.put_away_pipette,
            "set_eject_angle": self.set_eject_angle,
            "set_vial": self.set_vial,
            "extract_from_vial": self.extract_from_vial,
            "dispense": self.dispense,
            #"replace_tip": self.replace_tip,
            "mix_fluid": self.mix_fluid,
            "eject_tip": self.eject_tip,
            "set_grab_angle": self.set_grab_angle,
            
            "measure_spectrum": self.measure_spectrum,
            "automated_measurement": self.automated_measurement,
            
            "put_0": self.put_0,
            "put_1": self.put_1,
            "set_0": self.set_0,
            "set_1": self.set_1,
        }
        
        
        # procedure coordination info
        self.locations = []
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

    
    def validate_location(self, location: str):
        self.locations = ProcedureFile().Open("persistant/locations.yml")
        location_names = []
        for loc in self.locations:
            location_names.append(loc[0])
            self.logger.debug(loc[0])
            
        if location not in location_names:
            raise ValueError(f"Location name {location} not found")
        
# --------- GENERAL MOVES --------

    def home(self):
        """ Reset the machine"""
        self.toolhead.home()
        self.pippete_handler.home()
        self.vial_carousel.home()
        
        self.tip_matrix.refill_tips()
        self.slide_matrix.refill_slides()
        self.open_gripper()

        
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
        
    def super_move(self, file_name: str):
        """ Runs a file as a single move"""
        try:
            super_move = ProcedureFile().Open(f"persistant/{file_name}.yml")
            moves = super_move["Procedure"]
        except Exception as e:
            self.logger.error(f"Error while running supermove {file_name}: {e}")
        try:
            for i, move in enumerate(moves):
                self.logger.debug(f"Executing sub-move {i}")
                func_name = move[0]
                func_args = move[1:]
                
                self.move_dict[func_name](*func_args)
        except Exception as e:
            self.logger.error(f"Error while running sub-move: {e}")
            
    def example_move(self, value_1: int, value_2: float, value_3: str):
        return
    #  --------- HOTPLATE MOVES --------
    def set_temperature(self, temperature_c: int):
        self.hotplate.set_temperature(temperature_c)
    
    def wait_for_temperature(self, target_temperature: int, threshold: int):
        timeout_s = 600
        while abs(self.hotplate.current_temperature_c - target_temperature) > threshold:
            sleep(1)
            timeout_s -= 1
            if timeout_s == 0:
                raise Exception("Hotplate failed to reach temperature in under 600 seconds. Try a larger threshold?")

    # --------- TOOLHEAD MOVES --------
    def move_toolhead(self, x: float, y: float, z: float, relaitve: int):
        """Move the toolhead to the specified coordiantes """
        rrelaitve = False
        if relaitve >= 1:
            rrelaitve = True
        
        self.toolhead.move_axis("X", x, relative=rrelaitve)
        self.toolhead.move_axis("Y", y, relative=rrelaitve)
        self.toolhead.move_axis("Z", z, relative=rrelaitve)
        
    def move_to_location(self, destination: str):
        self.validate_location(destination)

        self.toolhead.move_axis("Z", 200)
        for location in self.locations:
            if destination == location[0]:
                
                x = location[1]
                y = location[2]
                z = location[3]
                
                self.toolhead.move_axis("X", x)
                sleep(1)
                self.toolhead.move_axis("Y", y)
                sleep(1)
                
                self.toolhead.move_axis("Z", z)
                sleep(1)
                
                break
         
    # --------- SPIN COATER MOVES --------
    def add_spin_coater_step(self, rpm: int, spin_time_seconds: int):
        """ Command the spincoater to spin at a specified speed for a specified time"""
        
        self.spin_coater.add_step(rpm, spin_time_seconds)
        
    def run_spin_coater(self):
        self.spin_coater.run(wait_to_finish=True)
    
    # --------- GRIPPER MOVES --------
    def open_gripper(self):
        self.gripper.set_finger_angle(60)
        
    def close_gripper(self):
        self.gripper.set_finger_angle(28)
    
    def set_gripper_angle(self, angle: int):
        self.gripper.set_arm_angle(angle)
        
    def set_finger_angle(self, angle:int):
        self.gripper.set_finger_angle(angle)
    
    def align_gripper(self):
        frame = self.camera.get_frame()
        
        angle0 = None
        angle1 = None
        try_count = 5
        while(angle0 is None or angle1 is None) or abs(angle1-angle0) > 5:
            self.logger.debug("Getting first angle")
            frame = self.camera.get_frame()
            
            angle0 = ImageProcessor.get_marker_angles(image=frame, marker_id=7)
            if angle0 is not None:
                angle0 = angle0 % 90
            
            self.logger.info(f"Got Angle0: {angle0}")
            sleep(1)
            self.logger.debug("Getting second angle")
            frame = self.camera.get_frame()
            angle1 = ImageProcessor.get_marker_angles(image=frame, marker_id=7)
            if angle1 is not None:
                angle1 = angle1 % 90 
            self.logger.debug(f"Got Angle1: {angle1}")
            sleep(1)
            
            try_count -= 1
            
            if try_count == 0:
                raise ValueError("Angle could not be found")
            
        
            
        self.logger.info(int(angle0))
        
        angle0 = (90-angle0) + 27 # from 25
        self.gripper.set_arm_angle(int(angle0))
        
    def grab_new_slide(self):
        self.open_gripper()
        self.move_to_location("slide matrix")
        x_offset, y_offset = self.slide_matrix.get_slide_offset(slide_num=self.slide_matrix.slides_taken)
        self.toolhead.move_axis("X", -x_offset, relative=True)
        self.toolhead.move_axis("Y", -y_offset, relative=True)
        self.toolhead.move_axis("Z", 13)
        self.close_gripper()
        self.toolhead.move_axis("Z", 200)
        self.slide_matrix.take_slide()
        
    # -------- PIPPETE MOVES --------
    def set_actuator(self, position: float):
        self.pippete_handler.set_actuator_position(position)
    
    def replace_tip(self):
        # raise machine to avoid collisions
        self.toolhead.move_axis("Z", 200)
        
        self.move_to_location("tip dropoff")
        self.eject_tip()
        self.move_to_location("tip matrix") #603.2, 193.5, 105

        next_tip_num = self.tip_matrix.tips_taken
        x_offset, y_offset = self.tip_matrix.get_tip_offset()
        self.toolhead.move_axis("X", -x_offset, relative=True)
        self.toolhead.move_axis("Y", -y_offset, relative=True)
        
        self.toolhead.move_axis("Z", 97.5)
        self.toolhead.move_axis("Z", 200)
            
    def extract_from_vial(self, vial_num: int, volume_ul: int):
        vial_draw_height = 82 #distance required for pipette to dip into vial
    
            
        
        self.toolhead.move_axis("Z", 200)
        self.move_to_location("vial carousel")
        self.vial_carousel.set_vial(vial_num)
        self.toolhead.move_axis("Z", vial_draw_height)
        self.pippete_handler.dispense_all(3)
        self.pippete_handler.draw_ul(volume_ul)
        self.toolhead.move_axis("Z", 200)
                
    def mix_fluid(self, source_vial_1: int, amount_1: int, source_vial_2: int, amount_2: int, destination_vial: int):
        vial_draw_height = 82
        

        # raise machine to avoid collisions
        self.toolhead.move_axis("Z", 200)
        self.toolhead.move_axis("X", 592)
        self.toolhead.move_axis("Y", 88)
        
        # draw from first vial
        self.vial_carousel.set_vial(source_vial_1)
        self.pippete_handler.dispense_all(3) 
        self.toolhead.move_axis("Z", vial_draw_height)
        self.pippete_handler.draw_ul(amount_1)
        self.toolhead.move_axis("Z", 200)
        
        # dispense fluid 1 into destination
        self.vial_carousel.set_vial(destination_vial)
        self.toolhead.move_axis("Z", vial_draw_height)
        self.pippete_handler.dispense_all(1)
        self.toolhead.move_axis("Z", 200)
        
        # draw from first vial
        self.vial_carousel.set_vial(source_vial_2)
        self.pippete_handler.dispense_all(3) 
        self.toolhead.move_axis("Z", vial_draw_height)
        self.pippete_handler.draw_ul(amount_2)
        self.toolhead.move_axis("Z", 200)
        
        # dispense fluid 1 into destination
        self.vial_carousel.set_vial(destination_vial)
        self.toolhead.move_axis("Z", vial_draw_height)
        self.pippete_handler.dispense_all(1)
        
        # mix fluids together
        for i in range(5):
            self.pippete_handler.draw_ul(10)
            self.pippete_handler.dispense_all(1)
        
        self.toolhead.move_axis("Z", 200)
        
    def dispense(self, duration_s: int):
        """ Dispense all fluid in pippete, assuming there is any"""
        # calculate feedrate
        self.pippete_handler.dispense_all(duration_s)
        
    def set_grab_angle(self, angle: int):
        self.pippete_handler.set_grabber_angle(angle)
    
    def put_away_pipette(self):
        current_pipette = self.pippete_handler.get_pippete_index()
        
        if not current_pipette:
            self.logger.debug("No pipette held, returning")
            return
        
        self.move_to_location("pipette stand")
        if current_pipette == 0:
            self.toolhead.move_axis("Y", self.pippete_handler.STAND_0_Y)
        else:
            self.toolhead.move_axis("Y", self.pippete_handler.STAND_1_Y)
            
        self.toolhead.move_axis("Z", 40, relative=True) # raise
        self.toolhead.move_axis("X", 120, relative=True) #move forward
        self.toolhead.move_axis("Z", -40, relative=True) #lower into stand
        self.pippete_handler.open_grabber()
        self.toolhead.move_axis("X", -120, relative=True) #move backwards
        
        self.pippete_handler.set_pipette()
        
    
    
    
    def set_0(self):
        self.pippete_handler.set_actuator_position(97)
        self.pippete_handler.set_pipette(0)
        self.toolhead.move_axis("Z", 200)
        self.move_to_location("pipette stand")
        self.pippete_handler.set_grabber_angle(145)
        self.toolhead.move_axis("X", 120, relative=True) #move forward
        self.pippete_handler.set_grabber_angle(48)
        self.toolhead.move_axis("Z", 40, relative=True) # raise
        self.toolhead.move_axis("X", -120, relative=True) #move backwards
        
    def set_1(self):
        self.pippete_handler.set_actuator_position(97)
        self.pippete_handler.set_pipette(1)
        
        self.move_to_location("pipette stand")
        self.toolhead.move_axis("Z", 200)
        self.toolhead.move_axis("Y", 151)
        self.toolhead.move_axis("Z", 128)
        self.pippete_handler.set_grabber_angle(145)
        self.toolhead.move_axis("X", 120, relative=True) #move forward
        self.pippete_handler.set_grabber_angle(48)
        self.toolhead.move_axis("Z", 40, relative=True) # raise
        self.toolhead.move_axis("X", -120, relative=True) #move backwards
        
    def put_0(self):
        self.pippete_handler.set_actuator_position(97)
        self.toolhead.move_axis("Z", 200)
        self.move_to_location("pipette stand")
        self.toolhead.move_axis("Z", 40, relative=True) # raise
        self.toolhead.move_axis("X", 120, relative=True) #move forward
        self.toolhead.move_axis("Z", -40, relative=True) # raise
        self.pippete_handler.set_grabber_angle(145)
        self.toolhead.move_axis("X", -120, relative=True) #move backwards
    
    def put_1(self):
        self.pippete_handler.set_actuator_position(97)
        self.toolhead.move_axis("Z", 200)
        self.move_to_location("pipette stand")
        self.toolhead.move_axis("Z", 200)
   
        self.toolhead.move_axis("Y", 151)
        self.toolhead.move_axis("Z", 168)
        self.toolhead.move_axis("X", 120, relative=True) #move forward
        self.toolhead.move_axis("Z", -40, relative=True) # raise
        self.pippete_handler.set_grabber_angle(145)
        self.toolhead.move_axis("X", -120, relative=True) #move backwards
    
    def set_pipette(self, target_pipette: int):
        # rasie toolhead to avoid collisions

        current_pipette = self.pippete_handler.get_pippete_index()
        self.toolhead.move_axis("Z", 200)
        
        #self.move_to_location("pipette pickup")
        #move in front of first pipette stand
        self.move_to_location("pipette stand")
        # self.toolhead.move_axis("Y", 85)
        # self.toolhead.move_axis("Z", 148)
        # self.toolhead.move_axis("X", 593)
        
        # if we have a pipette and its not the one we want, put it away
        if current_pipette and current_pipette != target_pipette:
            if current_pipette == 0:
                self.toolhead.move_axis("Y", self.pippete_handler.STAND_0_Y)
            else:
                self.toolhead.move_axis("Y", self.pippete_handler.STAND_1_Y)
            
            self.toolhead.move_axis("Z", 40, relative=True) # raise
            self.toolhead.move_axis("X", 120, relative=True) #move forward
            self.toolhead.move_axis("Z", -40, relative=True) #lower into stand
            self.pippete_handler.open_grabber()
            self.toolhead.move_axis("X", -120, relative=True) #move backwards
        
        if current_pipette == 0:
            self.toolhead.move_axis("Y", self.pippete_handler.STAND_0_Y)
        else:
            self.toolhead.move_axis("Y", self.pippete_handler.STAND_1_Y)
            
        self.pippete_handler.open_grabber()
        self.toolhead.move_axis("X", 120, relative=True) #move forward
        self.pippete_handler.close_grabber()
        self.toolhead.move_axis("Z", 40, relative=True) # raise
        self.toolhead.move_axis("X", -120, relative=True) #move backwards
        
        self.pippete_handler.set_pipette(target_pipette)
        
    def eject_tip(self):
        self.pippete_handler.eject_tip()
        
    def set_eject_angle(self, angle: int):
        self.pippete_handler.set_eject_angle(angle)

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
        if not hasattr(self, "wavelengths") or not isinstance(self.wavelengths, np.ndarray) or self.wavelengths.size == 0:
            self.logger.info("Retrieving wavelength data...")
            self.wavelengths = self.spectrometer.read_wavelengths()

        # Capture intensity data
        self.logger.info("Capturing spectrum intensity data...")
        intensities = self.spectrometer.read_spectrum(measurement_type)
        if self.spectrometer_frame:
            self.spectrometer_frame.update_plot()
        # Store the measurement
        if isinstance(intensities, np.ndarray) and intensities.size > 0 and \
           isinstance(self.wavelengths, np.ndarray) and self.wavelengths.size > 0 and \
           intensities.shape == self.wavelengths.shape:

                
            if not hasattr(self, "measurements"):
                self.measurements = {}

            self.measurements[measurement_type] = {
                "wavelengths": self.wavelengths,
                "intensities": intensities
            }

            self.logger.info(f"Measurement '{measurement_type}' captured successfully.")
        else:
            self.logger.warning(f"Incomplete data for measurement '{measurement_type}'. Skipping.")
        
    def automated_measurement(self):
        """Runs the full spectrometer measurement process."""
        measurement_types = ["Background", "Reference", "Sample"]
        
        for measurement in measurement_types:
            self.measure_spectrum(measurement)
            sleep(1.0) 
            
        save_all_to_csv(self.measurements, self.wavelengths)
        plot_spectra(self.measurements, self.wavelengths)
        
        self.logger.info("All spectrometer measurements completed successfully.")
    
    # -------- VIAL CAROUSEL MOVES --------
    def set_vial(self, vial_num: int):
        self.vial_carousel.set_vial(vial_num)
        
    # -------- INFEED MOVES --------
    def set_infeed_angle(self, angle: int):
        
        current_angle = int(self.infeed.servo.angle)
        step = 1 if angle > current_angle else -1

        for subangle in range(current_angle, angle, step):
            self.infeed.servo.angle = subangle
            sleep(0.1)
        self.infeed.servo.angle = angle
        
    def open_infeed(self):
        self.set_infeed_angle(90)
        
    def close_infeed(self):
        self.set_infeed_angle(0)
    
