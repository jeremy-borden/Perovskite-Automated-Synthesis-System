# import logging
# import smbus2

# class DAC():
#     def __init__(self):
#         self.logger = logging.getLogger("Main Logger")
#         self.bus = smbus2.SMBus(1)
#         self.address = 0x60
#         self.resolution_bits = 12
        
#     def set_value(self, level: float):
#         """Set the voltage of the DAC. 0 means min voltage, 1 means max"""
#         if level < 0:
#             level = 0
#         elif level > 1:
#             level = 1
        
#         data = int(level * (pow(2, self.resolution_bits) - 1))
#         self.logger.debug(f"data: {data}")
#         # somehow this works (up to 200C) and i have no idea why
#         high_byte = (data >> 8) & 0x0F  # Upper 4 bits
#         low_byte = data & 0xFF  # Lower 8 bits
#         self.bus.write_i2c_block_data(self.address, high_byte, [low_byte])

# adafruit library version
import logging
import board
import busio
import adafruit_mcp4725

class DAC():
    def __init__(self):
        self.logger = logging.getLogger("Main Logger")
        i2c = busio.I2C(board.SCL, board.SDA)
        try:
            self.dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)
        except ValueError as e:
            self.logger.error(f"Could not connect to DAC: {e}")
            self.dac = None

    def set_value(self, value: float):
        """Set the voltage of the DAC. Values are clamped between 0 (min) and 1 (max)"""
        if self.dac is None:
            return
        
        if value < 0:
            value = 0
        elif value > 1:
            value = 1
        self.logger.debug(f"value is: {self.dac.raw_value}")
        self.logger.debug(value)
        self.dac.normalized_value = value
        

