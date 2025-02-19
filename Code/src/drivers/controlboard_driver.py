import logging
import serial.threaded
import time
import serial
import threading
import queue

# DEFAULT_SPEED = 1000


class ControlBoard():
    """Class to control the octopus v1.1 control board.
    """
    def __init__(self, logger_instance: logging.Logger):
        
        self.serial = None
        self._connect("COM3")
        self.logger = logger_instance
        self.received_ok = threading.Event() 

        
        self.reader_thread = serial.threaded.ReaderThread(self.serial, lambda: ControlBoardLineReader(self.logger, self))
        self.reader_thread.daemon = True
        self.reader_thread.start()

    def _connect(self, port: str):
        """Connect to the control board."""
        if(self.serial is not None):
            self.logger.error("Serial is already connected")
            return
        
        try:
            self.serial = serial.Serial(port, 250000, timeout=0.5)
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to control board: {e}")
        
    def _send_message(self, message: str):
        """Send a message to the control board.

        Args:
            message (str): The message to send.
        """
        if self.reader_thread and self.reader_thread.is_alive():
            if '\r\n' not in message:
                message += "\r\n"
            self.reader_thread.write(message.encode("utf-8"))
            self.logger.debug(f"Sending message: {message}")
            
    def send_message(self, message: str):
        self._send_message(message)
        
            
    def stop_thread(self):
        """Stop the reader thread."""
        
        if self.reader_thread and self.reader_thread.is_alive():
            self.reader_thread.join()  # Wait for thread to finish
        
        return
    
    def _finish_move(self):
        """Wait for the move to finish."""
        self._send_message("M400")
        self.received_ok.clear()
        self.received_ok.wait()  # Wait until the move_finished event is set
        
    def goto(self, x:float = None, y:float = None, z:float = None, speed:int = 1000):
        self._send_message(f"G0 X{x} Y{y} Z{z} F{speed}")
        self._finish_move()
    def echo(self, message: str):
        self._send_message(f"M118 {message}")
        
        
    
    


class ControlBoardLineReader(serial.threaded.LineReader):
    """Class to read lines from the control board.
    """
    TERMINATOR = b"\n"
    def __init__(self, line_instance: logging.Logger, control_board: ControlBoard):
        """Initialize with optional logger."""
        super().__init__()
        self.logger = line_instance
        self.control_board = control_board 
       

    def handle_line(self, line):
        """Process each received line."""
        line = line.strip()
        self.logger.debug(f"Received: {line}")
        if "ok" in line:
            self.control_board.received_ok.set()  # Set the event when "DONE" is received
            


# Main program
class ProcedureHandeler(threading.Thread):
    """Class to handle procedures for the control board.
    """
    def __init__(self, dispatcher):
        super().__init__(
            name="ProcedureHandeler",
            daemon=True
        )
        
        self.dispatcher = dispatcher
        self.move_in_progress = False
        
        self.procedure_queue = queue.Queue()
        self.is_paused = False
        
    def run(self, moves: list):
        if moves:
            for move in moves:
                self.procedure_queue.put(move)
        
        while not self.procedure_queue.empty():
            while self.is_paused:
                time.sleep(0.1)
                
            move = self.procedure_queue.get() 
            func_name = move["function"]
            func_args = move["args"]
            self.dispatcher[func_name](*func_args)
            
                


# if __name__ == "__main__":

#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)
#     console_handler = logging.StreamHandler()
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     console_handler.setFormatter(formatter)
#     logger.addHandler(console_handler)

#     queue = queue.Queue()
    
#     with serial.Serial("COM3", 250000, timeout=3) as ser:

#         with serial.threaded.ReaderThread(ser, lambda: ControlBoardLineReader(logger)) as protocol:
#             protocol.write_line("G4 S1")
#             protocol.write_line("M118 HIIII") 
#             while True:
#                 print("horse")
#                 time.sleep(0.1)  # Let it run for 10 seconds
