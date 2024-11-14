import customtkinter as ctk

from Code.componentDrivers.gantry_controller import GantryController
from guiframes.hotplate_frame import HotplateFrame
from guiframes.hotplate_frame import HotplateFrame
from guiframes.gantry_frame import GantryFrame
from guiframes.gripper_frame import GripperFrame
from guiframes.pipette_frame import PipetteFrame
from guiframes.procedure_frame import ProcedureFrame


gantry_controller = GantryController("COM3", 115200)


# Create and run GUI
app = ctk.CTk()
app.geometry("1200x1000")

procedure_frame = ProcedureFrame(app)
procedure_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan = 3)

gantry_frame = GantryFrame(app, gantry_controller)
gantry_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw", rowspan = 2)

hotplate_frame = HotplateFrame(app)
hotplate_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

gripper_frame= GripperFrame(app)
gripper_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

pipette_frame = PipetteFrame(app)
pipette_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

app.mainloop()