
import customtkinter as ctk
from queue import Queue

class InfoFrame(ctk.CTkFrame):
    def __init__(self, master, data_dict):
        super().__init__(master)
        self.data = data_dict
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=0, padx=5, pady=5, sticky="new")

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
        if not self.data["current_temp"].empty():
            current_temperature = self.data["current_temp"].get_nowait()
            self.hotplate_label.configure(text=f"Hotplate: {current_temperature}/{current_temperature}")

        self.after(1000, self.update_information)