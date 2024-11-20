import customtkinter as ctk

from componentDrivers import hotplate_driver
from componentDrivers.gantry_driver import GantryDriver

from guiFrames.hotplate_frame import HotplateFrame
from guiFrames.gantry_frame import GantryFrame
from guiFrames.gripper_frame import GripperFrame
from guiFrames.pipette_frame import PipetteFrame
from guiFrames.procedure_frame import ProcedureFrame


gantry_driver = GantryDriver("COM3", 115200)
hotplate_driver = hotplate_driver.HotplateDriver(0x60)


# Create and run GUI
app = ctk.CTk()
app.geometry("1200x1000")

procedure_frame = ProcedureFrame(app)
procedure_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

gantry_frame = GantryFrame(app, gantry_driver)
gantry_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", rowspan = 2)

hotplate_frame = HotplateFrame(app)
hotplate_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

gripper_frame= GripperFrame(app)
gripper_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

pipette_frame = PipetteFrame(app)
pipette_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

app.mainloop()