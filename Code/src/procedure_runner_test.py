"""
 load in procedure from file (yaml)
 send procedure to procedure handeler
 begin procedure handeler
 
"""
import logging
from drivers.procedure_driver import Procedure
from procedure_handeler import ProcedureHandeler
from dispatcher import Dispatcher
from drivers.controlboard_driver import ControlBoard


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

    # initialize connection to control board
    control_board = ControlBoard(logger=logger)

    # load in the procedure
    procedure_config = Procedure().Open("src/default_procedure.yml")
    move_list = procedure_config["Procedure"]

    # create dispatcher
    dispatcher = Dispatcher(control_board)

    procedure_handeler = ProcedureHandeler(
        logger=logger,
        dispatcher=dispatcher.dispatcher
        )
    procedure_handeler.add_moves(move_list)
    procedure_handeler.run()
