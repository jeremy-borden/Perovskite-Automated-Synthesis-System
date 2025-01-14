from queue import Queue
import logging
import threading
import serial
import serial.threaded


# DEFAULT_SPEED = 1000


class ControlBoard():
    """Class to control the Octopus v1.1 control board"""

    def __init__(self, com_port: str, logger: logging.Logger, data_queue: Queue):

        self.logger = logger
        self.data_queue = data_queue

        self.serial = None
        self.reader_thread = None

        self._connect(com_port)
        self.received_ok = threading.Event()

    def _connect(self, port: str):
        """Connect to the control board and start the reader thread."""
        if (self.serial is not None):
            self.logger.error("Serial is already connected")
            return

        try:
            self.serial = serial.Serial(port, 250000, timeout=0.5)
            self._begin_reader_thread()
            self.logger.info(f"Connected to control board on port {port}")
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to control board: {e}")

    def _begin_reader_thread(self):
        self.reader_thread = serial.threaded.ReaderThread(
            serial_instance=self.serial,
            protocol_factory=lambda: ControlBoardLineReader(
                self.logger, self, self.data_queue)
        )
        self.reader_thread.daemon = True
        self.reader_thread.start()

    def _send_message(self, message: str):
        """Send a message to the control board.

        ### Args:
            message (str): The message to send.
        """
        if self.serial is None:
            self.logger.error("Serial is not connected")
            return
        if self.reader_thread is None:
            self.logger.error("Reader thread is not running")
            return

        if '\r\n' not in message:
            message += "\r\n"
        self.reader_thread.write(message.encode("utf-8"))
        self.logger.debug(f"Sending message: {message}")

    def send_message(self, message: str):
        """Send a message to the control board

        ### Args:
            message (str): The message to send.
        """
        self._send_message(message)

    def _finish_move(self):
        """Wait for the move to finish"""
        self._send_message("M400")
        self.received_ok.clear()
        self.logger.debug("Waiting for move to finish")
        self.received_ok.wait()  # Wait until the move_finished event is set

    def goto(self, x: float, y: float, z: float, speed: int = 1000):
        """Move the toolhead to the specified coordiantes """
        self._send_message(f"G0 X{x} Y{y} Z{z} F{speed}")
        self._finish_move()

    def echo(self, message: str):
        """ Make the control board echo a message """
        self._send_message(f"M118 {message}")


class ControlBoardLineReader(serial.threaded.LineReader):
    """Class to read lines from the control board on a separate thread."""
    TERMINATOR = b"\n"

    def __init__(self, logger: logging.Logger, control_board: ControlBoard, data_queue: Queue):
        """Initialize with optional logger."""
        super().__init__()
        self.logger = logger
        self.control_board = control_board
        self.data_queue = data_queue

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

            if self.data_queue.full():
                self.data_queue.get()
            self.data_queue.put(temp)
