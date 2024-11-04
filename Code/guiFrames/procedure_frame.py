import customtkinter as ctk
from pyparsing import col

class ProcedureFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.targetTempC = 0;
       
       
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=1, padx=50, pady=50, sticky="we")

        # Title Label
        self.titleLabel = ctk.CTkLabel(self, text="Procedure Overview", justify="center", font=("Arial", 20, "bold"))
        self.titleLabel.grid(row=0, column=3, padx=20, pady=20, sticky="nwes")
        
        self.progressLabel = ctk.CTkLabel(self, text="Procedure Progress: " + str(int(50)) + "%")
        self.progressLabel.grid(row=1, column=0, padx=20, pady=20, sticky="nwe")
        
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=2, column=0, padx=20, pady=20, sticky="nwe", columnspan = 2)
        self.progressbar.set(0.5)
        
        self.runlbl = ctk.CTkLabel(self, justify="left",text="Procedure Number: 3\nTime Elapsed: 10 minutes\nEstimated Time Remaining: 20 minutes")
        self.runlbl.grid(row=1, column=4, padx=20, pady=20, sticky="nwe")
