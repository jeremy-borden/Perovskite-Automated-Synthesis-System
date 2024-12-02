from calendar import c
from re import S
from turtle import st
import customtkinter as ctk
from numpy import pad

class ProcedureFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=400, height=400)
        
        self.titleLabel = ctk.CTkLabel(self, text="Procedure", justify="left", font=("Arial", 14, "bold")).grid(row=0, column=0)
        
        hf = HeatStep(self).grid(row=1, column=0, sticky = "nw", padx=10, pady=10)
        sf = SpinStep(self).grid(row=2, column=0, sticky = "nw", padx=10, pady=10)
        af = ApplyStep(self).grid(row=3, column=0, sticky = "nw", padx=10, pady=10)
        mf = MixStep(self).grid(row=4, column=0, sticky = "nw", padx=10, pady=10)
        
class StepFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, border_color="#1f6aa5", border_width=2, width=400, height=100)
        
        self.label_width = 200
        self.titleLabel = ctk.CTkLabel(self, text=title, justify="left", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky = "nw")
        
    def createValueEntryLabel(self, label_text):
        frame = ctk.CTkFrame(self)
        self.value_entry_label = ctk.CTkLabel(frame, text=label_text, justify="left", width=self.label_width, anchor="w").grid(row=0, column=0, sticky="nw")
        self.value_entry = ctk.CTkEntry(frame, width=50, placeholder_text="...").grid(row=0, column=1, sticky="nw")
        return frame
    
    def createDropdownLabel(self, label_text, options):
        frame = ctk.CTkFrame(self)
        self.dropdown_label = ctk.CTkLabel(frame, text=label_text, justify="left", width=self.label_width, anchor="w").grid(row=0, column=0, sticky="nw")
        self.dropdown = ctk.CTkOptionMenu(frame, values=options, width = 50, height = 20).grid(row=0, column=1, sticky="nw")
        return frame
    
    
    
    
class HeatStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "HEAT STEP")
        
        self.createValueEntryLabel("Bake Temperature: ").grid(row=1, column=0, sticky = "nw")
        self.createValueEntryLabel("Bake Time: ").grid(row=2, column=0, sticky = "nw")

class SpinStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "SPIN STEP")
        
        self.createValueEntryLabel("Spin Speed: ").grid(row=1, column=0, sticky = "nw")
        self.createValueEntryLabel("Spin Time: ").grid(row=2, column=0, sticky = "nw")

class ApplyStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "APPLY STEP")
        
        self.createDropdownLabel("Source Vial: ", ["1", "2", "3"]).grid(row=1, column=0, sticky = "nw")
        self.createValueEntryLabel("Application duration: ").grid(row=2, column=0, sticky = "nw")
        self.createValueEntryLabel("Application duration: ").grid(row=3, column=0, sticky = "nw")
        
    
        
class MixStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "MIX STEP")
        
        self.vial_list = []
        self.createDropdownLabel("Destination Vial: ", ["1", "2", "3"]).grid(row=1, column=0, sticky = "nw")

        self.newVialButton = ctk.CTkButton(self, text="New Vial", width = 20, height = 20, command=self.newVial).grid(row=2, column=0, sticky = "nw")
        self.delete_vial_button = ctk.CTkButton(self, text="Delete Vial", width = 20, height = 20, command=self.deleteLastVial).grid(row=2, column=1, sticky = "nw")
        self.newVial()
        
    def newVial(self):
        if(len(self.vial_list) == 3): return
        
        frame = ctk.CTkFrame(self, width=400, height=100, border_color="#1f6aa5", border_width=2)
        self.createDropdownLabel("Vial Number: ", ["1", "2", "3"]).grid(in_=frame, row=0, column=0, sticky = "nw")
        self.createValueEntryLabel("Amount: ").grid(in_ = frame, row=1, column=0, sticky = "nw")
        frame.grid(row=3 + len(self.vial_list), column=0, sticky = "nw", padx=2, pady=2)
        self.vial_list.append(frame)
        return
    
    def deleteLastVial(self):
        if(len(self.vial_list) == 1): return
        
        self.vial_list.pop().destroy()
    
        
        
      
    
        
        
class ProcedureHandeler():
    def __init__(self):
        self.steps = {}
        
    
    def addStep(self, step):
        self.steps.append(step)
        
    def removeStep(self, step, index):
        self.steps.pop(index)
        
    def insertStep(self, step, index):
        self.steps.insert(index, step)

if __name__ == "__main__":
    app = ctk.CTk()
    
    procedure_frame = ProcedureFrame(app).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
 
    app.mainloop()