from smbus2 import SMBus

# class DAC():
#     def __init__(self, address, resolution_bits: int = 12):
#         self.bus = SMBus(1)
#         self.address = address
#         self.resolution_bits = resolution_bits
        
#     def setVoltageLevel(self, level: float):
#         """Set the voltage of the DAC. 0 means min voltage, 1 means max"""
#         if level < 0:
#             level = 0
#         elif level > 1:
#             level = 1
        
#         data = int(level * (pow(2, self.resolution_bits) - 1))
        
#         # somehow this works (up to 200C) and i have no idea why
#         high_byte = (data >> 8) & 0x0F  # Upper 4 bits
#         low_byte = data & 0xFF  # Lower 8 bits
#         self.bus.write_i2c_block_data(self.address, high_byte, [low_byte])

# adafruit library version
import board
import busio
import adafruit_mcp4725
class DAC():
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.dac = adafruit_mcp4725.MCP4725(i2c)
    
    
    def set_value(self, value: float):
        """Set the voltage of the DAC. Values are clamped between 0 (min) and 1 (max)"""
        if level < 0:
            level = 0
        elif level > 1:
            level = 1
        
        self.dac.normalized_value = value

