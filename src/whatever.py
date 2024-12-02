import customtkinter as ctk
import abc

LABEL_WIDTH = 150

class ProcedureFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=450, height=500)
        self.step_frames = []
        
        self.titleLabel = ctk.CTkLabel(self, text="Procedure", justify="left", font=("Arial", 14, "bold")).grid(row=0, column=0)
        
        self.btn_frame = ctk.CTkFrame(self, height=100, border_color="#1f6aa5", border_width=2)
        self.btn_frame.grid(row=1, column=0, sticky = "nwe", padx=10, pady=10)
        
        self.add_step_button = ctk.CTkButton(self.btn_frame, text="Add Step", width = 20, height = 20, command=self.onAddStep)
        self.add_step_button.grid(row=1, column=0, sticky = "nw", padx=10, pady=10)
        
        self.step_dropdown = ctk.CTkOptionMenu(self.btn_frame, width = 50, height = 20, values=["Heat", "Spin", "Apply", "Mix"])
        self.step_dropdown.grid(row=1, column=1, sticky = "nw", padx=10, pady=10)
        
        self.delete_step_button = ctk.CTkButton(self.btn_frame, text="Delete Step", width = 20, height = 20, command=self.onRemoveStep)
        self.delete_step_button.grid(row=1, column=2, sticky = "nw", padx=10, pady=10)
        
        self.export_button = ctk.CTkButton(self.btn_frame, text="Export", width = 20, height = 20, command=self.exportProcedure)
        self.export_button.grid(row=1, column=3, sticky = "nw", padx=10, pady=10)
        
    def get_steps(self):
        steps = []
        for step in self.step_frames:
            steps.append(step.get_values())
        return steps
        
    def exportProcedure(self):
        steps = self.get_steps()
        print(steps)
        
            
            
    def onAddStep(self):
        step_label = self.step_dropdown.get()
        
        match step_label:
            case "Heat":
                step = HeatStep(self)
            case "Spin":
                step = SpinStep(self)
            case "Apply":
                step = ApplyStep(self)
            case "Mix":
                step = MixStep(self)
            case _:
                step = None
        
        if (step != None):
            step.grid(row=len(self.step_frames)+2, column=0, sticky = "nw", padx=10, pady=10)
            self.step_frames.append(step)
        
    def onRemoveStep(self):
        if (len(self.step_frames) == 0): return
        
        self.step_frames.pop().destroy()
        
class StepManager():
    def __init__(self):
        self.steps = {}
      
    
    def decodeStep(self, step_dict):
        step_type = step_dict["step_type"]
        
        match step_type:
            case "heat":
                temperature = step_dict["temperature"]
                duration = step_dict["duration"]
                
            case "spin":
                step = SpinStep(self.frame)
            case "apply":
                step = ApplyStep(self.frame)
            case "mix":
                step = MixStep(self.frame)
            case _:
                step = None

        
class StepFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, border_color="#1f6aa5", border_width=2, width=400, height=100)
        self.bind("<Button-1>", command = self.onFocusIn)
  
        pad = 5
        self.titleLabel = ctk.CTkLabel(self, text=title, justify="left", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky = "nw", padx=pad, pady=pad)
    
    def onFocusIn(self, event):
        print(f"Focus")
        
    @abc.abstractmethod
    def get_values(self):
        pass

class EntryLabel(ctk.CTkFrame):
    def __init__(self, master, label_text):
        super().__init__(master)
        pad = 5

        self.entry_label = ctk.CTkLabel(self, text=label_text, justify="left", width=LABEL_WIDTH, anchor="w")
        self.entry_label.grid(row=0, column=0, sticky="nw", padx=pad, pady=pad)
        self.entry = ctk.CTkEntry(self, width=100, placeholder_text="...")
        self.entry.grid(row=0, column=1, sticky="nw", padx=pad, pady=pad)
        
    def get_value(self):
        return self.entry.get()
    
    def set_value(self, value): 
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, value)

class DropdownLabel(ctk.CTkFrame):
    def __init__(self, master, label_text, options):
        super().__init__(master)
        pad = 5
        
        self.dropdown_label = ctk.CTkLabel(self, text=label_text, justify="left", width=LABEL_WIDTH, anchor="w")
        self.dropdown_label.grid(row=0, column=0, sticky="nw", padx=pad, pady=pad)
        
        self.dropdown = ctk.CTkOptionMenu(self, values=options, width = 100)
        self.dropdown.grid(row=0, column=1, sticky="nsw", padx=pad, pady=pad)
    
    def get_value(self):
        return self.dropdown.get()
    
    def set_value(self, value):
        self.dropdown.set(value)
    

    
    
class HeatStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "HEAT STEP")
        
        pad = 5
        
        self.value_dict = {"step_type": "heat",
                           "temperature": 0, 
                           "duration": 0
                           }
        
        self.bake_temperature = EntryLabel(self, "Bake Temperature: ")
        self.bake_temperature.grid(row=1, column=0, sticky = "nw", padx=pad, pady=pad)
        
        self.bake_time = EntryLabel(self, "Bake Time: ")
        self.bake_time.grid(row=2, column=0, sticky = "nw", padx=pad, pady=pad)
        
    def update_values(self):
        self.value_dict["temperature"] = self.bake_temperature.get_value()
        self.value_dict["duration"] = self.bake_time.get_value()
    
    def get_values(self):
        self.update_values()
        return self.value_dict
        
   
class SpinStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "SPIN STEP")

        pad = 5
        
        self.value_dict = { "step_type": "spin",
                            "speed": 0, 
                            "duration": 0}
        
        self.spin_speed = EntryLabel(self, "Spin Speed: ")
        self.spin_speed.grid(row=1, column=0, sticky = "nw", padx=pad, pady=pad)
        
        self.spin_time = EntryLabel(self, "Spin Time: ")
        self.spin_time.grid(row=2, column=0, sticky = "nw", padx=pad, pady=pad)
    
    def update_values(self):
        self.value_dict["speed"] = self.spin_speed.get_value()
        self.value_dict["duration"] = self.spin_time.get_value()
    
    def get_values(self):
        self.update_values()
        return self.value_dict

class ApplyStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "APPLY STEP")
        options = ["Vial 1", "Vial 2", "Vial 3"]
        pad = 5
        
        self.value_dict = { "step_type": "apply",
                            "source_vial": 0,
                            "duration": 0,
                            "amount": 0}

        self.source_vial = DropdownLabel(self, "Source Vial: ", options)
       
        self.source_vial.grid(row=1, column=0, sticky = "nw", padx=pad, pady=pad)
        
        self.application_duration = EntryLabel(self, "Application duration: ")
        self.application_duration.grid(row=2, column=0, sticky = "nw", padx=pad, pady=pad)
        
        self.amount = EntryLabel(self, "Amount: ")
        self.amount.grid(row=3, column=0, sticky = "nw", padx=pad, pady=pad)
   
    def update_values(self):
        self.value_dict["source_vial"] = self.source_vial.get_value()
        self.value_dict["duration"] = self.application_duration.get_value()
        self.value_dict["amount"] = self.amount.get_value()
    
    def get_values(self):
        self.update_values()
        return self.value_dict
    
class MixStep(StepFrame):
    def __init__(self, master):
        super().__init__(master, "MIX STEP")
        self.options = ["Vial 1", "Vial 2", "Vial 3", "Vial 4", "Vial 5"]
        
        pad = 5
        self.vial_frames = []
        
     
        self.value_dict = { "step_type": "mix",
                            "destination_vial": 0,
                            "sources": [], 
                            "source_amounts": []
                           }
        
        
        
        self.destination_vial = DropdownLabel(self, "Destination Vial: ", self.options)
        self.destination_vial.grid(row=1, column=0, sticky = "nw", padx=pad, pady=pad)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.grid(row=2, column=0, sticky = "nw", padx=pad, pady=pad)
        
        self.newVialButton = ctk.CTkButton(self.btn_frame, text="New Vial", width = 20, height = 20, command=self.newVial).grid(row=2, column=0, sticky = "nw")
        self.delete_vial_button = ctk.CTkButton(self.btn_frame, text="Delete Vial", width = 20, height = 20, command=self.deleteLastVial).grid(row=2, column=1, sticky = "nw")
        
        self.newVial()
        self.newVial()
        
    def newVial(self):
        if(len(self.vial_frames) == len(self.options)): return
        
        frame = ctk.CTkFrame(self, width=400, height=100, border_color="#1f6aa5", border_width=2)
        frame.grid(row=3 + len(self.vial_frames), column=0, sticky = "nw", padx=2, pady=2)
        
        dropdown = DropdownLabel(frame, "Source Vial: ", ["Vial 1", "Vial 2", "Vial 3"])
        dropdown.grid(row=0, column=0, sticky = "nw")
        entry = EntryLabel(frame, "Amount: ")
        entry.grid(row=1, column=0, sticky = "nw")
        
        
        
        self.vial_frames.append(frame)
        return
    
    def deleteLastVial(self):
        if(len(self.vial_frames) == 2): return
        
        self.vial_frames.pop().destroy()

        
    def update_values(self):
        self.value_dict["destination_vial"] = self.destination_vial.get_value()
        source_list = []
        source_amount_list = []
        for frame in self.vial_frames:
            for child in frame.winfo_children():
                if isinstance(child, DropdownLabel):
                    source_list.append(child.get_value())
                elif isinstance(child, EntryLabel):
                    source_amount_list.append(child.get_value())
                    
        self.value_dict["sources"] = source_list
        self.value_dict["source_amounts"] = source_amount_list
        
    def get_values(self):
        self.update_values()
        return self.value_dict
    



if __name__ == "__main__":
    app = ctk.CTk()
    step_manager = StepManager()
    procedure_frame = ProcedureFrame(app).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
 
    app.mainloop()