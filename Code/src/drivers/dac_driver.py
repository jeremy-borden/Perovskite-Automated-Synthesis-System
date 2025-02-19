from smbus2 import SMBus

class DAC():
    def __init__(self, address, resolution_bits: int = 12):
        self.bus = SMBus(1)
        self.address = address
        self.resolution_bits = resolution_bits
        
    def setVoltageLevel(self, level: float):
        """Set the voltage of the DAC. 0 means min voltage, 1 means max"""
        if level < 0:
            level = 0
        elif level > 1:
            level = 1
        print(level)
        data = int(level * (pow(2, self.resolution_bits) - 1))
        print(data)
        
        high_byte = (data >> 8) & 0x0F  # Upper 4 bits
        low_byte = data & 0xFF  # Lower 8 bits
        self.bus.write_i2c_block_data(self.address, high_byte, [low_byte])

