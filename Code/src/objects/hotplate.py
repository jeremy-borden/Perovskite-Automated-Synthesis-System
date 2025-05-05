import threading
import serial
import time
import logging

class Hotplate(threading.Thread):
    MAX_TEMPERATURE_C = 540

    def __init__(self):
        super().__init__(name="Hotplate", daemon=True)
        self.logger = logging.getLogger("Main Logger")
        
        self.serial = None
        self.current_temperature_c = 0
        self.target_temperature_c = 0
        
        self.start()
        time.sleep(2)  # Allow time for Arduino to reset
        
        
    def connect(self):
        """Connect to the control board and start the reader thread."""
        if self.is_connected():
            self.logger.error("Hotplate is already connected")
        
        port = "/dev/hotplate"
        try:
            self.serial = serial.Serial(port, 115200, timeout=None)
            self.logger.info(f"Connected to hotplate on port {port}")
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to hotplate: {e}")
    
    def disconnect(self):
        if not self.is_connected():
            return
        self.set_temperature(0)
        time.sleep(0.5)
        self.serial.close()
        self.logger.debug("Hotplate Disconnected")
            
    def is_connected(self) -> bool:
        return self.serial is not None and self.serial.is_open

    def send_message(self, message: str):
        try:
            self.serial.write(message.encode()) # utf-8
            time.sleep(0.2)
            response = self.serial.readline().decode().strip()
            if (response is not None and not ""):
                self.logger.debug(f"Raw response: {response}")
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            
            
            
    def get_temperature(self):
        """Read actual temperature from Arduino via serial."""
        if not self.is_connected():
            return
        
        try:
            self.serial.write(b"GET_TEMP\n") # utf-8
            time.sleep(0.5)
            response = self.serial.readline().decode().strip()
            #self.logger.debug(f"Raw response: {response}")
            temperature = None

            if response.startswith("TEMP:"):
                temperature = float(response.split(":")[1])
            else:
                self.logger.warning(f"Invalid response from Arduino: {response}")
        except Exception as e:
            self.logger.error(f"Error reading temperature: {e}")

        return temperature
        
    def set_temperature(self, temperature):
        """Send set temperature to Arduino and verify response."""
        if not self.is_connected():
            return
        
        if temperature > self.MAX_TEMPERATURE_C:
            self.logger.warning(f"Temperature {temperature} exceeds max limit of {self.MAX_TEMPERATURE_C}°C")
            return

        self.target_temperature_c = temperature
        command = f"SET_TEMP {temperature}\n"
        try:
            self.serial.flushInput()  # Clears the input buffer
            time.sleep(0.1)  # Small delay to ensure clean communication

            self.serial.write(command.encode())
            self.serial.flush()  # Ensure data is sent immediately
            time.sleep(0.1)  # Small delay to allow Arduino to process
        
        # Read response from Arduino
            response = self.serial.readline().decode().strip()
            if response.startswith("TARGET SET"):
                self.logger.info(f"Confirmed target temperature: {response}")
            else:
                self.logger.warning(f"Unexpected response: {response}")    

        except Exception as e:    
            self.logger.error(f"Error sending temperature command: {e}")

    def run(self):
        """Continuously read temperature from Arduino."""
        self.logger.info("Hotplate thread started.")
        while True:
            if self.is_connected():
                t = self.get_temperature()
                if t:
                    self.current_temperature_c = t
            time.sleep(1)


if __name__ == "__main__":
    hotplate = Hotplate()
    hotplate.set_temperature(50)  # Example: Set target temperature to 50°C
