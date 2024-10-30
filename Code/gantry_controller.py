from numpy import pad
import serial
from time import sleep
import customtkinter as ctk
from guiFrames.gantry_frame import GantryFrame
from guiFrames.hotplate_frame import HotplateFrame

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




app = ctk.CTk()
app.geometry("800x800")
geee = GantryController("COM3", 115200)

g = GantryFrame(app, geee)
g.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
h = HotplateFrame(app)
h.grid(row=1, column=0, padx=10, pady=10, sticky="nw")


app.mainloop()
# for i in range(10):
# c.sendGCode("M105")
# print(c.receiveResponse())
# #c.sendGCode("M999")
# c.sendGCode("G28 X")
# c.sendGCode("M400")

# #     sleep(1)
# #c.sendGCode("G91")
# c.sendGCode("M201 X200 Y200 Z200")
# for i in range(10):
#     sleep(0.1)
#     c.sendGCode("G0 X100 F5000")
#     c.sendGCode("G0 X20 F5000")
#     c.sendGCode("M400")
#     # p = c.receiveResponse()
#     # print(p)
#     # while p != "ok":
#     #     sleep(0.3)
#     #     p = c.receiveResponse()
#     #     print(p)
        
# c.sendGCode("M400")
# c.sendGCode("M114")
# print(c.receiveResponse())

# # # c.sendGCode("G0 X-100 Y-100 F5000")

# # c.sendGCode("G0 Z10 F50")
# # c.sendGCode("G0 Z-10 F50")

# #c.sendGCode("M410")
