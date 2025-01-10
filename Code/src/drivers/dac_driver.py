from smbus2 import SMBus

class DACDriver:
    def __init__(self, address, resolution):
        self.bus = SMBus(1)
        self.address = address
        self.resolution = resolution
        
    def setVoltageLevel(self, level: float):
        
        if(level < 0 or level > 1):
            return
        
        data = int(level * (pow(2, self.resolution) - 1))  # 12-bit resolution, 0-4095
        self.bus.write_byte_data(self.address, 0x00, data)
        
     
