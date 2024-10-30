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
        self.temperatureLabel = ctk.CTkLabel(self, text="Target Hotplate Temperature: " + str(int(0)) + " °C")
        self.temperatureLabel.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        
        # Hotplate Temperature Slider
        self.temperatureSlider = ctk.CTkSlider(self, width = 300, from_=0, to=300, number_of_steps=301, orientation="horizontal", command = self.UpdateTargetTemperature)
        self.temperatureSlider.grid(row=4, column=0, padx=10, pady=10, sticky="we")
        self.temperatureSlider.set(0)
        
    def UpdateTargetTemperature(self, value):
        self.temperatureLabel.configure(text="Target Hotplate Temperature: \t" + str(int(value)) + " °C")
        
# app = ctk.CTk()
# app.geometry("600x600")

# hotplateFrame = HotplateFrame(app)

# app.mainloop()