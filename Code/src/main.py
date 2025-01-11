import customtkinter as ctk
import threading

from drivers.controlboard_driver import ControlBoard

from guiFrames.hotplate_frame import HotplateFrame
from guiFrames.gantry_frame import GantryFrame
from guiFrames.gripper_frame import GripperFrame
from guiFrames.pipette_frame import PipetteFrame
from guiFrames.procedure_frame_copy import ProcedureFrame

control_board = ControlBoard("COM4", 115200)



# Create and run GUI
app = ctk.CTk()
app.geometry("1200x1000")

procedure_frame = ProcedureFrame(app)
procedure_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


hotplate_frame = HotplateFrame(app)
hotplate_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

gripper_frame= GripperFrame(app)
gripper_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

pipette_frame = PipetteFrame(app)
pipette_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


app.mainloop()
