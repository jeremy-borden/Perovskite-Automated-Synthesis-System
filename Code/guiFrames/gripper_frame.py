from turtle import width
import customtkinter as ctk

class GripperFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.servo1Angle = 0
        self.servo2Angle = 0
        
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=1, padx=50, pady=50, sticky="nsew")
        # Title Label
        self.titleLabel = ctk.CTkLabel(self, text="Gripper Control", justify="center", font=("Arial", 20, "bold"))
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20, sticky="nwe", columnspan = 2)

        # Servo 1 Label
        self.angle1Label = ctk.CTkLabel(self, text="Servo 1 Angle: " + str(int(0)))
        self.angle1Label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        # Servo 1 Value Entry
        self.angle1Entry = ctk.CTkEntry(self, placeholder_text="...", width = 50)
        self.angle1Entry.grid(row=2, column=1, padx=10, pady=10, sticky="ne")
        
        # 1 Entry Button
        self.angle1Button = ctk.CTkButton(self, text="Set", width = 50, command = self.UpdateAngle1)
        self.angle1Button.grid(row=2, column=2, padx=10, pady=10, sticky="ne")
        
        # Servo 2 Label
        self.angle2Label = ctk.CTkLabel(self, text="Servo 2 Angle: " + str(int(0)))
        self.angle2Label.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        
        # Servo 2 Value Entry
        self.angle2Entry = ctk.CTkEntry(self, placeholder_text="...", width = 50)
        self.angle2Entry.grid(row=3, column=1, padx=10, pady=10, sticky="ne")
        
        # Servo 2 Entry Button
        self.angle2Button = ctk.CTkButton(self, text="Set", width = 50, command = self.UpdateAngle2)
        self.angle2Button.grid(row=3, column=2, padx=10, pady=10, sticky="ne")
    
    def UpdateAngle1(self):
        try:
            entry = int(self.angle1Entry.get())
        except ValueError:
            print("Please enter an integer between 0 and 180")
            return
        
        if(entry > 180 or entry < 0):
            print("Angle must be between 0 and 180")
            return
        
        self.servo1Angle = entry
        self.angle1Label.configure(text="Servo 1 Angle: " + str(self.servo1Angle))
        
        
    def UpdateAngle2(self):
        try:
            entry = int(self.angle2Entry.get())
        except ValueError:
            print("Please enter an integer between 0 and 180")
            return
        
        if(entry > 180 or entry < 0):
            print("Angle must be between 0 and 180")
            return
        self.servo2Angle = entry
        self.angle2Label.configure(text="Servo 2 Angle: " + str(self.servo2Angle))
