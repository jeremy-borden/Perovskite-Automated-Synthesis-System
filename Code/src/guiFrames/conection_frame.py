from src.drivers.spincoater_driver import SpinCoater
from src.drivers.controlboard_driver import ControlBoard
import customtkinter as ctk
from PIL import Image
import sys
import os

# get current directory so we can import from outside guiFrames folder
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(path)


class ConnectionFrame(ctk.CTkFrame):
    def __init__(self, master, control_board: ControlBoard, spincoater: SpinCoater = None):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2,
            height=400
        )

        self.control_board = control_board
        self.spincoater = spincoater

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
            light_image=Image.open("Code/src/guiImages/controlboard.png"),
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
            width=100,
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
            font=("Arial", 10)
        )
        self.control_board_status_label.grid(
            row=3, column=0, padx=5, pady=5, sticky="nw")

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
        self.command_entry.grid(row=4, column=1, rowspan=2, padx=5, pady=5, sticky="nw")
        self.command_entry.bind("<Return>", self._send_entry)
        
        self.send_entry_button = ctk.CTkButton(
            master=self,
            text="Send",
            width=50,
            height=50,
            command=self._send_entry
        )
        self.send_entry_button.grid(row=4, column=2, rowspan=2, padx=5, pady=5, sticky="nw")
        self._update()

    def _update(self):

        if not self.control_board.is_connected():
            self.connect_control_board_button.configure(state="normal")
            self.control_board_status_label.configure(
                text="Status: Disconected")
        else:
            self.control_board_status_label.configure(text="Status: Connected")

        self.after(1000, self._update)

    def _connect_control_board(self):
        self.control_board.connect()
        self.connect_control_board_button.configure(state="disabled")

    def _set_command_destination(self, value: str):
        self.command_destination = value
        self.command_destination_label.configure(text=f"Destination: {self.command_destination}")

    def _send_entry(self, event=None):
        value = self.command_entry.get()
        
        if value == "":
            return
        
        if self.command_destination == "Control Board":
            self.control_board.send_message(value)
