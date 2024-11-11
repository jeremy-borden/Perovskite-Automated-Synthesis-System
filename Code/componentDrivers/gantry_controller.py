import serial
from time import sleep

class GantryController:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connect()

    def connect(self):
        if self.ser == None:
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=0.01)
                
            except:
                print("could not connect to serial port")
                return False
        else:
            self.ser.open()
        print("connected to serial port")
        return True
            
    def disconnect(self):
        if(self.ser != None ):
            self.ser.close()
            print("disconnected from serial port")

    def sendGCode(self, gcode: str):
        if(self.ser != None):
            self.ser.write(str.encode(gcode +"\r\n"))

    def receiveMessage(self):
        if(self.ser != None):
            
            return self.ser.readline().decode().strip()
        else:
            return None
