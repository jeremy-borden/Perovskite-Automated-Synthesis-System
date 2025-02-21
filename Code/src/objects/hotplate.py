import os
import sys
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)

from drivers.dac_driver import DAC
from time import sleep

class Hotplate():
    def __init__(self, max_temperature: int, dac: DAC):
        self.max_temperature = max_temperature
        self.dac = dac
        
        self.temperature = 0
        
    def set_temperature(self, temperature: int):
        if temperature > self.max_temperature:
            temperature = self.max_temperature
        elif temperature < 0:
            temperature = 0
       
        level = temperature/self.max_temperature
        self.dac.setVoltageLevel(level)
        
    def wait_for_temperature(self, target_temperature: int, threshold: int):
        
        if target_temperature > self.max_temperature:
            return
        
        while abs(self.temperature - target_temperature) > threshold:
            sleep(1)
            