import logging
from tkinter import PhotoImage
import customtkinter as ctk
from PIL import Image
from gpiozero import AngularServo, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from objects.hotplate import Hotplate
from objects.gripper import Gripper

from guiFrames.console_frame import ConsoleFrame
from guiFrames.procedure_frame import ProcedureFrame
from guiFrames.info_frame import InfoFrame
from guiFrames.camera_frame import CameraFrame
from guiFrames.conection_frame import ConnectionFrame

from drivers.controlboard_driver import ControlBoard
from drivers.spincoater_driver import SpinCoater
from drivers.dac_driver import DAC
from drivers.camera_driver import Camera
from drivers.procedure_file_driver import ProcedureFile
from drivers.spectrometer_driver import Spectrometer

from procedure_handler import ProcedureHandler
from moves import Dispatcher

if __name__ == "__main__":
    # --------INITIALIZATION--------
    logger = logging.getLogger("Main Logger")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    
    #enable software pwm
    Device.pin_factory = PiGPIOFactory()
    
    # initialize peripherals
    control_board = ControlBoard(com_port="/dev/ttyACM0",logger=logger)
    spincoater= SpinCoater(com_port="/dev/ttyACM1",logger=logger)
    spectrometer = Spectrometer(com_port="/dev/ttyACM2", logger=logger)
    camera = Camera(logger=logger)

    # initialize objects
    
    gripper = Gripper(arm_servo=AngularServo(pin=17, min_angle=0, max_angle=270, ),
                      finger_servo=AngularServo(pin=18, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000))
    
    dac = DAC(0x60)
    hotplate = Hotplate(max_temperature=540, dac=dac)
    
    
    dispatcher = Dispatcher(logger=logger,
                            control_board=control_board,
                            spincoater=spincoater,
                            hotplate=hotplate,
                            camera=camera,
                            gripper=gripper)
    
    
    procedure_handler = ProcedureHandler(logger=logger,dispatcher=dispatcher)
    
    # --------LOAD DEFAULT PROCEDURE--------
    procedure_config = ProcedureFile().Open("procedures/default_procedure.yml")
    if procedure_config is not None:
        move_list = procedure_config["Procedure"]
        procedure_handler.set_procedure(move_list)
    else:
        logger.warning("Default procedure not found")



    # --------GUI--------
    app = ctk.CTk()
    ctk.set_appearance_mode("dark")
    app.geometry("1000x1000")
    app.title("ECD 515 - Perovskite Automated Synthesis System")
    icon = PhotoImage(file="guiImages/logo.png")
    app.wm_iconphoto(False, icon)

    procedure_frame = ProcedureFrame(app, procedure_handler)
    procedure_frame.grid(
        row=0, column=0,
        padx=5, pady=5,sticky="nsew")

    console_frame = ConsoleFrame(app, logger)
    console_frame.grid(
        row=1, column=0,
        padx=5, pady=5,sticky="nsew")

    connection_frame = ConnectionFrame(master=app,
                                       control_board=control_board,
                                       spin_coater=spincoater,
                                       camera=camera,
                                       spectrometer=spectrometer)
    connection_frame.grid(
        row=0, column=1,
        padx=5, pady=5, sticky="nsew")

    camera_frame = CameraFrame(master=app, camera=camera)
    camera_frame.grid(
        row=1, column=1,rowspan=2,
        padx=5, pady=5,sticky="nsew")

    info_frame = InfoFrame(app, control_board)
    info_frame.grid(
        row=2, column=0,
        padx=5, pady=5, sticky="nsew")

    # run the gui
    app.mainloop()
    
    # --------CLEANUP--------
    logger.removeHandler(console_frame.console_handler)
    
    control_board.disconnect()
    spincoater.disconnect()
    camera.disconnect()
    
    
    
