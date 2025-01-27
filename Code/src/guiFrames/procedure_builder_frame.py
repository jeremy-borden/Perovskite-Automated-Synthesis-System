import customtkinter as ctk
import abc
from time import sleep

class ProcedureBuilder(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2,
            width=500)
        
        self.step_list = []
        self.selected_step = None
        
        self.steps = {"Wait":WaitStep,
                          "Heat":HeatStep,
                          "Move":MoveStep,
                          "Move Fluid": MoveFluidStep,}
        
        # TODO add button to save procedure
        self.step_frame = ctk.CTkScrollableFrame(
            master=self,
            width=500,
            height=600)
        self.step_frame.grid(
            row=0, column=0, rowspan=4,
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
            width=80,
            height=50,
            command=self._add_step)
        self.add_step_button.grid(
            row=1, column=1,
            padx=5,pady=5, sticky="nw")
        
        # insert step button
        self.insert_step_button = ctk.CTkButton(
            master=self,
            text="Insert Step",
            width=80,
            height=50,
            command=self.insert_step)
        self.insert_step_button.grid(
            row=2, column=1,
            padx=5, pady=5,
            sticky="nw")
        
        # delete step button
        self.delete_step_button = ctk.CTkButton(
            master=self,
            text="Delete Step",
            width=80,
            height=50,
            command=self.delete_step)
        self.delete_step_button.grid(
            row=3, column=1,
            padx=5, pady=5,
            sticky="nw")
        
        
    
    
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
                print(f"Selected frame: {widget}")

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
        self._update()
    
    def delete_step(self):
        if self.selected_step is None:
            return
        
        
        step = self.selected_step
        self.step_list.remove(step)
        
        
        self.selected_step = None
        self._update()
        step.destroy()
        
    def insert_step(self):
        if self.selected_step is None:
            return
        
        new_step = self.steps[self.step_dropdown.get()](self.step_frame)
        self._bind_step_widgets(new_step)
        index = self.step_list.index(self.selected_step)
        self.step_list.insert(index, new_step)
        self._update()
        
    def _update(self):
        """ Update the step frame"""
        for i, step in enumerate(self.step_list):
            step.grid(
                row=i, column=0,
                padx=5,pady=5,
                sticky="nw")
        
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
        super().__init__(
                master=master,
                title="Wait",
        )
        
        self.wait_time = LabelEntry(self.step_frame, "Wait time:")
        self.wait_time.grid(row=0, column=0, padx=5, pady=5)
        
        
    def get_steps(self):
        wait_time: int = self.wait_time_entry.get()
        d = {"function": "wait",
             "args": wait_time}
        
        return [d]
    
    
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
        
        s1 = {"function": "set_temp",
              "args": int(self.heat_temperature.get_entry())}

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
        self.destination_vial.grid(row=2, column=0, padx=5, pady=5)
        
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
    
class Spin(StepFrame):
    def __init__(self, master):
        super().__init__(
                master=master,
                title="Spin")
        
        self.spin_rpm = LabelEntry(self.step_frame, "Spin RPM: ")
        self.spin_rpm.grid(row=0, column=0, padx=5,pady=5)
        
        self.spin_duration = LabelEntry(self.step_frame, "Spin Duration (s): ")
        self.spin_duration.grid(row=0, column=0, padx=5, pady=5)
        
    

# spectrometer measure
# save picture
# Move Slide

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
            anchor="w"
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