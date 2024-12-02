from cProfile import label
from calendar import c
from re import S
from tkinter import E
from turtle import st
import customtkinter as ctk
from numpy import pad

LABEL_WIDTH = 100

class ProcedureFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=450, height=800)
        
        self.titleLabel = ctk.CTkLabel(self, text="Procedure", justify="left", font=("Arial", 14, "bold")).grid(row=0, column=0)
        
        self.btn_frame = ctk.CTkFrame(self, height=100, border_color="#1f6aa5", border_width=2)
        self.btn_frame.grid(row=1, column=0, sticky = "nwe", padx=10, pady=10)
        self.add_step_button = ctk.CTkButton(self.btn_frame, text="Add Step", width = 20, height = 20)
        self.add_step_button.grid(row=1, column=0, sticky = "nw", padx=10, pady=10)

        
        hf = HeatStep(self).grid(row=2, column=0, sticky = "nw", padx=10, pady=10)
        sf = SpinStep(self).grid(row=3, column=0, sticky = "nw", padx=10, pady=10)
        af = ApplyStep(self).grid(row=4, column=0, sticky = "nw", padx=10, pady=10)
        mf = MixStep(self).grid(row=5, column=0, sticky = "nw", padx=10, pady=10)
        
    
        
class StepFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, border_color="#1f6aa5", border_width=2, width=400, height=100)
        self.bind("<Button-1>", command = self.onFocusIn)
  
        pad = 5
        self.titleLabel = ctk.CTkLabel(self, text=title, justify="left", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky = "nw", padx=pad, pady=pad)
        
    def createValueEntryLabel(self, label_text):
        frame = ctk.CTkFrame(self)
        self.value_entry_label = ctk.CTkLabel(frame, text=label_text, justify="left", width=LABEL_WIDTH, anchor="w").grid(row=0, column=0, sticky="nw")
        self.value_entry = ctk.CTkEntry(frame, width=50, placeholder_text="...").grid(row=0, column=1, sticky="nw")
        return frame
    
    def createDropdownLabel(self, label_text, options):
        frame = ctk.CTkFrame(self)
        self.dropdown_label = ctk.CTkLabel(frame, text=label_text, justify="left", width=LABEL_WIDTH, anchor="w").grid(row=0, column=0, sticky="nw")
        self.dropdown = ctk.CTkOptionMenu(frame, values=options, width = 50, height = 20).grid(row=0, column=1, sticky="nw")
        return frame
    
    def onFocusIn(self, event):
        print(f"Focus")
        

class EntryLabel(ctk.CTkFrame):
    def __init__(self, master, label_text):
        super().__init__(master)
        pad = 5

        self.entry_label = ctk.CTkLabel(self, text=label_text, justify="left", width=LABEL_WIDTH, anchor="w")
        self.entry_label.grid(row=0, column=0, sticky="nw", padx=pad, pady=pad)
        self.entry = ctk.CTkEntry(self, width=50, placeholder_text="...")
        self.entry.grid(row=0, column=1, sticky="nw", padx=pad, pady=pad)
        
    def get_value(self):
        return self.entry.get()
    
    def set_value(self, value): 
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, value)

class DropdownLabel(ctk.CTkFrame):
    def __init__(self, master, label_text, options):
        super().__init__(master, border_color="#1f6aa5", border_width=2, width=400, height=100)
        self.dropdown_label = ctk.CTkLabel(self, text=label_text, justify="left", width=LABEL_WIDTH, anchor="w")
        self.dropdown_label.grid(row=0, column=0, sticky="nw")
        self.dropdown = ctk.CTkOptionMenu(self,values=options, width = 50, height = 20)
        self.dropdown.grid(row=0, column=1, sticky="nw")
    
    def get_value(self):
        return self.dropdown.get()
    
    def set_value(self, value):
        self.dropdown.set(value)
    

    
    
class HeatStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "HEAT STEP")
        self.value_dict = {"bake_temperature": None, "bake_time": None}
        
        self.bake_temperature = EntryLabel(self, "Bake Temperature: ")
        self.bake_temperature.grid(row=1, column=0, sticky = "nw", padx=10, pady=10)
        
        self.bake_time = EntryLabel(self, "Bake Time: ")
        self.bake_time.grid(row=2, column=0, sticky = "nw", padx=10, pady=10)
    
    def get_values(self):
        self.value_dict["bake_temperature"] = self.bake_temperature.entry.get()
        self.value_dict["bake_time"] = self.bake_time.entry.get()
        return self.value_dict
        
   

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
    
        
        
      
    
        
        
class StepManager():
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