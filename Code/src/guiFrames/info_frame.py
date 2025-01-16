import customtkinter as ctk
from queue import Queue
import os
import sys

# get current directory so we can import from outside guiFrames folder
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)
from src.drivers.controlboard_driver import ControlBoard

class InfoFrame(ctk.CTkFrame):
    def __init__(self, master, control_board: ControlBoard):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2)

        self.control_board = control_board
        
        # Title
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Info",
            justify="center",
            font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="new")

        # info
        self.hotplate_label = ctk.CTkLabel(
            master=self,
            text="Hotplate: X/X",
            justify="left",
            anchor="w",
            width=400,)
        self.hotplate_label.grid(row=1, column=0, padx=20, pady=20)
        
        self.pipette_label = ctk.CTkLabel(
            master=self,
            text="Pipette: X/X",
            justify="left",
            anchor="w",
            width=400,)
        self.pipette_label.grid(row=2, column=0, padx=20, pady=20)
        
        self.update_information()
        
    def update_information(self):
        current_temperature = self.control_board.hotplate_temperature
        self.hotplate_label.configure(text=f"Hotplate: {current_temperature}/{current_temperature}")

        self.after(1000, self.update_information)