import customtkinter as ctk

class PipetteFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.drawVolume = 0;
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=1, padx=50, pady=50, sticky="we")
        
        # Title Label
        self.titleLabel = ctk.CTkLabel(self, text="Pipette Control", justify="center", font=("Arial", 20, "bold"))
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20, sticky="we", columnspan = 5)
        
        # Current Pipette Label
        self.currentPipetteLabel = ctk.CTkLabel(self, text="Current Pipette: " + "None")
        self.currentPipetteLabel.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        
        # Target Pipette Label
        self.currentPipetteLabel = ctk.CTkLabel(self, text="Target Pipette: ")
        self.currentPipetteLabel.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        
        # Target Pipette Combobox
        self.pipetteCombo = ctk.CTkComboBox(self, values=["None", "Pipette 1", "Pipette 2", "Pipette 3", "Pipette 4"], state="readonly")
        self.pipetteCombo.grid(row=2, column=1, padx=10, pady=10, sticky="nw")
        self.pipetteCombo.set("None")
        
        # Draw Volume Label
        self.drawVolumeLabel = ctk.CTkLabel(self, text="Draw Volume: " + str(int(self.drawVolume)))
        self.drawVolumeLabel.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        
        # Draw Volume Value Entry
        self.drawVolumeEntry = ctk.CTkEntry(self, placeholder_text="...", width = 50)
        self.drawVolumeEntry.grid(row=3, column=1, padx=10, pady=10, sticky="ne")
        
        # Draw Volume Entry Button
        self.drawVolumeButton = ctk.CTkButton(self, text="Set", width = 50, command = self.UpdateDrawVolume)
        self.drawVolumeButton.grid(row=3, column=2, padx=10, pady=10, sticky="nw")
        
    def UpdateDrawVolume(self):
        try:
            entry = int(self.drawVolumeEntry.get())
        except ValueError:
            print("Please enter an integer between 0 and 200")
            return
        
        if(entry > 180 or entry < 0):
            print("Value must be between 0 and 200")
            return
        
        self.drawVolume = entry
        self.drawVolumeLabel.configure(text="Draw Volume: " + str(self.drawVolume))
        