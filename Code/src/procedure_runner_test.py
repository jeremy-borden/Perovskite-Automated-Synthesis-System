"""
 load in procedure from file (yaml)
 send procedure to procedure handeler
 begin procedure handeler
 
"""
import logging
from queue import Queue
from guiFrames.console_frame import ConsoleFrame
from drivers.procedure_driver import Procedure
from procedure_handeler import ProcedureHandeler
from dispatcher import Dispatcher
from drivers.controlboard_driver import ControlBoard
from guiFrames.info_frame import InfoFrame
import customtkinter as ctk

from guiFrames.procedure_frame import ProcedureFrame



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
        logger=logger,
        data_queue=current_temp_queue)

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
    data_dict = {
        "current_temp": current_temp_queue
    }
    
    app = ctk.CTk()
    app.geometry("800x600")
    #info_frame = InfoFrame(app, data_dict)
    #info_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    
    procedure_frame = ProcedureFrame(app, procedure_handeler)
    procedure_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    
    console_frame = ConsoleFrame(app, logger)
    console_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    
    app.mainloop()
    procedure_handeler.join(timeout=1)
