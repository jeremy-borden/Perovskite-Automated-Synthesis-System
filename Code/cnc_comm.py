import serial

class GantryController:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def connect(self):
        if self.ser == None:
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
                
            except:
                print("could not connect to serial port")
                return False
        else:
            self.ser.open()
        print("connected to serial port")
        return True
            
    def disconnect(self):
        if(self.ser != None):
            self.ser.close()
        print("disconnected from serial port")

    def sendGCode(self, gcode: str):
        if(self.ser != None):
            self.ser.write(str.encode(gcode +"\r\n"))

    def receiveResponse(self):
        if(self.ser != None):
            return self.ser.readline().decode().strip()
        else:
            return None


c = GantryController('COM3', 115200)
c.connect()
c.sendGCode("G91")

c.sendGCode("G0 X100 Y100")
c.sendGCode("G0 X-100 Y-100")