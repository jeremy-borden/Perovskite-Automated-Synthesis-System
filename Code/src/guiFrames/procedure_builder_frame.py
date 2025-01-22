import customtkinter as ctk

class ProcedureBuilder(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2,
            width=500)
        
        self.step_list = []
        self.selected_step = None
        
      
        
        self.step_frame = ctk.CTkScrollableFrame(
            master=self,
            width=500,
            height=600)
        self.step_frame.grid(
            row=0, column=0,
            padx=5,pady=5)
        
        # add step button
        self.add_step_button = ctk.CTkButton(
            master=self,
            text="Add Step",
            width=50,
            height=50,
            command=self._add_step)
        self.add_step_button.grid(
            row=1, column=0,
            padx=5,pady=5)
        # insert step button
        self.insert_step_button = ctk.CTkButton(
            master=self,
            text="+",
            width=30,
            height=30,
            command=self.insert_step)
        self.insert_step_button.grid(
            row=1, column=1,
            padx=5, pady=5,
            sticky="ne")
        # delete step button
        self.delete_step_button = ctk.CTkButton(
            master=self,
            text="x",
            width=30,
            height=30,
            command=self.delete_step)
        self.delete_step_button.grid(
            row=1, column=2,
            padx=5, pady=5,
            sticky="ne")
    
    
    def _select_step(self, event):
        print(event)
        print("G")
        
    def _add_step(self):
        new_step = StepFrame(self.step_frame, self)
        new_step.bind('<Button-1>', self._select_step)
        self.step_list.append(new_step)
        self._update()
    
    def delete_step(self):
        step = self.step_list[self.selected_step]
        self.step_list.remove(step)
        step.destroy()
        self._update()
        
    def insert_step(self):
        new_step = StepFrame(self.step_frame, self)
        new_step.bind('<Button-1>', self._select_step)
        self.step_list.insert(self.selected_step, new_step)
        self._update()
        
    def _update(self):
        """ Update the step frame"""
        for i, step in enumerate(self.step_list):
            step.grid(
                row=i, column=0,
                padx=5,pady=5)
        
class StepFrame(ctk.CTkFrame):
    def __init__(self, master, title: str = "Empty Step"):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2,
            width=400)
        self.master = master
        
        self.step_dict = {
            "WAIT": WaitStep,
            "HEAT": HeatStep
        }
        
        # title
        self.title_label = ctk.CTkLabel(
            master = self,
            text=title,
            width=250,
            justify="center",
            anchor="w",
            font=("Arial", 20, "bold")
        )
        self.title_label.grid(
            row=0, column=0,
            padx=5, pady=5,
            sticky="nw"
        )
        
        # change step dropdown
        keys = list(self.step_dict.keys())
        self.step_dropdown = ctk.CTkOptionMenu(
            master=self,
            values=keys,
            command=self._change_step
        )  
        self.step_dropdown.grid(
            row=0, column=1,
            padx=5, pady=5,
            sticky="nw"
        )

        # by doing this, the wit step will be the default
        self._change_step("WAIT")


        
    def _change_step(self, value):
        self.step = self.step_dict[value](self)
        self.step.grid(
            row=1, column=0, columnspan=2,
            padx=5, pady=5,
            sticky="nswe"
        )
        
    def get_steps(self):
        """ Returns a list of one or more dicts formatted to be run by the procedure handler"""
        return self.step.get_steps()
    
        
        
class WaitStep(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
                master=master,
                width=350,
        )
        
        # wait time
        self.wait_time_label = ctk.CTkLabel(
            master=self,
            text="Wait time:"
            
        )
        self.wait_time_label.grid(
            row=0, column=0,
            padx=5, pady=5,
            sticky="nw"
        )
        
        self.wait_time_entry = ctk.CTkEntry(
            master=self,
            width=100, 
            placeholder_text="..."
        )
        self.wait_time_entry.grid(
            row=0, column=1,
            padx=5, pady=5,
            sticky="nw"
        )
        
    def get_steps(self):
        wait_time: int = self.wait_time_entry.get()
        d = {"function": "wait",
             "args": wait_time}
        
        return [d]
    
    
class HeatStep(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
                master=master,
                width=350,
        )
         
        # heat time
        self.wait_time = LabelEntry(self, "Heat Time: ")
        self.wait_time.grid(row=0, column=0, padx=5,pady=5)
        # heat temp
        self.heat_temperature = LabelEntry(self, "Heat Temperature: ")
        self.heat_temperature.grid(row=1, column=0, padx=5,pady=5)
        
        
        self.wait_for_temp_checkbox = ctk.CTkCheckBox(
            master=self,
            width=20,
            height=20,
            text="Wait for temperature"
        )
        self.wait_for_temp_checkbox.grid(row=0, column=1, padx=5,pady=5)
        
    def get_steps(self):
        
        s1 = {"function": "set_temp",
              "args": int(self.heat_temperature.get_entry())}
        
class LabelEntry(ctk.CTkFrame):
    def __init__(self, master, label: str):
        super().__init__(
            master=master,
            width=200,
        )
        
        self.label = ctk.CTkLabel(
            master=self,
            text=label,
            width=100,
        )
        self.label.grid(
            row=0, column=0,
            padx=5, pady=5,
            sticky="nw"
        )
        self.entry = ctk.CTkEntry(
            master=self,
            width=100, 
            placeholder_text="..."
        )
        self.entry.grid(
            row=0, column=1,
            padx=5, pady=5,
            sticky="nw"
        )
    def get_entry(self):
        return self.entry.get()
      
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x1000")
    
    f = ProcedureBuilder(app)
    f.grid(
        row=0, column=0,
        padx=5, pady=5,
        sticky="nw"
    )
    app.mainloop()