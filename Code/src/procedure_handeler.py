import threading
import time
import queue
import logging
from venv import logger


class ProcedureHandeler(threading.Thread):
    """Class to handle procedures for the control board.
    """

    def __init__(self, logger: logging.Logger, dispatcher):
        super().__init__(
            name="ProcedureHandeler",
            daemon=True
        )
        self.logger = logger
        self.dispatcher = dispatcher
        self.move_in_progress = False

        self.procedure_queue = queue.Queue()
        self.is_paused = False

    def add_moves(self, moves: list):
        """Add moves to the procedure queue.

        Args:
            moves (list): list of moves to add to the queue.
        """
        for move in moves:
            self.procedure_queue.put(move)

    def run(self):
        """Run the procedure."""
        while not self.procedure_queue.empty():
            while self.is_paused:
                time.sleep(0.1)

            move = self.procedure_queue.get()
            func_name = move["function"]
            func_args = move["args"]
            self.dispatcher[func_name](*func_args)
        logger.info("Procedure complete")