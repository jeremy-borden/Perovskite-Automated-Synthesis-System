import customtkinter as ctk
from tkinter import filedialog
from inspect import signature
import logging

# get current directory so we can import from outside guiFrames folder
import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(path)
from drivers.procedure_file_driver import ProcedureFile

class ProcedureBuilderFrame(ctk.CTkFrame):
    def __init__(self, master, moves, procedure_handler):
        super().__init__(master=master,border_color="#1f6aa5",border_width=2,
                         width=600)
        self.logger=logging.getLogger("Main Logger")
        self.step_list = []
        self.variation_step_list = []
        self.selected_step = None
        self.moves = moves
        self.procedure_handler = procedure_handler
        
        # step holding frame
        self.step_frame = ctk.CTkScrollableFrame(
            master=self,
            width=600,height=500)
        self.step_frame.grid(
            row=0, column=0, rowspan=9,
            padx=5,pady=5)
        
        self.step_frame.bind("<Button-1>", self._deselect_step)
        
        # step select dropdown
        self.step_dropdown = ctk.CTkOptionMenu(master=self,
            width=120, height=50, values=list(self.moves.keys()))
        self.step_dropdown.grid(row=0, column=1,
            padx=5, pady=5,
            sticky="nwe")
   
        
        # add step button
        self.add_step_button = ctk.CTkButton(
            master=self,
            text="Add Step",
            width=120,height=50,
            command=self._add_step)
        self.add_step_button.grid(
            row=1, column=1,
            padx=5,pady=5, sticky="nwe")
        
        # insert step button
        self.insert_step_button = ctk.CTkButton(
            master=self,
            text="Insert Step",
            width=120,height=50,
            command=self._insert_step)
        self.insert_step_button.grid(
            row=2, column=1,
            padx=5, pady=5,
            sticky="nwe")
        
        # delete step button
        self.delete_step_button = ctk.CTkButton(
            master=self,
            text="Delete Step",
            width=120,height=50,
            command=self._delete_step)
        self.delete_step_button.grid(
            row=3, column=1,
            padx=5, pady=5,
            sticky="nwe")
        
        # vary step button
        self.vary_step_button = ctk.CTkButton(
            master=self,
            text="Vary Step",
            width=120,height=50,
            command=self._add_variation)
        self.vary_step_button.grid(
            row=4, column=1,
            padx=5, pady=5,
            sticky="nwe")
        
        # export steps button
        self.export_button = ctk.CTkButton(
            master=self,
            text="Export\nProcedure",
            width=120, height=50,
            command=self._export)
        self.export_button.grid(
            row=5, column=1,
            padx=5, pady=5, 
            sticky="nwe")
        
        # import steps button
        self.import_button = ctk.CTkButton(
            master=self,
            text="Import\nProcedure",
            width=120, height=50,
            command=self._import)
        self.import_button.grid(
            row=6, column=1,
            padx=5, pady=5, 
            sticky="nwe")
        
        # quick run button
        self.quick_run_button = ctk.CTkButton(
            master=self,
            text="Quick Run",
            width=120, height=50,
            command=self._quick_run)
        self.quick_run_button.grid(
            row=7, column=1,
            padx=5, pady=5,
            sticky="nwe")

        # Loop Count
        self.loop_count = LabelEntry(self, "Loop Count: ", int)
        self.loop_count.entry.insert(0,"1")
        self.loop_count.grid(
            row=8, column=1,
            padx=5, pady=5,
            sticky="nwe")
        
    def _bind_step_widgets(self, step_frame):
        """Recursively bind click events to all widgets in step frame"""
        
        step_frame.bind('<Button-1>', lambda e: self._select_step(e,))
        
        for child in step_frame.winfo_children():
            # Skip binding for checkboxes since it disables them
            if isinstance(child, ctk.CTkCheckBox):
                continue
            
            child.bind('<Button-1>', lambda e: self._select_step(e,))
            if len(child.winfo_children()) > 0:
                self._bind_step_widgets(child)
    
    
    def _deselect_step(self,event):
        """ Reset the border color of selected step if user clicks off"""
        if self.selected_step is not None:
            self.selected_step.configure(border_color="#1f6aa5")
        self.selected_step = None
    
    def _select_step(self, event):
        """ change the border color of selected step if user clicks on it"""
        if self.selected_step is not None:
            self.selected_step.configure(border_color="#1f6aa5")
        
        # user likely clicked on something within the frame, so we have to find the OG
        # parent frame so we can change its color
        widget = event.widget
        while widget != self.step_frame:
            if isinstance(widget, StepFrame):
                self.selected_step = widget
                break
            widget = widget.master
        
        widget.configure(border_color="#edf556")
        
    def _add_step(self):
        """ Add a step to the steplist"""
        # get the function we are making a step for
        function = self.moves[self.step_dropdown.get()]
        new_step = StepFrame(self.step_frame, function)
        #bind click events to window and its children
        self._bind_step_widgets(new_step)
        
        # update lists and gui
        self.step_list.append(new_step)
        self.variation_step_list.append(None)
        self._update()

    def _insert_step(self):
        """ Insert step before currently selected one"""
        # prevent inserting after nothing
        if self.selected_step is None:
            return

        
        # get the function we are making a step for
        function = self.moves[self.step_dropdown.get()]
        new_step = StepFrame(self.step_frame, function)
        #bind click events to window and its children
        self._bind_step_widgets(new_step)
        
        #find index to insert step at
        
        # selected frame could be a variation so we need to check for that
        if(self.selected_step in self.step_list):
            index = self.step_list.index(self.selected_step)
        else:
            index = self.variation_step_list.index(self.selected_step)
        
        # update lists and gui
        self.step_list.insert(index, new_step)
        self.variation_step_list.insert(index, None)
        self._update()
        
    def _add_variation(self):
        # prevent adding varaint to nothing
        if self.selected_step is None:
            return
        # prevent adding variant to variant
        if self.selected_step in self.variation_step_list: 
            return
        # prevent adding additional variants
        index = self.step_list.index(self.selected_step)
        if self.variation_step_list[index] is not None:
            return
        
        
        function = self.selected_step.function
        variation_step = StepFrame(self.step_frame, function)
   
        self.variation_step_list.insert(index, variation_step)
        
        self._bind_step_widgets(variation_step)
        self._update()
        
    def _delete_step(self):
        """ Delete the currently selected step"""
        if self.selected_step is None:
            return
        
        # if selected step is a normal step, delete it and any variations
        if self.selected_step in self.step_list:
            step = self.selected_step
            
            index = self.step_list.index(step)
            v_step = self.variation_step_list.pop(index)
            self.step_list.remove(step)
            
            if(v_step is not None):
                v_step.destroy()
            step.destroy()
        # otherwise if selected step is varaint, jsut delete that
        elif self.selected_step in self.variation_step_list:
            index = self.variation_step_list.index(self.selected_step)
            self.variation_step_list.pop(index).destroy()
        
        self.selected_step = None
        self._update()
        
    def _quick_run(self):
        """Quickly run the procedure without exporting."""
        
        procedure = self._get_procedure()
        self.procedure_handler.set_procedure(procedure["Procedure"])
        self.procedure_handler.begin()
        self.logger.info("Quick Run started!")
        
    def _get_procedure(self):
        """Returns a runnable procedure list of moves

        Returns:
            _type_: _description_
        """
        procedure = {"Procedure": []}
        try:
            loop_count = self.loop_count.get_entry()
        except ValueError:
            self.logger.error("Loop count must be > 0")
            return
        
        for loop in range(loop_count):
            for step, variation_step in zip(self.step_list, self.variation_step_list):
                partial_step = [step.function.__name__] # get step name
                if variation_step is not None: # if step should vary throughout procedures
                    for initial_value, final_value in zip(step.get_entries(), variation_step.get_entries()):
                        # skip interpolation and use the first value when entry isnt a number
                        if (type(initial_value) is not float) and (type(initial_value) is not int):
                            partial_step.append(initial_value)
                        else:
                            partial_step.append(initial_value + (final_value-initial_value)*(loop)/(loop_count-1)) #interpolate between first and final value
                else:
                    for entry in step.get_entries():
                        partial_step.append(entry)  
                procedure["Procedure"].append(partial_step)
        
        return procedure
        
    def _export(self):
        procedure = self._get_procedure()
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=("Yaml files","*.yml*"),
            initialdir="src/procedures/",title="Save As",
            filetypes=(("Yaml files","*.yml*"),))
        if file_path != "":
            ProcedureFile().Save(path=file_path, procedure=procedure)
            self.logger.info("Procedure Succesfully Exported!")
            
        
    def _import(self):
        file_path = filedialog.askopenfilename(
        initialdir="src/procedures/",
        title="Open Procedure File",
        filetypes=(("Yaml files", "*.yml*"), ("All files", "*.*")))
        if not file_path:
            return
        
        
        
        try:
            procedure = ProcedureFile().Open(file_path)
            for step, vstep in zip(self.step_list, self.variation_step_list):
                if step is not None:
                    step.destroy()
                if vstep is not None:
                    vstep.destroy()
                
            self.step_list.clear()
            self.variation_step_list.clear()
            self.selected_step = None

            for step in procedure["Procedure"]:
                func_name = step[0]
                if func_name not in self.moves:
                    self.logger.error(f"Function '{func_name}' not found in moves.")
                    return
                
                function = self.moves[func_name]
                new_step = StepFrame(self.step_frame, function)

                # Populate step entries with the arguments from the procedure
                for entry, value in zip(new_step.entry_list, step[1:]):
                    entry.entry.insert(0, str(value))

                # Bind click events and update lists
                self._bind_step_widgets(new_step)
                self.step_list.append(new_step)
                self.variation_step_list.append(None)
        except Exception as e:
            self.logger.error(f"Ran into error {e} while importing")
        self._update()
        
    def _update(self):
        """ Update the step frame"""
        for i, step in enumerate(self.step_list):
            step.grid(
                row=i, column=0,
                padx=5,pady=5,
                sticky="nw")
            
        for i, step in enumerate(self.variation_step_list):
            if step is None:
                continue
            
            step.grid(
                row=i, column=1,
                padx=5,pady=5,
                sticky="nw")
    
    def update_super_moves(self):
        # search through persistant folder
        # for each file ending in _supermove, add it to the moves list
        # when this move is run, it should run the moves specified in the file
        
        pass
