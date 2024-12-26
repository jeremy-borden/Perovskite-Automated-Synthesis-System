import serial
import threading
import queue

DEFAULT_SPEED = 1000

class ControlBoard:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connect()
        
        self.message_queue = queue.Queue()
        self.thread = threading.Thread(target=self.receiveMessage, args=())
        self.thread.start()

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

    def sendGCode(self, gcode: str, wait_for_response: bool = False):
        if(self.ser == None):
            return
        
        self.ser.write(str.encode(gcode +"\r\n"))
        
        
    def receiveMessage(self):
        if(self.ser == None):
            return
        
        while True:
            if(self.ser.inWaiting() != 0):
                message = self.ser.readline().decode().strip()
                self.message_queue.put(message)
                print(message)