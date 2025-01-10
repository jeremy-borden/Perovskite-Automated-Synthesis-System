import customtkinter as ctk
from drivers.controlboard_driver import ControlBoard
from guiFrames.gantry_frame import GantryFrame


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("500x500")
    control_board = ControlBoard("COM3", 250000)
    gantry_frame = GantryFrame(app, control_board)
    gantry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    app.mainloop()