import logging
import serial
import serial.threaded
import threading
# SPINCOATER COMMANDS
# spc set pcmode
# spc add step {rpm} {time}
# spc get steps
# spc del steps
# spc run
# spc stop

class SpinCoater():
    """ Class to control the spin coater """
    def __init__(self):
        self.logger = logging.getLogger("Main Logger")
        self.serial = None
        self.reader_thread = None
        
        self.done = threading.Event()
        
    def connect(self, port_num):
        if self.is_connected():
            self.logger.error("Spin Coater is already connected")
            return
        port = "/dev/ttyACM"+str(port_num)
        try:
            self.serial = serial.Serial(port, 9600, timeout=None)
            self._begin_reader_thread()
            self.set_pc_mode()
            self.logger.info(
                f"Connected to spincoater on port {port}")
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to spincoater: {e}")
               
    def disconnect(self):
        if not self.is_connected():
            return
        self.serial.close()
        self.logger.debug("Spin Coater Disconnected")
        
    def is_connected(self) -> bool:
        return (self.serial is not None) and (self.serial.is_open)

    def _begin_reader_thread(self):
        self.reader_thread = serial.threaded.ReaderThread(
            serial_instance=self.serial,
            protocol_factory=lambda: SpinCoaterLineReader(
                self.logger, self)
        )
        self.reader_thread.daemon = True
        self.reader_thread.start()
        
    def send_command(self, message: str):
        if self.serial is None:
            self.logger.error("Serial is not connected")
            return

        self.reader_thread.write(message.encode("ascii"))
        self.logger.debug(f"Sending command: {message}")
        
        
        
    def stop(self):
        self.send_message("spc stop")
        
    def run(self, wait_to_finish: bool = False):
        self.send_message("spc run")
        self.done.clear()
        if wait_to_finish:
            self.done.wait()
        
    def add_step(self, rpm: int, time_seconds:float):
        self.send_message(f"spc add step {rpm} {time_seconds}")
    
    def clear_steps(self):
        self.send_message("spc del steps")
        
    def set_pc_mode(self):
        self.send_message("spc set pcmode")
        
    


class SpinCoaterLineReader(serial.threaded.LineReader):
    """Class to read lines from the spin coater on a separate thread"""
    
    TERMINATOR = b"\n"
    def __init__(self, logger: logging.Logger, spin_coater: SpinCoater):
        super().__init__()
        self.logger = logger
        self.spin_coater = spin_coater

    def handle_line(self, line: str):
        line = line.strip()
        self.logger.debug(f"Received: {line}")
        
        if line == "done":
            self.spin_coater.done.set()
            
    
    def connection_lost(self, exc):
        """Handle the loss of connection."""
        if exc:
            self.logger.error(f"Serial connection lost: {exc}")
        else:
            self.logger.info("Serial connection closed")
        self.spin_coater.disconnect()