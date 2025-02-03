import customtkinter as ctk

from guiFrames.console_frame import ConsoleFrame
from guiFrames.procedure_frame import ProcedureFrame
from guiFrames.info_frame import InfoFrame
from guiFrames.camera_frame import CameraFrame
from guiFrames.conection_frame import ConnectionFrame

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x500")
        self.title("CTk example")
        
        

        

    # add methods to app
    def button_click(self):
        print("button click")

