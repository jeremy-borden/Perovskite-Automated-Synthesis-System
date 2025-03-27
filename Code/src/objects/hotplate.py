'''

import logging
import threading

import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)


from drivers.adc_driver import ADC
from drivers.dac_driver import DAC
from time import sleep



class Hotplate(threading.Thread):
    MAX_TEMPERATURE_C: int = 540
    
    def __init__(self, dac: DAC, adc: ADC):
        super().__init__(name="Hotplate",daemon=True)
        self.dac = dac
        self.adc = adc
        
        self._current_temperature_c = 0
        self.target_temperature_c = 0
        self.logger = logging.getLogger("Main Logger")
    def set_temperature(self, temperature_c: int):
        if temperature_c > self.MAX_TEMPERATURE_C:
            return
        
        level = temperature_c/self.MAX_TEMPERATURE_C
        self.target_temperature_c = temperature_c
        self.dac.set_value(level)
        
    def get_temperature(self):
        return self._current_temperature_c
            
    def run(self):
        """Continuously read from the ADC to update temperature"""
        while True:
            self._current_temperature_c = self.adc.get_temperature()
            print(f"Temperature Read: {self._current_temperature_c} C")
            sleep(1)
            '''
import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)
            
import threading
import serial
import time
import logging

class Hotplate(threading.Thread):
    MAX_TEMPERATURE_C = 540

    def __init__(self, serial_port="/dev/ttyUSB0", baud_rate=115200):
        super().__init__(name="Hotplate", daemon=True)
        self.serial_port = serial.Serial(serial_port, baud_rate, timeout=1)
        self._current_temperature_c = 0
        self.target_temperature_c = 0
        self.logger = logging.getLogger("Main Logger")

    def get_temperature(self):
        """Read actual temperature from Arduino"""
        self.serial_port.write(b"GET_TEMP\n")  # Request temperature from Arduino
        response = self.serial_port.readline().decode().strip()
        try:
            self._current_temperature_c = float(response)
        except ValueError:
            self.logger.error(f"Invalid temperature data: {response}")
        return self._current_temperature_c

    def set_temperature(self, temperature):
        """Send set temperature to Arduino"""
        self.target_temperature_c = temperature
        command = f"SET_TEMP {temperature}\n"
        self.serial_port.write(command.encode())

    def run(self):
        """Continuously update the temperature"""
        while True:
            self.get_temperature()
            print(f"Actual Temperature: {self._current_temperature_c:.2f} C")
            time.sleep(1)

if __name__ == "__main__":
    hotplate = Hotplate()
    hotplate.set_temperature(50)  # Example: Set temp to 50°C
    hotplate.run()

