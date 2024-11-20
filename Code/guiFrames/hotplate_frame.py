import customtkinter as ctk

class HotplateFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.targetTempC = 0;
       
       
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=1, padx=50, pady=50, sticky="we")

        # Title Label
        self.titleLabel = ctk.CTkLabel(self, text="Hotplate Control", justify="center", font=("Arial", 20, "bold"))
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20, sticky="we", columnspan = 5)

        # Hotplate Temperature Label
        self.temperatureLabel = ctk.CTkLabel(self, text="Current Hotplate Temperature: " + str(int(0)) + " °C")
        self.temperatureLabel.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        
        # Hotplate Target Temperature Label
        # mock Label
        self.angle_1_label = ctk.CTkLabel(self, text="Bake Temperature: 150 °C")
        self.angle_1_label.grid(row=4, column=0, padx=10, pady=10, sticky="nw")

        # mock Value Entry
        self.angle_1_entry = ctk.CTkEntry(self, placeholder_text="...", width = 50)
        self.angle_1_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ne")
        
        # mock Button
        self.angle_1_button = ctk.CTkButton(self, text="Set", width = 50)
        self.angle_1_button.grid(row=4, column=2, padx=10, pady=10, sticky="ne")
         # mock Label
        self.angle_1_label = ctk.CTkLabel(self, text="Time To Bake: 180 Seconds")
        self.angle_1_label.grid(row=5, column=0, padx=10, pady=10, sticky="nw")

        # mock Value Entry
        self.angle_1_entry = ctk.CTkEntry(self, placeholder_text="...", width = 50)
        self.angle_1_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ne")
        
        # mock Button
        self.angle_1_button = ctk.CTkButton(self, text="Set", width = 50)
        self.angle_1_button.grid(row=5, column=2, padx=10, pady=10, sticky="ne")
        
        
        
        
    def UpdateTargetTemperature(self, value):
        self.temperatureLabel.configure(text="Target Hotplate Temperature: " + str(int(value)) + " °C")
        