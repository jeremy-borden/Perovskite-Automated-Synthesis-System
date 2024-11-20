from smbus2 import SMBus


MAX_TEMPERATURE = 300

class HotplateDriver:
    def __init__(self, address):
        self.bus = SMBus(1)
        self.address = address
        
    def setTemperature(self, temperature):
        temperature = max(0, min(300, temperature)) # clamp temperature values between 0 and 300
        
        data = int((temperature/MAX_TEMPERATURE) * 4095)
        
        self.bus.write_byte_data(self.address, 0x00, data)
        
    def getTemperature(self):
       
        return 0