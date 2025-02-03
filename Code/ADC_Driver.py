from smbus2 import SMBus
import math
import time


class ADC():
    """FOR TESTING ONLY"""
    # Thermistor constants
    R_Room = 10000   # Resistance at 25C
    T_Room = 25      # Temperature at 25C

    Beta = 4000  # Random Beta coefficient (experimentally deduce later)
    VD_Resistor = 10000  # Resistor value in the voltage divider
    
    def __init__(self, address, resolution_bits: int = 12):
        self.address = address
        self.bus = SMBus(1)
        self.resolution_bits = resolution_bits
          
    def read_adc(self, channel):
        """Reads ADC value from the given channel (0-3 for a typical 4-channel ADC)."""
        if channel < 0 or channel > 3:
            return ValueError("Invalid ADC channel. Must be 0-3.")

        adc_command = 0x40 | (channel << 4)  # Example (varies by ADC)
        self.bus.write_byte(self.address, adc_command)
        time.sleep(0.1)  # Small delay for ADC to process

        # Read data (assuming 2 bytes response for 12-bit ADC)
        data = self.bus.read_word_data(self.address, adc_command)
        adc_value = ((data & 0xFF) << 8) | (data >> 8)  # Convert little-endian
        
        return adc_value & ((1 << self.resolution_bits) - 1)  # Mask to ADC resolution
    
    def readLevel(self, level: float):
        if level < 0:
            level = 0
        if level > 1:
            level = 1
        
        adc_data = int(level * (pow(2, self.resolution_bits) - 1))  # 12-bit resolution, 0-4095
        print(adc_data)
        
    # def adcTempCalc(self, adc_data):
    #     voltage = (adc_data / 4095.0) * 3.3 #assuming 12 bit resolution and 3.3V is the reference voltage
    #     resistance = VD_Resistor * ((3.3/ voltage) - 1)
        
    #     #calculating temperature from resistance
    #     temperature = resistance / R_Room #(R/R0)
    #     temperature = math.log(resistance) #ln(R/Ro)
    #     temperature /= Beta #1/B * ln(R/R0)
    #     temperature += 1.0 / (T_Room + 273.15)
    #     temperature = 1.0 / temperature
    #     temperature -= 273.15
    #     return temperature
        
        