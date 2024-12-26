from smbus2 import SMBus

class ServoDriver:
    def __init__(self, address):
        self.bus = SMBus(1)
        self.address = address
        
    def setAngle(self, servoNum, angle):
        self.bus.write_byte_data(self.address, 0x00, servoNum)
        self.bus.write_byte_data(self.address, 0x01, angle)