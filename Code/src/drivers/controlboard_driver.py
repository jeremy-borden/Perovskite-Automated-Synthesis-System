import logging
import threading
import serial
import serial.threaded



# DEFAULT_SPEED = 1000


class ControlBoard():
    """Class to control the octopus v1.1 control board.
    """

    def __init__(self, logger: logging.Logger):

        self.serial = None
        self._connect("COM3")
        self.logger = logger
        self.received_ok = threading.Event()

        self.reader_thread = serial.threaded.ReaderThread(
            self.serial, lambda: ControlBoardLineReader(self.logger, self))
        self.reader_thread.daemon = True
        self.reader_thread.start()

    def _connect(self, port: str):
        """Connect to the control board."""
        if (self.serial is not None):
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

    def goto(self, x: float = None, y: float = None, z: float = None, speed: int = 1000):
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