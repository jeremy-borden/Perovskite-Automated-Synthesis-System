import customtkinter as ctk
from PIL import Image
import sys
import os

# get current directory so we can import from outside guiFrames folder
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(path)
from objects.hotplate import Hotplate
from drivers.controlboard_driver import ControlBoard
from drivers.spincoater_driver import SpinCoater
from drivers.camera_driver import Camera
from drivers.spectrometer_driver import Spectrometer

class ConnectionFrame(ctk.CTkFrame):
    def __init__(self, master, control_board: ControlBoard, spin_coater: SpinCoater, hotplate: Hotplate, camera: Camera, spectrometer: Spectrometer):  # Add spectrometer parameter
        super().__init__(master=master,border_color="#1f6aa5",border_width=2,height=400)

        self.control_board = control_board
        self.spin_coater = spin_coater
        self.hotplate = hotplate
        self.camera = camera
        self.spectrometer = spectrometer
        self.command_destination = "Control Board"
        
        # Title
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Connection Manager",
            justify="left",anchor="w",
            font=("Arial", 20, "bold"))
        self.title_label.grid(
            row=0, column=0, columnspan=5, 
            padx=5, pady=5, sticky="nw")
        # Control Board
        self.control_board_connection = NameLater(
            self, "controlboard.png",self._connect_control_board)
        self.control_board_connection.grid(
            row=1, column=0,
            padx=5,pady=5,
            sticky="nw")
        # Spin Coater
        self.spin_coater_connection = NameLater(
            self, "spin_coater.png",self._connect_spin_coater)
        self.spin_coater_connection.grid(
            row=1, column=1,
            padx=5,pady=5,sticky="nw")
        # Hotplate
        self.hotplate_connection = NameLater(
            self, "hotplate.png",self._connect_hotplate)
        self.hotplate_connection.grid(
            row=1, column=2,
            padx=5,pady=5,sticky="nw")
        # Spectrometer
        self.spectrometer_connection = NameLater(
            self, "spectrometer.png",self._connect_spectrometer)
        self.spectrometer_connection.grid(
            row=1, column=3,
            padx=5,pady=5,sticky="nw")
        # Camera
        self.camera_connection = NameLater(
            self, "camera.png",self._connect_camera)
        self.camera_connection.grid(
            row=1, column=4,
            padx=5,pady=5,sticky="nw")

        # command entry
        self.command_destination_label = ctk.CTkLabel(
            master=self,
            text=f"Destination:",
            width=80,
            anchor="w"
        )
        self.command_destination_label.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        
        self.command_entry_destination = ctk.CTkOptionMenu(
            master=self,
            values=["Control Board", "Spincoater", "Hotplate", "Spectrometer"],
            width=120,
            command=self._set_command_destination
        )
        self.command_entry_destination.grid(row=5, column=0, padx=5, pady=5, sticky="nw")

        self.command_entry = ctk.CTkEntry(
            master=self,
            width=300,
            height=50
        )
        self.command_entry.grid(row=4, column=1, rowspan=2, columnspan=3, padx=5, pady=5, sticky="nw")
        self.command_entry.bind("<Return>", self._send_entry)
        
        self.send_entry_button = ctk.CTkButton(
            master=self,text="Send",
            width=50,height=50,
            command=self._send_entry)
        self.send_entry_button.grid(
            row=4, column=4, rowspan=2,
            padx=5, pady=5, sticky="nw")
        
        self._update()

    def _update(self):
        self.control_board_connection.set_connection_status(self.control_board.is_connected())
        self.spin_coater_connection.set_connection_status(self.spin_coater.is_connected())
        self.hotplate_connection.set_connection_status(self.hotplate.is_connected())
        self.spectrometer_connection.set_connection_status(self.spectrometer.is_connected())
        self.camera_connection.set_connection_status(self.camera.is_connected())

        self.after(1000, self._update)

    def _connect_control_board(self):
        self.control_board.connect()
        self.control_board_connection.set_connection_status(True)
    
    def _connect_spin_coater(self):
        self.spin_coater.connect()
        self.spin_coater_connection.set_connection_status(True)
        
    def _connect_hotplate(self):
        self.hotplate.connect()
        self.hotplate_connection.set_connection_status(True)
        
    def _connect_spectrometer(self):
        self.spectrometer.connect()
        self.spectrometer_connection.set_connection_status(True)
        
    def _connect_camera(self):
        self.camera.connect()
        self.camera_connection.set_connection_status(True)
        
    def _set_command_destination(self, value: str):
        self.command_destination = value
        self.command_destination_label.configure(text=f"Destination:")

    def _send_entry(self, event=None):
        value = self.command_entry.get()
        
        if value == "":
            return
        
        if self.command_destination == "Control Board":
            self.control_board.send_message(value)
        elif self.command_destination == "Spincoater":
            self.spin_coater.send_message(value)
        elif self.command_destination == "Spectrometer":
            self.spectrometer.send_message(value)
        elif self.command_destination == "Hotplate":
            self.hotplate.send_message(value)
            
class NameLater(ctk.CTkFrame):
    def __init__(self, master, image_path, command, default_port: int = 0):
        super().__init__(master=master)
        # Image
        image = ctk.CTkImage(
            light_image=Image.open(f"guiImages/{image_path}"),
            size=(100, 100))
        self.image_label = ctk.CTkLabel(
            master=self, text="", image=image,
            width=100, height=100)
        self.image_label.grid(
            row=0, column=0, columnspan=2,
            padx=5, pady=5, 
            sticky="nw")
        # Status Label
        self.status_label = ctk.CTkLabel(
            master=self, text="Status: Disconected",
            width=100, height=20,
            font=("Arial", 10))
        self.status_label.grid(
            row=1, column=0, columnspan=2,
            padx=5, pady=5, 
            sticky="nw")
        # Connect button
        self.connect_button = ctk.CTkButton(
            master=self, text="Connect",
            width=100, height=20,
            command=command)
        self.connect_button.grid(
            row=2, column=0, 
            padx=5, pady=5, 
            sticky="nw")
      

    def set_connection_status(self, connected: bool):
        if connected:
            self.status_label.configure(text="Status: Connected")
            self.connect_button.configure(state="disabled")
        else:
            self.status_label.configure(text="Status: Disconected")
            # check prevents it from glitching out and updating constantly
            if self.connect_button.cget("state") != "normal":
                self.connect_button.configure(state="normal")
    
if __name__ == "__main__":
    app = ctk.CTk()
    ctk.set_appearance_mode("dark")
    app.geometry("1200x1000")
    control_board_connection = NameLater(
        app, "controlboard.png",print("hi"))
    control_board_connection.grid(
        row=1, column=0,
        padx=5,pady=5,
        sticky="nw")
    app.mainloop()