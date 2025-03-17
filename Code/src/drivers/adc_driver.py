import board
import digitalio
import adafruit_max31856
import logging


class ADC():
    def __init__(self):
        self.logger = logging.getLogger("Main Logger")
        try:
            spi = board.SPI()
            cs = digitalio.DigitalInOut(board.D5)
            cs.direction = digitalio.Direction.OUTPUT
            self.adc = adafruit_max31856.MAX31856(spi,cs)
        except Exception as e:
            self.logger.error("Failed to connect to ADC")
            self.adc = None
        
    def get_temperature(self):
        if self.adc is None:
            return
        
        return self.adc.temperature