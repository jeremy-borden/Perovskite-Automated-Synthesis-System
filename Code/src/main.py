import logging
from queue import Queue
import customtkinter as ctk


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

from procedure_handler import ProcedureHandler
from moves import Dispatcher


def create_logger() -> logging.Logger:
    _logger = logging.getLogger("Main Logger")
    _logger.setLevel(logging.DEBUG)
    _console_handler = logging.StreamHandler()
    _formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    _console_handler.setFormatter(_formatter)
    _logger.addHandler(_console_handler)

    return _logger

if __name__ == "__main__":
    # initialize logger
    logger = create_logger()

    # initialize peripherals
    control_board = ControlBoard(com_port="COM7",logger=logger)
    spincoater= SpinCoater(com_port="COM4",logger=logger)
    camera = Camera(logger=logger)
    camera.start()
    dac = DAC(0x00)
    
    

    

    
    # create dispatcher, might switch to just dict in the future
    dispatcher = Dispatcher(logger=logger,control_board=control_board,spincoater=spincoater,dac=dac)
    procedure_handler = ProcedureHandler(logger=logger,dispatcher=dispatcher)
    
    procedure_handler.start()
    # load in the procedure
    procedure_config = ProcedureFile().Open("Code/src/printandwait.yml")
    if procedure_config is not None:
        move_list = procedure_config["Procedure"]
        procedure_handler.set_procedure(move_list)
    else:
        logger.warning("Default procedure not found")

    app = ctk.CTk()
    app.geometry("1000x1000")

    procedure_frame = ProcedureFrame(app, procedure_handler)
    procedure_frame.grid(
        row=0, column=0,
        padx=5, pady=5,sticky="nsew")

    console_frame = ConsoleFrame(app, logger)
    console_frame.grid(
        row=1, column=0,
        padx=5, pady=5,sticky="nsew")

    connection_frame = ConnectionFrame(master=app, control_board=control_board, spin_coater=spincoater, camera=camera)
    connection_frame.grid(
        row=0, column=1,
        padx=5, pady=5, sticky="nsew")
 ## TODO add a yaml callable function that is called aruco align servo that aligns the servo with the aruco marker
 # also TODO actually put the aruco marker stuff in here, camera output should draw boxes. option to turn it on or off
 # TODO put gui in its own file and make a custom root thing
    camera_frame = CameraFrame(master=app, camera=camera)
    camera_frame.grid(
        row=1, column=1,rowspan=2,
        padx=5, pady=5,sticky="nsew")

    info_frame = InfoFrame(app, control_board)
    info_frame.grid(
        row=2, column=0,
        padx=5, pady=5, sticky="nsew")

    app.mainloop()
    
    # cleanup
    logger.removeHandler(console_frame.console_handler)
    
    control_board.disconnect()
    spincoater.disconnect()
    camera.disconnect()
    
    
    
