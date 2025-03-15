import customtkinter as ctk
from tkinter import filedialog
import abc
from time import sleep

# get current directory so we can import from outside guiFrames folder
import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(path)
from src.drivers.procedure_file_driver import ProcedureFile

class ProcedureBuilder(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2,
            width=600)
        
        self.step_list = []
        self.selected_step = None
        
        self.steps = {
            "Wait":WaitStep,
            "Heat":HeatStep,
            "Move":MoveStep,
            "Move Fluid": MoveFluidStep,
            "Spin": SpinStep}
        
        
        self.step_frame = ctk.CTkScrollableFrame(
            master=self,
            width=600,
            height=600)
        self.step_frame.grid(
            row=0, column=0, rowspan=7,
            padx=5,pady=5)
        
        self.step_frame.bind("<Button-1>", self._deselect_step)
        
        # step select dropdown
        self.step_dropdown = ctk.CTkOptionMenu(master=self,
            width=80, height=50, values=list(self.steps.keys()))
        self.step_dropdown.grid(row=0, column=1,
            padx=5, pady=5,
            sticky="nw")
        
        # add step button
        self.add_step_button = ctk.CTkButton(
            master=self,
            text="Add Step",
            width=80,height=50,
            command=self._add_step)
        self.add_step_button.grid(
            row=1, column=1,
            padx=5,pady=5, sticky="nw")
        
        # insert step button
        self.insert_step_button = ctk.CTkButton(
            master=self,
            text="Insert Step",
            width=80,height=50,
            command=self._insert_step)
        self.insert_step_button.grid(
            row=2, column=1,
            padx=5, pady=5,
            sticky="nw")
        
        # delete step button
        self.delete_step_button = ctk.CTkButton(
            master=self,
            text="Delete Step",
            width=80,height=50,
            command=self._delete_step)
        self.delete_step_button.grid(
            row=3, column=1,
            padx=5, pady=5,
            sticky="nw")
        
        # vary step button
        self.vary_step_button = ctk.CTkButton(
            master=self,
            text="Vary Step",
            width=80,height=50,
            command=self._add_variation)
        self.vary_step_button.grid(
            row=4, column=1,
            padx=5, pady=5,
            sticky="nw")
        
        # export steps button
        self.export_button = ctk.CTkButton(
            master=self,
            text="Export\nProcedure",
            width=80, height=50,
            command=self._export)
        self.export_button.grid(
            row=5, column=1,
            padx=5, pady=5,
            sticky="nw")
  
        self.loop_count = LabelEntry(self, "Loop Count: ")
        self.loop_count.grid(
            row=6, column=1,
            padx=5, pady=5,
            sticky="nw")
        
        self.a_step = []
    
    
    def _deselect_step(self,event):
        if self.selected_step is not None:
            self.selected_step.configure(border_color="#1f6aa5")
        self.selected_step = None
    
    def _select_step(self, event):
        
        if self.selected_step is not None:
            self.selected_step.configure(border_color="#1f6aa5")
        
        widget = event.widget
        while widget != self.step_frame:
            if isinstance(widget, StepFrame):
                self.selected_step = widget
                break
            widget = widget.master
        
        widget.configure(border_color="#edf556")
        
    def _bind_step_widgets(self, step_frame):
        """Recursively bind click events to all widgets in step frame"""
        step_frame.bind('<Button-1>', lambda e: self._select_step(e,))
        
        for child in step_frame.winfo_children():
            child.bind('<Button-1>', lambda e: self._select_step(e,))
            if len(child.winfo_children()) > 0:
                self._bind_step_widgets(child)
        
    def _add_step(self):
        """ Add a new step, defaults to Wait"""
        new_step = self.steps[self.step_dropdown.get()](self.step_frame)
        self._bind_step_widgets(new_step)
        self.step_list.append(new_step)
        self.a_step.append(None)
        self._update()
    
    def _delete_step(self):
        if self.selected_step is None:
            return
        
        if self.selected_step in self.step_list:
            step = self.selected_step
            
            index = self.step_list.index(step)
            v_step = self.a_step.pop(index)
            self.step_list.remove(step)
            
            if(v_step is not None):
                v_step.destroy()
            step.destroy()
            
        elif self.selected_step in self.a_step:
            index = self.a_step.index(self.selected_step)
            self.a_step.pop(index).destroy()
        
        
        self.selected_step = None
        self._update()
        
        
    def _insert_step(self):
        if self.selected_step is None:
            return

        index = self.step_list.index(self.selected_step)
        new_step = self.steps[self.step_dropdown.get()](self.step_frame)
        
        self._bind_step_widgets(new_step)
        self.step_list.insert(index, new_step)
        self.a_step.insert(index, None)
        self._update()
        
    def _add_variation(self):
        if self.selected_step is None:
            return
        
        if self.selected_step in self.a_step:
            return
        
        index = self.step_list.index(self.selected_step)
        if self.a_step[index] is not None:
            return
        
        step_type = type(self.selected_step)
        new_step = step_type(self.step_frame)
        
   
        self.a_step.insert(index, new_step)
        self._bind_step_widgets(new_step)
        
        self._update()
        
    def _export(self):
        procedure = {"Procedure": []}
        loops = self.loop_count.get_entry()
        for loop_num in range(loops):
            for steps, v_steps in zip(self.step_list, self.a_step):
                if v_steps is not None: # if step should vary throughout procedures
                    step = steps.get_steps()[0] # get step name
                    for e1, e2 in zip(steps.get_steps()[1:], v_steps.get_steps()[1:]):
                        
                        step.append(e1 + (e2-e1)*(loop_num)/(loops-1)) #interpolate between first and final value
                        
                else:
                    for step in steps.get_steps():
                        procedure["Procedure"].append(step)
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=("Yaml files","*.yml*"),
            initialdir="src/procedures/",title="Save As",
            filetypes=(("Yaml files","*.yml*"),))
        if file_path != "":
            ProcedureFile().Save(path=file_path, procedure=procedure)
            
        
        
    def _update(self):
        """ Update the step frame"""
        for i, step in enumerate(self.step_list):
            step.grid(
                row=i, column=0,
                padx=5,pady=5,
                sticky="nw")
            
        for i, step in enumerate(self.a_step):
            if step is None:
                continue
            
            step.grid(
                row=i, column=1,
                padx=5,pady=5,
                sticky="nw")
        
