import time
import serial

class Gantry_Component:
    def __init__(self, serialPortID):
        self.serialPortID = serialPortID # Store the serial port ID
        self.serialPort=serial.Serial(serialPortID, 115200) # Establish connection with printer; change serial port ID if necessary
        
    def WriteToSerialPort(self, message):
        self.serialPort.write(str.encode(message))
        
    def WriteToSerialPort(self, messages):
        for message in messages:
            self.serialPort.write(str.encode(message))
            time.sleep(0.1)

    def CloseSerialPort(self):
        self.serialPort.close()
        
    def OpenSerialPort(self):
        self.serialPort.open()
    
    