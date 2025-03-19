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
            cs = digitalio.DigitalInOut(board.D8)
            cs.direction = digitalio.Direction.OUTPUT
            self.adc = adafruit_max31856.MAX31856(spi,cs, ThermocoupleType.K)
            self._set_continuous_mode()
            self.logger.info("ADC initialized in continuous mode.")
            
        except Exception as e:
            self.logger.error("Failed to connect to ADC")
            self.adc = None
    
    def _set_continuous_mode(self):
        try:
            cr0 = self.adc._read_u8(0x00)
            cr0 |= 0x80
            self.adc._write_u8(0x00, cr0)
            self.logger.debug("ADC set to continuous mode (CMODE=1)")  
        except Exception as e:
            self.logger.error(e)
            
    def get_temperature(self):
        
        if self.adc is None:
            return
        
        for k in self.adc.fault:
            if self.adc.fault[k] is True:
                self.logger.debug(f"{k}: {self.adc.fault[k]}")
        
        #self.adc.initiate_one_shot_measurement()
        #while(self.adc.oneshot_pending):
            #pass
        #t = self.adc.unpack_temperature()
        
        try:
             temp = self.adc.temperature
             return temp
        except Exception as e:
            self.logger.error(f"Failed to read temperature: {e}")
            return None
        #while(self.adc.conversion_mode_pending):
            #pass
        #t = self.adc.unpack_temperature()
        #return t