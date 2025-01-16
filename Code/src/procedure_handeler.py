import threading
from inspect import signature
import queue
import logging



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

        self.procedure = None
        self.move_queue = queue.Queue()
        self.running = threading.Event()
        self.started = threading.Event()
        self.running.clear()
        self.started.clear()
        
    def set_procedure(self, procedure: list):
        """Set the procedure to be run.

        Args:
            procedure (list): list of moves to run.
        """
        if not self.validate_moves(procedure):
            self.logger.error("Invalid moves in procedure")
            return
        
        self.procedure = procedure
        
    def validate_moves(self, moves: list) -> bool:
        """Validates a list of moves

        ### Args:
            moves (list): _description_

        ### Returns:
            bool: returns True if all moves are valid, False otherwise
        """
        valid = True
        
        if not moves:
            self.logger.error("No moves found")
            return False
        
        for index, move in enumerate(moves):
            func_name = move["function"]
            func_args = move["args"]
            
            if func_name not in self.dispatcher:
                self.logger.error(f"Function #{index},{func_name} not found in dispatcher")
                valid = False
            
            func = self.dispatcher[func_name]
            try:
                sig = signature(func)
                sig.bind(*func_args)
            except TypeError as e:
                self.logger.error(f"Function #{index}, \"{func_name}\" has incorrect arguments: {e}")
                valid = False
                
        return valid
        
    def _add_moves(self):
        """Add moves to the procedure queue."""
        for move in self.procedure:
            self.move_queue.put(move)
        
    def clear_moves(self):
        """Clear the procedure queue."""
        self.move_queue.queue.clear()

    def run(self):
        """Run the procedure."""
        while True:
            self.started.wait()
            
            if self.move_queue.empty():
                self.logger.error("No moves in queue")
                self.stop()
                continue
            
            while not self.move_queue.empty() and self.started.is_set():
                self.running.wait()
                
                self.logger.debug("Getting next move")
                move = self.move_queue.get()
                func_name = move["function"]
                func_args = move["args"]
                
                self.dispatcher[func_name](*func_args)
            
            self.started.clear()
            self.running.clear()
            self.logger.info("Procedure ended")
        
    def begin(self):
        """Begin the procedure."""
        if not self.procedure:
            self.logger.error("No procedure set")
            return
        self._add_moves()
        self.started.set()
        self.running.set()
        self.logger.info("Procedure started")
        
    def stop(self):
        """Stop the procedure."""
        
        self.started.clear()
        self.running.clear()
        self.clear_moves()
        self.logger.info("Procedure stopped")
        
    def pause(self):
        """Pause the procedure."""
        self.running.clear()
        self.logger.info("Procedure paused")
    
    def resume(self):
        """Resume the procedure."""
        self.running.set()
        self.logger.info("Procedure resumed")
        
        