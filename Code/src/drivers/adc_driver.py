import board
import digitalio
import adafruit_max31856
from adafruit_max31856 import ThermocoupleType
import logging


class ADC():
    def __init__(self):
        self.logger = logging.getLogger("Main Logger")
        try:
            spi = board.SPI()
            cs = digitalio.DigitalInOut(board.D5)
            #cs.direction = digitalio.Direction.OUTPUT
            self.adc = adafruit_max31856.MAX31856(spi,cs, ThermocoupleType.K)
        except Exception as e:
            self.logger.error("Failed to connect to ADC")
            self.adc = None
        
    def get_temperature(self):
        
        if self.adc is None:
            return
        
        for k in self.adc.fault:
            self.logger.debug(f"{k}: {self.adc.fault[k]}")
        
        self.adc.initiate_one_shot_measurement()
        while(self.adc.oneshot_pending):
            pass
        t = self.adc.unpack_temperature()
        return t