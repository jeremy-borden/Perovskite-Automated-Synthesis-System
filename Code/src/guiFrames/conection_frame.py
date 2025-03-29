import customtkinter as ctk
from PIL import Image
import sys
import os

# get current directory so we can import from outside guiFrames folder
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(path)
from src.drivers.controlboard_driver import ControlBoard
from src.drivers.spincoater_driver import SpinCoater
from src.drivers.camera_driver import Camera
from src.drivers.spectrometer_driver import Spectrometer  # Add this import

class ConnectionFrame(ctk.CTkFrame):
    def __init__(self, master, control_board: ControlBoard, spin_coater: SpinCoater, camera: Camera, spectrometer: Spectrometer):  # Add spectrometer parameter
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2,
            height=400)

        self.control_board = control_board
        self.spin_coater = spin_coater
        self.camera = camera
        self.spectrometer = spectrometer  # Add this line

        # title
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Connection Manager",
            justify="left",
            anchor="w",
            font=("Arial", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nw")

        # control board
        control_board_image = ctk.CTkImage(
            light_image=Image.open("guiImages/controlboard.png"),
            size=(100, 100))
        self.control_board_image_label = ctk.CTkLabel(
            master=self,
            text="",
            image=control_board_image,
            width=100,
            height=100
        )
        self.control_board_image_label.grid(
            row=1, column=0, padx=5, pady=5, sticky="nw")

        self.connect_control_board_button = ctk.CTkButton(
            master=self,
            text="Connect",
            width=60,
            height=30,
            command=self._connect_control_board
        )
        self.connect_control_board_button.grid(
            row=2, column=0, padx=5, pady=5, sticky="nw")

        self.control_board_status_label = ctk.CTkLabel(
            master=self,
            text="Status: Disconected",
            width=100,
            height=20,
            font=("Arial", 10))
        self.control_board_status_label.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        
        self.control_board_usb_num = ctk.CTkEntry(master=self)
        self.control_board_usb_num.grid(row=2, column=1, padx=5, pady=5, sticky="nw")
        
        # spincoater
        spincoater_image = ctk.CTkImage(
            light_image=Image.open("guiImages/spincoater.png"),
            size=(100, 100))
        self.spincoater_image_label = ctk.CTkLabel(
            master=self,
            text="",
            image=spincoater_image,
            width=100,
            height=100
        )
        self.spincoater_image_label.grid(
            row=1, column=1, padx=5, pady=5, sticky="nw")

        self.connect_spincoater_button = ctk.CTkButton(
            master=self,
            text="Connect",
            width=100,
            height=30,
            command=self._connect_spincoater)
        self.connect_spincoater_button.grid(
            row=2, column=1, padx=5, pady=5, sticky="nw")

        self.spincoater_status_label = ctk.CTkLabel(
            master=self,
            text="Status: Disconected",
            width=100,
            height=20,
            font=("Arial", 10))
        self.spincoater_status_label.grid(
            row=3, column=1, padx=5, pady=5, sticky="nw")
        
        # camera
        camera_image = ctk.CTkImage(
            light_image=Image.open("guiImages/camera.png"),
            size=(100, 100))
        self.camera_image_label = ctk.CTkLabel(
            master=self,
            text="",
            image=camera_image,
            width=100,
            height=100
        )
        self.camera_image_label.grid(
            row=1, column=2, padx=5, pady=5, sticky="nw")

        self.connect_camera_button = ctk.CTkButton(
            master=self,
            text="Connect",
            width=100,
            height=30,
            command=self._connect_camera)
        self.connect_camera_button.grid(
            row=2, column=2, padx=5, pady=5, sticky="nw")

        self.camera_status_label = ctk.CTkLabel(
            master=self,
            text="Status: Disconected",
            width=100,
            height=20,
            font=("Arial", 10))
        self.camera_status_label.grid(
            row=3, column=2, padx=5, pady=5, sticky="nw")

        # spectrometer
        spectrometer_image = ctk.CTkImage(
            light_image=Image.open("guiImages/spectrometer.png"),
            size=(100, 100))
        self.spectrometer_image_label = ctk.CTkLabel(
            master=self,
            text="",
            image=spectrometer_image,
            width=100,
            height=100
        )
        self.spectrometer_image_label.grid(
            row=1, column=3, padx=5, pady=5, sticky="nw")

        self.connect_spectrometer_button = ctk.CTkButton(
            master=self,
            text="Connect",
            width=100,
            height=30,
            command=self._connect_spectrometer)
        self.connect_spectrometer_button.grid(
            row=2, column=3, padx=5, pady=5, sticky="nw")

        self.spectrometer_status_label = ctk.CTkLabel(
            master=self,
            text="Status: Disconnected",
            width=100,
            height=20,
            font=("Arial", 10))
        self.spectrometer_status_label.grid(
            row=3, column=3, padx=5, pady=5, sticky="nw")

        # command entry
        self.command_destination = "Control Board"

        self.command_destination_label = ctk.CTkLabel(
            master=self,
            text=f"Destination: {self.command_destination}",
            width=150,
            anchor="w"
        )
        self.command_destination_label.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        
        self.command_entry_destination = ctk.CTkOptionMenu(
            master=self,
            values=["Control Board", "Spincoater", "Spectrometer"],
            width=150,
            command=self._set_command_destination
        )
        self.command_entry_destination.grid(row=5, column=0, padx=5, pady=5, sticky="nw")

        self.command_entry = ctk.CTkEntry(
            master=self,
            width=300,
            height=50
        )
        self.command_entry.grid(row=4, column=1, rowspan=2, columnspan=2, padx=5, pady=5, sticky="nw")
        self.command_entry.bind("<Return>", self._send_entry)
        
        self.send_entry_button = ctk.CTkButton(
            master=self,
            text="Send",
            width=50,
            height=50,
            command=self._send_entry
        )
        self.send_entry_button.grid(row=4, column=3, rowspan=2, padx=5, pady=5, sticky="nw")
        self._update()

    def _update(self):
        
        if not self.spin_coater.is_connected():
            if self.connect_spincoater_button.cget("state") != "normal":
                self.connect_spincoater_button.configure(state="normal")
            self.spincoater_status_label.configure(
                text="Status: Disconected")
        else:
            self.spincoater_status_label.configure(text="Status: Connected")
            
        if not self.control_board.is_connected():
            if self.connect_control_board_button.cget("state") != "normal":
                self.connect_control_board_button.configure(state="normal")
            self.control_board_status_label.configure(
                text="Status: Disconected")
        else:
            self.control_board_status_label.configure(text="Status: Connected")
            
        if not self.camera.is_connected():
            if self.connect_camera_button.cget("state") != "normal":
                self.connect_camera_button.configure(state="normal")
            self.camera_status_label.configure(
                text="Status: Disconected")
        else:
            self.camera_status_label.configure(text="Status: Connected")

        if not self.spectrometer.is_connected():
            if self.connect_spectrometer_button.cget("state") != "normal":
                self.connect_spectrometer_button.configure(state="normal")
            self.spectrometer_status_label.configure(
                text="Status: Disconnected")
        else:
            self.spectrometer_status_label.configure(text="Status: Connected")

        self.after(1000, self._update)

    def _connect_control_board(self):
        n = self.control_board_usb_num.get()
        self.control_board.connect(n)
        self.connect_control_board_button.configure(state="disabled")
    
    def _connect_spincoater(self):
        
        self.spin_coater.connect()
        self.connect_spincoater_button.configure(state="disabled")
        
    def _connect_camera(self):
        self.camera.connect()
        self.connect_camera_button.configure(state="disabled")
        
    def _connect_spectrometer(self):
        self.spectrometer.connect()
        self.connect_spectrometer_button.configure(state="disabled")
        
    def _set_command_destination(self, value: str):
        self.command_destination = value
        self.command_destination_label.configure(text=f"Destination: {self.command_destination}")

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