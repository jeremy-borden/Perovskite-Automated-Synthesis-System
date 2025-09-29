import logging
from tkinter import PhotoImage
import customtkinter as ctk
from gpiozero import AngularServo, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# -- DRIVER IMPORT --
from drivers.controlboard_driver import ControlBoard
from drivers.spincoater_driver import SpinCoater
from drivers.camera_driver import Camera
from drivers.procedure_file_driver import ProcedureFile
from drivers.spectrometer_driver import Spectrometer
# from drivers import ml_driver

# -- OBJECT IMPORT --
from objects.tip_matrix import TipMatrix
from objects.vial_carousel import VialCarousel
from objects.infeed import Infeed
from objects.hotplate import Hotplate
from objects.gripper import Gripper
from objects.pippete import Pipette, PipetteHandler
from objects.toolhead import Toolhead

# -- GUI IMPORT --
from guiFrames.console_frame import ConsoleFrame
from guiFrames.procedure_frame import ProcedureFrame
from guiFrames.info_frame import InfoFrame
from guiFrames.camera_frame import CameraFrame
from guiFrames.conection_frame import ConnectionFrame
from guiFrames.procedure_builder_frame import ProcedureBuilderFrame
from guiFrames.spectrometer_frame import SpectrometerFrame
from guiFrames.locations_frame import LocationFrame
# from guiFrames.ml_model_frame import MLModelFrame

from procedure_handler import ProcedureHandler
from moves import Dispatcher

if __name__ == "__main__":
    #enable software pwm
    Device.pin_factory = PiGPIOFactory()
    
    # -- LOGGING --
    logger = logging.getLogger("Main Logger")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    
    # -- CONTROL BOARD --
    control_board = ControlBoard()
    
    # -- TOOLHEAD --
    toolhead = Toolhead(control_board=control_board)
    
    # -- SPIN COATER --
    spin_coater= SpinCoater()

    # -- CAMERA --
    camera = Camera()

    # -- GRIPPER --
    arm_servo = AngularServo(pin=17, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    arm_servo.angle = 20
    finger_servo = AngularServo(pin=18, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    finger_servo.angle=40
    gripper = Gripper(arm_servo=arm_servo, finger_servo=finger_servo)
    
    # -- PIPETTE HANDLER --
    tip_eject_servo = AngularServo(pin=27, min_angle=0, max_angle=270, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    grabber_servo = AngularServo(pin=22, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    grabber_servo.angle = 180
    pipettes = [Pipette(200, 97, 17, 3, False),
                Pipette(1000, 97, 17, 3, True)]
    pipette_handler = PipetteHandler(control_board=control_board,
                                     tip_eject_servo=tip_eject_servo, grabber_servo=grabber_servo,
                                     pipettes=pipettes)
    
    # -- HOTPLATE --
    hotplate = Hotplate()
    # -- SPECTROMETER + INFEED --
    spectrometer = Spectrometer()
    
    
    # -- TIP MATRIX --
    tip_matrix = TipMatrix()
  
    infeed_servo = AngularServo(pin=24, min_angle=0, max_angle=180,min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
    infeed = Infeed(infeed_servo)
    
    # -- VIAL CAROUSEL --
    vial_carousel = VialCarousel(control_board)

    # -- GUI --
    app = ctk.CTk()
    ctk.set_appearance_mode("dark")
    app.geometry("1200x1000")
    app.title("ECD 515 - Perovskite Automated Synthesis System")
    
    spectrometer_frame = SpectrometerFrame(master=app, spectrometer=spectrometer)
    
    dispatcher = Dispatcher(toolhead=toolhead,
                            spin_coater=spin_coater,
                            hotplate=hotplate,
                            camera=camera,
                            gripper=gripper,
                            infeed=infeed,
                            spectrometer=spectrometer,
                            vial_carousel=vial_carousel,
                            pippete_handler=pipette_handler,
                            spectrometer_frame=spectrometer_frame, 
                            tip_matrix=tip_matrix)
    
    procedure_handler = ProcedureHandler(dispatcher=dispatcher)
    
    # program stalls when not everything is connected and this is called
    # # connect to devices
    # spectrometer.connect()
    # control_board.connect()
    # camera.connect()
    # spin_coater.connect()
    # hotplate.connect()
    
    
    # --------LOAD DEFAULT PROCEDURE--------
    procedure_config = ProcedureFile().Open("procedures/default_procedure.yml")
    if procedure_config is not None:
        move_list = procedure_config["Procedure"]
        procedure_handler.set_procedure(move_list)
    else:
        logger.warning("Default procedure not found")


    # trying to make an icon 
    icon = PhotoImage(file="guiImages/logo.png")
    app.wm_iconphoto(True, icon)

    # creating frames
    procedure_frame = ProcedureFrame(app, procedure_handler)
    console_frame = ConsoleFrame(app)
    connection_frame = ConnectionFrame(app, control_board,spin_coater,hotplate,camera,spectrometer)
    camera_frame = CameraFrame(app, camera)
    info_frame = InfoFrame(app, control_board, hotplate, pipette_handler, vial_carousel)
    procedure_builder_frame = ProcedureBuilderFrame(app, dispatcher.move_dict, procedure_handler)
    location_frame = LocationFrame(master=app)
    # ml_model_frame = MLModelFrame(app, width=370)
    
    # putting the frames on the gui
    procedure_frame.grid(row=0, column=0, padx=5, pady=5,sticky="nsew")
    connection_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    spectrometer_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    console_frame.grid(row=1, column=0, padx=5, pady=5,sticky="nsew")
    procedure_builder_frame.grid(row=1, column=1, rowspan=2, sticky="nsew")
    camera_frame.grid(row=1, column=2, padx=5, pady=5,sticky="new")
    info_frame.grid(row=2, column=0, padx=5, pady=5, sticky="new")
    location_frame.grid(row=2, column=2,padx=5, pady=5, sticky="new")
    # ml_model_frame.grid(row=1, column=2, padx=5, pady=5,sticky="new")

    # run the gui
    hotplate.set_temperature(0)
    app.mainloop()
    
    # -- CLEANUP --
    hotplate.set_temperature(0)
    sleep(1)
    
    control_board.disconnect()
    spectrometer.disconnect()
    spin_coater.disconnect()
    camera.disconnect()
    hotplate.disconnect()
