from turtle import width
import customtkinter as ctk

class GripperFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.servo_1_angle = 0
        self.servo_2_angle = 0
        
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=1, padx=50, pady=50, sticky="nsew")
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Gripper Control", justify="center", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="nwe", columnspan = 2)

        # Servo 1 Label
        self.angle_1_label = ctk.CTkLabel(self, text="Servo 1 Angle: " + str(int(0)))
        self.angle_1_label.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

        # Servo 1 Value Entry
        self.angle_1_entry = ctk.CTkEntry(self, placeholder_text="...", width = 50)
        self.angle_1_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ne")
        
        # 1 Entry Button
        self.angle_1_button = ctk.CTkButton(self, text="Set", width = 50, command = self.UpdateAngle1)
        self.angle_1_button.grid(row=2, column=2, padx=10, pady=10, sticky="ne")
        
        # Servo 2 Label
        self.angle_2_label = ctk.CTkLabel(self, text="Servo 2 Angle: " + str(int(0)))
        self.angle_2_label.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        
        # Servo 2 Value Entry
        self.angle_2_entry = ctk.CTkEntry(self, placeholder_text="...", width = 50)
        self.angle_2_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ne")
        
        # Servo 2 Entry Button
        self.angle_2_button = ctk.CTkButton(self, text="Set", width = 50, command = self.UpdateAngle2)
        self.angle_2_button.grid(row=3, column=2, padx=10, pady=10, sticky="ne")
    
    def UpdateAngle1(self):
        try:
            entry = int(self.angle_1_entry.get())
        except ValueError:
            print("Please enter an integer between 0 and 180")
            return
        
        if(entry > 180 or entry < 0):
            print("Angle must be between 0 and 180")
            return
        
        self.servo_1_angle = entry
        self.angle_1_label.configure(text="Servo 1 Angle: " + str(self.servo_1_angle))
        
        
    def UpdateAngle2(self):
        try:
            entry = int(self.angle_2_entry.get())
        except ValueError:
            print("Please enter an integer between 0 and 180")
            return
        
        if(entry > 180 or entry < 0):
            print("Angle must be between 0 and 180")
            return
        self.servo_2_angle = entry
        self.angle_2_label.configure(text="Servo 2 Angle: " + str(self.servo_2_angle))
        
