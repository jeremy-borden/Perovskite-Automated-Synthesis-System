import customtkinter as ctk

class GripperFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=1, padx=50, pady=50, sticky="we")

        # Title Label
        self.titleLabel = ctk.CTkLabel(self, text="Gripper Control", justify="center", font=("Arial", 20, "bold"))
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20, sticky="we", columnspan = 5)

        # Gripper Finger Servo 1 Label
        self.temperatureLabel = ctk.CTkLabel(self, text="Servo 1 Angle: " + str(int(0)))
        self.temperatureLabel.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        
        # Gripper Finger Servo 1 Slider
        
        
        
        # Gripper  Temperature Label
        self.temperatureLabel = ctk.CTkLabel(self, text="Target Hotplate Temperature: " + str(int(0)) + " °C")
        self.temperatureLabel.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        
        # Hotplate Temperature Slider
        self.temperatureSlider = ctk.CTkSlider(self, from_=0, to=300, number_of_steps=301, orientation="horizontal", command = self.UpdateTargetTemperature)
        self.temperatureSlider.grid(row=3, column=1, padx=10, pady=10, sticky="we")
        self.temperatureSlider.set(0)
        
    
        
# app = ctk.CTk()
# app.geometry("600x600")

# hotplateFrame = HotplateFrame(app)

# app.mainloop()