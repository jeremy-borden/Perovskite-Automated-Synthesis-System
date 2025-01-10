import customtkinter as ctk

class ProcedureFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.targetTempC = 0;
       
       
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=1, padx=50, pady=50, sticky="we")

        # Title Label
        self.titleLabel = ctk.CTkLabel(self, text="Procedure Overview", justify="center", font=("Arial", 20, "bold"))
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20, sticky="nwes", columnspan = 2)
        
        self.progressLabel = ctk.CTkLabel(self, justify="left", text="Procedure Progress: " + str(int(50)) + "%")
        self.progressLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ne")
        
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=2, column=1, padx=20, pady=20, sticky="ne")
        self.progressbar.set(0.5)
        
        self.runlbl = ctk.CTkLabel(self, justify="left",text="Procedure Number: 10\nTime Elapsed: 10 minutes\nEstimated Time Remaining: 20 minutes")
        self.runlbl.grid(row=3, column=0, padx=20, pady=20, sticky="ne")
        
        # mock Label
        self.angle_1_label = ctk.CTkLabel(self, text="Number of Procedures To Run: 30")
        self.angle_1_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

        # mock Value Entry
        self.angle_1_entry = ctk.CTkEntry(self, placeholder_text="...", width = 50)
        self.angle_1_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ne")
        
        # mock Button
        self.angle_1_button = ctk.CTkButton(self, text="Set", width = 50)
        self.angle_1_button.grid(row=1, column=2, padx=10, pady=10, sticky="ne")
        
        #########################
        # mock Label
        
