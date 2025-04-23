import logging
import customtkinter as ctk
from queue import Queue
import os
import sys

# get current directory so we can import from outside guiFrames folder
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)
from drivers.controlboard_driver import ControlBoard
from objects.hotplate import Hotplate
from objects.pippete import PipetteHandler
from objects.vial_carousel import VialCarousel

class InfoFrame(ctk.CTkFrame):
    def __init__(self, master, control_board: ControlBoard, hotplate: Hotplate, pipette_handler: PipetteHandler, vial_carousel: VialCarousel):
        super().__init__(master=master,border_color="#1f6aa5",border_width=2, height=200)
        
        self.logger = logging.getLogger("Main Logger")
        self.control_board = control_board
        self.hotplate = hotplate
        self.pipette_handler = pipette_handler
        self.vial_carousel = vial_carousel
        
        # Title
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Info",
            justify="center",
            font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        
        # ---TOOLHEAD POSITION---
        self.toolhead_position_label = ctk.CTkLabel(
            master=self,
            text="Toolhead Position: X/X",
            justify="left",anchor="w",
            width=400,)
        self.toolhead_position_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        # ---HOTPLATE TEMPERATURE---
        self.hotplate_label = ctk.CTkLabel(
            master=self,
            text="Hotplate: X/X",
            justify="left",anchor="w",
            width=400,)
        self.hotplate_label.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        
        # ---PIPETTE STATUS---
        self.pipette_label = ctk.CTkLabel(
            master=self,
            text="Pipette: X/X",
            justify="left",anchor="w",
            width=400,)
        self.pipette_label.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        
        # ---CURRENT VIAL---
        self.vial_label =  ctk.CTkLabel(
            master=self,
            text="Vial",
            justify="left",anchor="w",
            width=400,)
        self.vial_label.grid(row=4,column=0, padx=5, pady=5, sticky="nw")

        self.update_information()
        
    def update_information(self):
        # Hotplate temperature
        if self.hotplate is not None:
            current_temperature = self.hotplate.current_temperature_c
            target_temperature  = self.hotplate.target_temperature_c
            self.hotplate_label.configure(text=f"Current/Target Hotplate Temperature | {current_temperature}/{target_temperature}")
        
        # Toolhead Position
        x=self.control_board.positions["X"]
        y=self.control_board.positions["Y"]
        z=self.control_board.positions["Z"]
        a=self.control_board.positions["A"]
        b=self.control_board.positions["B"]

        self.toolhead_position_label.configure(
            text=f"Toolhead Positon | X: {x}\tY: {y}\tZ: {z}")
        
        pipette = self.pipette_handler.get_pippete_index()
        self.pipette_label.configure(
            text=f"Current Pipette | {pipette}\nActuator Position | B: {b}")
        
        vial = self.vial_carousel.current_vial
        self.vial_label.configure(
            text=f"Current Vial | {vial}\nCarousel Position | A: {a}")

        self.after(200, self.update_information)
        