# -------- STEPS --------
class StepFrame(ctk.CTkFrame):
    def __init__(self, master, title: str = "Empty Step"):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2,
            width=400,)
        self.master = master
        self.index=0
        
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
            sticky="nw")

        self.step_frame = ctk.CTkFrame(master=self,
                                       width=350)
        self.step_frame.grid(
            row=1, column=0, columnspan=2,
            padx=5, pady=5,
            sticky="nswe")
    
    @abc.abstractmethod
    def get_steps(self):
        """Method to be implemented by subclasses"""
        pass
        
class WaitStep(StepFrame):
    def __init__(self, master):
        super().__init__(master=master,title="Wait")
        
        self.wait_time = LabelEntry(self.step_frame, "Wait time:")
        self.wait_time.grid(row=0, column=0, padx=5, pady=5)
        
        
    def get_steps(self):
        wait_time: int = self.wait_time.get_entry()
        return ["wait", wait_time]
        
class HeatStep(StepFrame):
    def __init__(self, master):
        super().__init__(
                master=master,
                title="Heat")
        
        # heat time
        self.wait_time = LabelEntry(self.step_frame, "Heat Time: ")
        self.wait_time.grid(row=0, column=0, padx=5,pady=5)
        # heat temp
        self.heat_temperature = LabelEntry(self.step_frame, "Heat Temperature: ")
        self.heat_temperature.grid(row=1, column=0, padx=5,pady=5)
        
        
        self.wait_for_temp_checkbox = ctk.CTkCheckBox(master=self.step_frame,
            width=20,
            height=20,
            text="Wait for temperature")
        self.wait_for_temp_checkbox.grid(row=0, column=1, padx=5,pady=5)

        
    def get_steps(self):
        target_temperature = int(self.heat_temperature.get_entry())
        move = ["set_temp", target_temperature]
        return move

