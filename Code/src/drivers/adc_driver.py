'''
import board
import time
import digitalio
import adafruit_max31856
from adafruit_max31856 import ThermocoupleType
import logging
import smbus

I2C_ADDR = 0x08  # Arduino's I2C address

class ADC():
    def __init__(self):
        self.logger = logging.getLogger("Main Logger")
        self.bus = smbus.SMBus(1)  # Use I2C bus 1 for Raspberry Pi
        self.temperature = None

    def get_temperature(self):
        try:
            # Request 2 bytes from Arduino
            data = self.bus.read_i2c_block_data(I2C_ADDR, 0, 2)
            temp = (data[0] << 8) | data[1]  # Convert bytes to integer
            self.temperature = temp / 100.0  # Convert back to float
            return self.temperature
        except Exception as e:
            self.logger.error(f"I2C Read Error: {e}")
            return None
 '''   
import time
import board
import busio
import digitalio
import adafruit_max31856

class ADCDriver:
    def __init__(self):
        """Initialize SPI connection to MAX31856"""
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.cs = digitalio.DigitalInOut(board.D8)  # Chip Select (GPIO8 / CE0)
        self.cs.direction = digitalio.Direction.OUTPUT

        self.max31856 = adafruit_max31856.MAX31856(self.spi, self.cs)

    def get_temperature(self):
        """Read temperature from the MAX31856 ADC"""
        return self.max31856.temperature

if __name__ == "__main__":
    adc = ADCDriver()
    
    while True:
        temp = adc.get_temperature()
        print(f"Temperature: {temp:.2f}°C")
        time.sleep(1)

    '''def __init__(self):
        self.logger = logging.getLogger("Main Logger")
        try:
            spi = board.SPI()
            cs = digitalio.DigitalInOut(board.D8)
            cs.direction = digitalio.Direction.OUTPUT
            self.adc = adafruit_max31856.MAX31856(spi,cs, ThermocoupleType.K)
            self.adc.temperature_thresholds = (-1.5, 30.8)
            #self.adc.thermocouple_type = ThermocoupleType.k
            #print(f"Themocouple Type: {self.adc.thermocouple_type}")
        except Exception as e:
            self.logger.error("Failed to connect to ADC")
            self.adc = None
            
    def get_temperature(self):
        
        #if self.adc is None:
            #return
        if self.adc is None:
            self.logger.error("ADC initialization failed!")
            print("ERROR: ADC failed to initialize")    
            
        for k in self.adc.fault:
            if self.adc.fault[k] is True:
                #self.logger.debug(f"{k}: {self.adc.fault[k]}")
                print(f"Thermocouple fault detected: {k} -> {self.adc.fault[k]}")
                
        self.adc.auto_convert = False  # Disable auto-conversion
        self.adc.initiate_one_shot_measurement()  # Force a new measurement
        time.sleep(0.1)  # Wait for ADC to complete measurement
        temp = self.adc.unpack_temperature()
    
        print(f"Fresh Read: {temp} C")  # Debug output
        return temp
        
        #self.adc.initiate_one_shot_measurement()
       # while(self.adc.oneshot_pending):
            #pass
        ##t = self.adc.unpack_temperature()
        ##return t
        #try:
             #temp = self.adc.unpack_temperature()
             #return temp
       # except Exception as e:
            #self.logger.error(f"Failed to read temperature: {e}")
            #return None
'''
    
