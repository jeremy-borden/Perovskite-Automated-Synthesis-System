from queue import Queue
import logging
import threading
import serial
import serial.threaded


# DEFAULT_SPEED = 1000


class ControlBoard():
    """Class to control the Octopus v1.1 control board"""

    def __init__(self, com_port: str, logger: logging.Logger):

        self.logger = logger
        self.com_port = com_port
        
        self.hotplate_temperature = 0
        self.positions = {"X": 0,
                          "Y": 0,
                          "Z": 0,
                          "A": 0,
                          "B": 0}
        self.serial = None
        self.reader_thread = None

        self.received_ok = threading.Event()

    def connect(self):
        """Connect to the control board and start the reader thread."""
        if self.is_connected():
            self.logger.error("Control board is already connected")
        
        
        try:
            self.serial = serial.Serial(self.com_port, 250000, timeout=0.5)
            self._begin_reader_thread()
            self.logger.info(f"Connected to control board on port {self.com_port}")
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to control board: {e}")
    
    def disconnect(self):
        if not self.is_connected():
            return
        
        self.serial.close()
        self.logger.debug("Control Board Disconnected")
            
    def is_connected(self) -> bool:
        return self.serial is not None and self.serial.is_open
    
    def kill(self):
        """ Sends M112 to immediately stop steppers and heaters"""
        self.send_message("M112")
        
        
            
    def _begin_reader_thread(self):
        self.reader_thread = serial.threaded.ReaderThread(
            serial_instance=self.serial,
            protocol_factory=lambda: ControlBoardLineReader(
                self.logger, self)
        )
        self.reader_thread.daemon = True
        self.reader_thread.start()

    def send_message(self, message: str):
        """Send a message to the control board.

        ### Args:
            message (str): The message to send.
        """
        if not self.is_connected():
            self.logger.error("Serial is not connected")
            return
  
        
        if self.reader_thread is None:
            self.logger.error("Reader thread is not running")
            return

        # if '\r\n' not in message:
        #     message += "\r\n"
        self.reader_thread.write(message.encode("utf-8"))
        self.logger.debug(f"Sending message: {message}")


    def finish_move(self):
        """Wait for the move to finish"""
        self.send_message("M400")
        self.received_ok.clear()
        self.logger.debug("Waiting for move to finish")
        self.received_ok.wait()  # Wait until the move_finished event is set

    def get_temperature(self):
        return self.hotplate_temperature


class ControlBoardLineReader(serial.threaded.LineReader):
    """Class to read lines from the control board on a separate thread."""
    TERMINATOR = b"\n"
    POSITION_PREFIXS = ["X:", "Y:", "Z:", "A:", "B:"]
    
    def __init__(self, logger: logging.Logger, control_board: ControlBoard):
        """Initialize with optional logger."""
        super().__init__()
        self.logger = logger
        self.control_board = control_board

    def handle_line(self, line):
        """Process each received line."""
        line = line.strip()
        self.logger.debug(f"Received: {line}")
        if line == "ok":
            self.control_board.received_ok.set()  # Set the event when "DONE" is received
        
        if all(substr in self.POSITION_PREFIXS for substr in line): # if these substrings are present we know the board is sending positional data
            for substr, key in zip(self.POSITION_PREFIXS, self.control_board.positions):
                # extract the number that comes after the prefix and before the next space
                number = (line.split(substr)[1]).split(" ")[0]
                self.control_board[key] = float(number)
            
            
        if "B:" in line: # 
            # Extract the temperature from the line "B:{temp} ..."
            temp = line.split("B:")[1]
            temp = temp.split(" ")[0]
            self.control_board.hotplate_temperature = float(temp)
            
    def connection_lost(self, exc):
        """Handle the loss of connection."""
        if exc:
            self.logger.error(f"Serial connection lost: {exc}")
        else:
            self.logger.info("Serial connection closed")
        self.control_board.disconnect()
