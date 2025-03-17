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
        
        self.current_temperature_c = 0
        self.target_temperature_c = 0
        
    def set_temperature(self, temperature_c: int):
        if temperature_c > self.MAX_TEMPERATURE_C:
            return
        
        level = temperature_c/self.MAX_TEMPERATURE_C
        self.target_temperature_c = temperature_c
        self.dac.set_value(level)
        
    def get_temperature(self):
        return self.current_temperature_c
            
    def run(self):
        """Continuously read from the ADC to update temperature"""
        while True:
            self.current_temperature_c = self.adc.get_temperature()
            sleep(0.5)