class WaitForTemp(StepFrame):
    def __init__(self, master):
        super().__init__(master, "Wait For Temperature")
        self.target_temperature = LabelEntry(self.step_frame, "")

class MoveStep(StepFrame):
    def __init__(self, master):
        super().__init__(
                master=master,
                title="Move")
        
        self.x_coord = LabelEntry(self.step_frame, "X: ")
        self.x_coord.grid(row=0, column=0, padx=5,pady=5)

        self.y_coord = LabelEntry(self.step_frame, "Y: ")
        self.y_coord.grid(row=1, column=0, padx=5,pady=5)
        
        self.z_coord = LabelEntry(self.step_frame, "Z: ")
        self.z_coord.grid(row=2, column=0, padx=5,pady=5)
        
        
class MoveFluidStep(StepFrame):
    def __init__(self, master):
        super().__init__(
                master=master,
                title="Mix")
        
        self.source_vial = LabelEntry(self.step_frame, "Source Vial: ")
        self.source_vial.grid(row=0, column=0, padx=5, pady=5)
        
        self.fluid_amount_ul = LabelEntry(self.step_frame, "Fluid Amount (ul): ")
        self.fluid_amount_ul.grid(row=1, column=0, padx=5, pady=5)
        
        self.destination = LabelEntry(self.step_frame, "Destination Vial: ")
        self.destination.grid(row=2, column=0, padx=5, pady=5)
        
        self.mix_checkbox = ctk.CTkCheckBox(master=self.step_frame,
            width=20,
            height=20,
            text="Mix after deposit")
        self.mix_checkbox.grid(row=0, column=1, padx=5, pady=5)
        
        
    def get_steps(self):
        # vialcarousel move to self.source_vial
        # gantry goto above self.source_vial
        #gantry lower
        #pippete extract self.fluid_amount_ul
        #gantry raise
        
        # gantry goto above self.destination_vial
        #gantry lower
        # vialcarousel move to self.destination_vial
        #pippete deposit
        #gantry raise
        
        #if mix
        #spin vc if possible or suck in and out with tip
        
        
        return super().get_steps()
    
class SpinStep(StepFrame):
    def __init__(self, master):
        super().__init__(
                master=master,
                title="Spin")
        
        self.spin_rpm = LabelEntry(self.step_frame, "Spin RPM: ")
        self.spin_rpm.grid(row=0, column=0, padx=5,pady=5)
        
        self.spin_duration = LabelEntry(self.step_frame, "Spin Duration (s): ")
        self.spin_duration.grid(row=1, column=0, padx=5, pady=5)
        
    

# spectrometer measure
# save picture
# Move Slide

class LabelEntry(ctk.CTkFrame):
    def __init__(self, master, label: str):
        super().__init__(
            master=master,width=200,)
        
        self.label = ctk.CTkLabel(
            master=self,text=label,
            width=100,
            anchor="w")
        self.label.grid(
            row=0, column=0,
            padx=5, pady=5,sticky="nw")
        self.entry = ctk.CTkEntry(
            master=self,placeholder_text="...",
            width=100)
        self.entry.grid(
            row=0, column=1,
            padx=5, pady=5,sticky="nw")
    def get_entry(self):
        return self.entry.get()
      
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x1000")
    app.configure()
    f = ProcedureBuilder(app)
    f.grid(
        row=0, column=0,
        padx=5, pady=5,
        sticky="nw"
    )
    app.mainloop()