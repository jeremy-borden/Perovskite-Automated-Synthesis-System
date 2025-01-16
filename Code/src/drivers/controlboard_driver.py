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
        if self.serial is None:
            return
        
        self.serial.close()
            
    def is_connected(self) -> bool:
        if self.serial is None:
            return False
        if self.serial.is_open is False:
            return False
        
        return True
            
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

        if '\r\n' not in message:
            message += "\r\n"
        self.reader_thread.write(message.encode("utf-8"))
        self.logger.debug(f"Sending message: {message}")


    def _finish_move(self):
        """Wait for the move to finish"""
        self.send_message("M400")
        self.received_ok.clear()
        self.logger.debug("Waiting for move to finish")
        self.received_ok.wait()  # Wait until the move_finished event is set

    def goto(self, x: float, y: float, z: float, speed: int = 1000):
        """Move the toolhead to the specified coordiantes """
        self.send_message(f"G0 X{x} Y{y} Z{z} F{speed}")
        self._finish_move()

    def echo(self, message: str):
        """ Make the control board echo a message """
        self.send_message(f"M118 {message}")


class ControlBoardLineReader(serial.threaded.LineReader):
    """Class to read lines from the control board on a separate thread."""
    TERMINATOR = b"\n"

    def __init__(self, logger: logging.Logger, control_board: ControlBoard):
        """Initialize with optional logger."""
        super().__init__()
        self.logger = logger
        self.control_board = control_board

    def handle_line(self, line):
        """Process each received line."""
        line = line.strip()
        self.logger.debug(f"Received: {line}")
        if "ok" in line:
            self.control_board.received_ok.set()  # Set the event when "DONE" is received
        elif "B:" in line:
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
