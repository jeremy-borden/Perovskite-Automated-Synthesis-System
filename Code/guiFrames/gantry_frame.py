import customtkinter as ctk

BUTTON_SIZE = 40
BUTTON_PAD = 10

class GantryFrame(ctk.CTkFrame):          
    def __init__(self, master, gantry):
        super().__init__(master)
        
        self.gantry = gantry
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=1, padx=50, pady=50, sticky="")

        self.stepSize_mm = 1
        # Title Label
        self.titleLabel = ctk.CTkLabel(self, text="Gantry Control", justify="center", font=("Arial", 20, "bold"))
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20, sticky="we", columnspan = 5)
        
        # Gantry Step Size Slider
        self.stepSizeSlider = ctk.CTkSlider(self, from_=1, to=10, number_of_steps=9, orientation="vertical", command = self.updateStepSize)
        self.stepSizeSlider.grid(row=2, column=0, padx=20, pady=0, sticky="ns", rowspan=3)
        self.stepSizeSlider.set(1)
        
        # Gantry Step Size Label
        self.stepSizeLabel = ctk.CTkLabel(self, text="Step Size: " + str(int(self.stepSize_mm)) + " mm")
        self.stepSizeLabel.grid(row=5, column=0, padx=10, pady=0, sticky="nw", columnspan = 3)
        
        # Gantry Position Label
        self.positionLabel = ctk.CTkLabel(self, text="X: " + str(int(0)) + " mm \t Y: " + str(int(0)) + " mm\t Z: " + str(int(0)) + " mm")
        self.positionLabel.grid(row=5, column=4, padx=10, pady=0, sticky="ne", columnspan = 2)
        
        # Gantry Axis Control Buttons Subframe
        self.axisControlFrame = ctk.CTkFrame(self)
        self.axisControlFrame.grid(row=2, column=3, padx=20, pady=20, sticky="nsew", columnspan = 3, rowspan = 3)
        
        # X Axis Buttons
        self.xPlusButton = ctk.CTkButton(self.axisControlFrame, text="X+", width = BUTTON_SIZE, height = BUTTON_SIZE)
        self.xPlusButton.grid(row=3, column=3, padx=BUTTON_PAD, pady=BUTTON_PAD, sticky="")
        
        self.xMinusButton = ctk.CTkButton(self.axisControlFrame, text="X-", width = BUTTON_SIZE, height = BUTTON_SIZE)
        self.xMinusButton.grid(row=3, column=1, padx=BUTTON_PAD, pady=BUTTON_PAD, sticky="")
        
        # Y Axis Buttons
        self.yPlusButton = ctk.CTkButton(self.axisControlFrame, text="Y+", width = BUTTON_SIZE, height = BUTTON_SIZE)
        self.yPlusButton.grid(row=2, column=2, padx=BUTTON_PAD, pady=BUTTON_PAD, sticky="")
        
        self.yMinusButton = ctk.CTkButton(self.axisControlFrame, text="Y-", width = BUTTON_SIZE, height = BUTTON_SIZE)
        self.yMinusButton.grid(row=4, column=2, padx=BUTTON_PAD, pady=BUTTON_PAD, sticky="")
        
        # Z Axis Buttons
        self.zPlusButton = ctk.CTkButton(self.axisControlFrame, text="Z+", width = BUTTON_SIZE, height = BUTTON_SIZE)
        self.zPlusButton.grid(row=2, column=4, padx=BUTTON_PAD, pady=BUTTON_PAD, sticky="")
        
        self.zMinusButton = ctk.CTkButton(self.axisControlFrame, text="Z-", width = BUTTON_SIZE, height = BUTTON_SIZE)
        self.zMinusButton.grid(row=4, column=4, padx=BUTTON_PAD, pady=BUTTON_PAD, sticky="")
        
        # Command Entry Box
        self.commandEntry = ctk.CTkEntry(self, placeholder_text="Enter Command", width = 200)
        self.commandEntry.grid(row=6, column=0, padx=20, pady=20, sticky="", columnspan = 4)
        
        # Send Command Button
        self.sendCommandButton = ctk.CTkButton(self, text="Send Command", command = self.sendCommand)
        self.sendCommandButton.grid(row=6, column=4, padx=20, pady=20, sticky="")
        
        # Home Button
        self.homeButton = ctk.CTkButton(self, text="Connect", width = BUTTON_SIZE, height = BUTTON_SIZE, command = self.connectToController)
        self.homeButton.grid(row=7, column=0, padx=BUTTON_PAD, pady=BUTTON_PAD, sticky="")
        
        # Quick Stop Button
        self.quickStopButton = ctk.CTkButton(self, text="Stop", width = BUTTON_SIZE, height = BUTTON_SIZE, command=self.quickStop)
        self.quickStopButton.grid(row=7, column=1, padx=BUTTON_PAD, pady=BUTTON_PAD, sticky="")
        
    def updateStepSize(self, value):
        self.stepSizeLabel.configure(text="Step Size: " + str(int(value)) + " mm")
        
    def sendCommand(self):
        command = str(self.commandEntry.get())
        print(command)
        self.gantry.sendGCode(command)
        #self.commandEntry.delete(0, "end") # clear entry box
    
    def connectToController(self):
        self.gantry.connect()
        
    def quickStop(self):
        self.gantry.sendGCode("M410")