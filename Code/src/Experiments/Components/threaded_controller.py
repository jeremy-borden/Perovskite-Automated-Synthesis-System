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
        self.logger = logger_instance

        self._connect("COM3")
        
        self.reader_thread = serial.threaded.ReaderThread(self.serial, lambda: ControlBoardLineReader(self.logger))
        self.reader_thread.daemon = True
        self.reader_thread.start()

    def _connect(self, port: str):
        """Connect to the control board."""
        if(self.serial is not None):
            self.logger.error("Serial is already connected")
            return
        
        try:
            self.serial = serial.Serial(port, 250000, timeout=3)
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to control board: {e}")
        
    def _send_message(self, message: str):
        """Send a message to the control board.

        Args:
            message (str): The message to send.
        """
        if self.reader_thread and self.reader_thread.is_alive():
            with self.reader_thread as rt:
                rt.write_line(message)
            
    def stop_thread(self):
        """Stop the reader thread."""
        
        if self.reader_thread and self.reader_thread.is_alive():
            self.reader_thread.join()  # Wait for thread to finish
        
        return
    
    def _wait_to_finish(self):
        
    

class ControlBoardLineReader(serial.threaded.LineReader):
    """Class to read lines from the control board.
    """
    def __init__(self, line_instance: logging.Logger):
        """Initialize with optional logger."""
        super().__init__()
        self.logger = line_instance
        

    def handle_line(self, line):
        """Process each received line."""
        print(line)
        self.logger.info(f"Received: {line}")

