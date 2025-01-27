import logging
import serial
import serial.threaded


class SpinCoater():
    """ Class to control the spin coater """
    def __init__(self, com_port: str, logger: logging.Logger):
        self.com_port = com_port
        self.logger = logger

        self.serial = None
        self.reader_thread = None
        
    def connect(self):
        if self.is_connected():
            self.logger.error("Spin Coater is already connected")
            return

        try:
            self.serial = serial.Serial(self.com_port, 9600, timeout=3) # try removing timeout?
            self._begin_reader_thread()
            self.logger.info(
                f"Connected to spincoater on port {self.com_port}")
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to spincoater: {e}")
               
    def disconnect(self):
        if not self.is_connected():
            return
        self.serial.close()
        self.logger.debug("Spin Coater Disconnected")
        
    def is_connected(self) -> bool:
        return self.serial is not None and self.serial.is_open

    def _begin_reader_thread(self):
        self.reader_thread = serial.threaded.ReaderThread(
            serial_instance=self.serial,
            protocol_factory=lambda: SpinCoaterLineReader(
                self.logger, self)
        )
        self.reader_thread.daemon = True
        self.reader_thread.start()
        
    def send_message(self, message: str):
        if self.serial is None:
            self.logger.error("Serial is not connected")
            return

        self.reader_thread.write(message.encode("ascii"))
        self.logger.debug(f"Sending command: {message}")


class SpinCoaterLineReader(serial.threaded.LineReader):
    """Class to read lines from the spin coater on a separate thread"""
    def __init__(self, logger: logging.Logger, spin_coater: SpinCoater):
        super().__init__()
        self.logger = logger
        self.spin_coater = spin_coater

    def handle_line(self, line: str):
        line = line.strip()
        self.logger.debug(f"Received: {line}")
    
    def connection_lost(self, exc):
        """Handle the loss of connection."""
        if exc:
            self.logger.error(f"Serial connection lost: {exc}")
        else:
            self.logger.info("Serial connection closed")
        self.spin_coater.disconnect()