# -------- STEPS --------
class StepFrame(ctk.CTkFrame):
    def __init__(self, master, function):
        super().__init__(
            master=master,border_color="#1f6aa5",border_width=2,
            width=400,)
        self.master = master
        self.function = function
        self.entry_list = []
        
      
        title = self.snake_to_title(function.__name__)
        
        # title
        self.title_label = ctk.CTkLabel(
            master = self,text=title,
            width=250,
            justify="center",anchor="w",
            font=("Arial", 16, "bold"))
        self.title_label.grid(
            row=0, column=0,
            padx=5, pady=5,
            sticky="nw")

        # main step frame
        self.step_frame = ctk.CTkFrame(
            master=self,
            width=200, height=20)
        self.step_frame.grid(
            row=1, column=0, columnspan=2,
            padx=5, pady=5,
            sticky="nswe")
        
        self.generate_frame()
        
    def snake_to_title(self, snake_str):
        return ' '.join(word.capitalize() for word in snake_str.split('_'))
    
    def get_entries(self):
        entries = []
        
        for entry in self.entry_list:
            entries.append(entry.get_entry())
        
        return entries
        
        
    def generate_frame(self):
        func_sig = signature(self.function)
        num_args = len(func_sig.parameters)
        
        for index, (name, param) in enumerate(func_sig.parameters.items()):
            
            name = self.snake_to_title(name) # reformat the funciton arg
            entry = LabelEntry(self.step_frame, f"{name}: ", param.annotation)
            entry.grid(row=index, column=0,
                       padx=5, pady=5)
             
            self.entry_list.append(entry)
            
