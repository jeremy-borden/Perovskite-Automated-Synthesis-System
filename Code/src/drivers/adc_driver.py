import board
import digitalio
import adafruit_max31856



class ADC():
    def __init__(self):
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)
        cs.direction = digitalio.Direction.OUTPUT
        self.adc = adafruit_max31856.MAX31856(spi,cs)
        
    def get_temperature(self):
        return self.adc.temperature