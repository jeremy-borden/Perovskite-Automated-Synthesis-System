import threading

import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)

from drivers.adc_driver import ADC
from drivers.dac_driver import DAC
from time import sleep

class Hotplate(threading.Thread):
    def __init__(self, max_temperature: int, dac: DAC, adc: ADC):
        self.max_temperature = max_temperature
        self.dac = dac
        self.adc = adc
        
        self.current_temperature = 0
        self.target_temperature = 0
        
    def set_temperature(self, temperature: int):
        level = temperature/self.max_temperature
        self.target_temperature = temperature
        self.dac.set_value(level)
        
    def get_temperature(self):
        return self.current_temperature
    
    
    def wait_for_temperature(self, target_temperature: int, threshold: int):
        
        if target_temperature > self.max_temperature:
            return
        
        while abs(self.current_temperature - target_temperature) > threshold:
            sleep(1)
            
    def run(self):
        """Continuously read from the ADC to update temperature
        """
        while True:
            
            self.current_temperature = self.adc.get_temperature()
            sleep(0.5)