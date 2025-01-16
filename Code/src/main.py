import logging
from queue import Queue
import customtkinter as ctk

from guiFrames.console_frame import ConsoleFrame
from guiFrames.procedure_frame import ProcedureFrame
from guiFrames.info_frame import InfoFrame
from guiFrames.camera_frame import CameraFrame
from guiFrames.conection_frame import ConnectionFrame

from drivers.controlboard_driver import ControlBoard
from drivers.camera_driver import Camera
from drivers.procedure_driver import Procedure

from procedure_handeler import ProcedureHandeler
from dispatcher import Dispatcher


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
    current_temp_queue = Queue(maxsize=1)
    # initialize connection to control board
    control_board = ControlBoard(
        com_port="COM7",
        logger=logger)

    # load in the procedure
    procedure_config = Procedure().Open("Code/src/printandwait.yml")
    move_list = procedure_config["Procedure"]

    # create dispatcher
    dispatcher = Dispatcher(
        logger=logger,
        control_board=control_board)

    procedure_handeler = ProcedureHandeler(
        logger=logger,
        dispatcher=dispatcher.dispatcher
    )
    procedure_handeler.set_procedure(move_list)
    procedure_handeler.start()

    camera = Camera(logger=logger)
    # camera.connect()
    # camera.start()

    app = ctk.CTk()
    app.geometry("1000x1000")

    procedure_frame = ProcedureFrame(app, procedure_handeler)
    procedure_frame.grid(
        row=0, column=0,
        padx=5, pady=5,
        sticky="nsew")

    console_frame = ConsoleFrame(app, logger)
    console_frame.grid(
        row=1, column=0,
        padx=5, pady=5,
        sticky="nsew")

    connection_frame = ConnectionFrame(master=app, control_board=control_board)
    connection_frame.grid(
        row=0, column=1,
        padx=5, pady=5,
        sticky="nsew")

    camera_frame = CameraFrame(master=app, camera=camera)
    camera_frame.grid(
        row=1, column=1,
        padx=5, pady=5,
        sticky="nsew",
        rowspan=2)

    info_frame = InfoFrame(app, control_board)
    info_frame.grid(
        row=2, column=0,
        padx=5, pady=5,
        sticky="nsew")

    app.mainloop()
    procedure_handeler.join(timeout=1)