class LabelEntry(ctk.CTkFrame):
    def __init__(self, master, label: str, entry_type: type = str):
        super().__init__(master=master,width=200)
        self.entry_type = entry_type
        
        # entry label
        self.label = ctk.CTkLabel(
            master=self,text=label,
            width=80,
            anchor="w")
        self.label.grid(
            row=0, column=0,
            padx=5, pady=5,sticky="nwe")
        
        # create input (checkbox or entry) based on entry type
        if entry_type is bool:
            self.entry = ctk.CTkCheckBox(
                master=self, text="", 
                width=50,)
        else:
            self.entry = ctk.CTkEntry(
                master=self,
                width=100)
            
        self.entry.grid(
            row=0, column=1,
            padx=5, pady=5,sticky="ne")
        
        # assign proper validation function based on entry type
        if entry_type is int:
            self.entry.configure(validate="key",
                                 validatecommand=(self.register(self._validate_int), '%P'))
        elif entry_type is float:
            self.entry.configure(validate="key",
                                 validatecommand=(self.register(self._validate_float), '%P'))

    def get_entry(self,):
        """ Return the entry formatted as its entry type. 
        Raises a ValueError if the entry is empty"""
        if self.entry.get().strip() == "":
            raise ValueError

        return self.entry_type(self.entry.get().strip())
    
    def _validate_float(self, P):
        """ Validate that only floats are entered. """
        if P.isdigit() or P == "" or (P.count('.') == 1 and P.replace('.', '').replace("-", "").isdigit()) or ((P.count('-') == 1 and (P.replace('-', '').replace(".", "").isdigit() or P.replace('-', '') == ''))):
            return True
        else:
            return False
        
    def _validate_int(self, P):
        """ Validate that only ints are entered. """
        if P.isdigit() or P == "" or ((P.count('-') == 1 and (P.replace('-', '').isdigit() or P.replace('-', '') == ''))):
            return True
        else:
            return False
        
# testing 
class peepee():
    def __init__(self):
        
        self.moves = {
            "move": self.move,
            "move_another": self.move_another,
            "what_the": self.what_the
        }
        
    def move(self, this_is_an_int: int, this_is_a_str: str, this_is_a_float: float):
        pass
    
    def move_another(self, inbt: int, flot: float, str: str):
        pass # gas
    
    def what_the(self):
        pass
    
    def get_dick(self):
        return self.moves
        
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x1000")
    app.configure()
    pee = peepee()
    moves = pee.get_dick()
    f = ProcedureBuilderFrame(app, moves, None)
    f.grid(
        row=0, column=0,
        padx=5, pady=5,
        sticky="nw"
    )
    app.mainloop()
    
    
    

