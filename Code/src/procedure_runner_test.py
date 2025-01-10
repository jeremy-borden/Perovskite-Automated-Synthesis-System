"""
 load in procedure from file (yaml)
 send procedure to procedure handeler
 begin procedure handeler
 
"""
import logging
from time import sleep
from drivers.procedure_driver import Procedure
from drivers.controlboard_driver import ProcedureHandeler
from drivers.controlboard_driver import ControlBoard

def print_task(message: str):
    print(message)
    
def sleep_task(seconds: int):
    print(f"Sleeping for {seconds} seconds")
    sleep(seconds)

def create_logger() -> logging.Logger:
    _logger = logging.getLogger("Main Logger")
    _logger.setLevel(logging.DEBUG)
    
    _console_handler = logging.StreamHandler()
    _formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    _console_handler.setFormatter(_formatter)
    _logger.addHandler(_console_handler)
    
    return _logger

if __name__ == "__main__":
    #init logger
    logger = create_logger()
    
    #initializing connection to control board
    
    control_board = ControlBoard(logger_instance=logger)
    
    #first load in the procedure
    procedure_config = Procedure().Open("src/default_procedure.yml")
    
    move_list = procedure_config["Procedure"]
    
    dispatcher = {
        "print": print_task,
        "wait": sleep_task,
        "goto": control_board.goto,
        "echo": control_board.echo,
        "gcode": control_board.send_message
    }
    
    procedure_handeler = ProcedureHandeler(dispatcher)
    procedure_handeler.run(move_list)
    
    