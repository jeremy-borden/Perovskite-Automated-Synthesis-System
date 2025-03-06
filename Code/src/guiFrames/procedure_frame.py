from sre_parse import State
import customtkinter as ctk
from procedure_handler import ProcedureHandler
from tkinter import filedialog

import sys
import os

# get current directory so we can import from outside guiFrames folder
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(path)
from src.drivers.procedure_file_driver import ProcedureFile

class ProcedureFrame(ctk.CTkFrame):
    """GUI Frame to display and control the procedure."""

    def __init__(self, master, procedure_handler: ProcedureHandler):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2)
        self.procedure_handler = procedure_handler
        self.killed = False

        # title label
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Procedure Overview",
            justify="center",
            anchor="w",
            font=("Arial", 20, "bold"))
        self.title_label.grid(
            row=0, column=0, columnspan=4,
            padx=20, pady=20, sticky="nswe",)

        # start button
        self.start_button = ctk.CTkButton(
            master=self,text="Start",
            width=80,height=50,
            command=self._start_procedure)
        self.start_button.grid(
            row=1, column=0,
            padx=5, pady=20)
        # pause button
        self.pause_button = ctk.CTkButton(
            master=self,text="Pause",
            width=80,height=50,
            command=self._toggle_pause)
        self.pause_button.grid(
            row=1, column=1,
            padx=5, pady=20)
        # stop button
        self.stop_button = ctk.CTkButton(
            master=self,text="Stop",
            width=80,height=50,
            command=self._stop_procedure)
        self.stop_button.grid(
            row=1, column=2,
            padx=5, pady=20)
        # kill button
        self.kill_button = ctk.CTkButton(
            master=self, text="Kill",
            fg_color="#a10e22",hover_color="#45060f",
            width=80,height=50,
            command=self._kill_procedure)
        self.kill_button.grid(
            row=1, column=3,
            padx=5, pady=20)
        
        # progress
        self.time_label = ctk.CTkLabel(
            master=self,text="",)
        self.time_label.grid(
            row=2,column=0,
            padx=5, pady=5)
        self.progress_bar = ctk.CTkProgressBar(
            master=self,mode="determinate",
            width=200)
        self.progress_bar.grid(
            row=2, column=1, columnspan=2,
            padx=5, pady=5, sticky="nw")
        self.progress_label = ctk.CTkLabel(
            master=self,text="0%")
        self.progress_label.grid(
            row=2, column=3,
            padx=5, pady=5, sticky="nw")
        
        #number of procedures
        self.num_procedures_label = ctk.CTkLabel(
            master=self, text="Number of Procedures:")
        self.num_procedures_label.grid(
            row=3, column=0,
            padx=5, pady=5, sticky="w")
        
        self.num_procedures_entry = ctk.CTkEntry(
            master=self, width=80,
            validate="key", validatecommand=(self.register(self._validate_num_procedures), '%P'))
        self.num_procedures_entry.grid(
            row=3, column=1,
            padx=5, pady=5, sticky="w")
        
       #import procedurs
        self.current_procedure = "default_procedure.yml"
        self.import_procedure_button = ctk.CTkButton(
            master=self, text="Import",
            width=80, height=30,
            command=self._import_procedure)
        self.import_procedure_button.grid(
            row=4,column=0,
            padx=5, pady=5)
        self.current_procedure_label = ctk.CTkLabel(
            master=self, text=f"Current Procedure: {self.current_procedure}")
        self.current_procedure_label.grid(
            row=4,column=1,columnspan=3,
            padx=5,pady=5)

        
        self._update()
        
    def _validate_num_procedures(self, P):
        """ Validate that only numbers are entered. """
        if P.isdigit() or P == "":
            return True
        else:
            return False
        
    def _update(self):
        """ Update the frame """

        if not self.procedure_handler.started.is_set():
            if self.start_button.cget("state") != "normal":
                self.start_button.configure(state="normal") 
            self.pause_button.configure(text="Pause")
            self.pause_button.configure(state="disabled")
            self.stop_button.configure(state="disabled")
            self.import_procedure_button.configure(state="normal")
        else:
            self.start_button.configure(state="disabled")
            
            if self.pause_button.cget("state") != "normal":
                self.pause_button.configure(state="normal")
            if self.stop_button.cget("state") != "normal":
                self.stop_button.configure(state="normal")
            self.import_procedure_button.configure(state="disabled")
            
        if self.killed:
            self.start_button.configure(state="disabled")
            self.pause_button.configure(state="disabled")
            self.stop_button.configure(state="disabled")
            self.kill_button.configure(state="disabled")
            self.import_procedure_button.configure(state="disabled")
                

        self.time_label.configure(text=self.procedure_handler.get_time_elapsed())
        self.progress_bar.set(self.procedure_handler.get_progress())
        
        self.progress_label.configure(text=f"{int(self.procedure_handler.get_progress()*100)}%")
        
        self.after(500, self._update)

    def _start_procedure(self):
        """ Callback to begin the procedure."""

        loop_entry = self.num_procedures_entry.get()
        if loop_entry is None or int(loop_entry) == 0:
            return
        
        if self.procedure_handler.started.is_set():
            return
        
        self.procedure_handler.begin(int(loop_entry))

    def _toggle_pause(self):
        """ Toggle the pause state of the procedure  """
        if self.procedure_handler.running.is_set():
            self.procedure_handler.pause()
            self.pause_button.configure(text="Resume")
        else:
            self.procedure_handler.resume()
            self.pause_button.configure(text="Pause")

        # disable button after pressing to prevent double press
        self.pause_button.configure(state="disabled")

    def _stop_procedure(self):
        self.procedure_handler.stop()
        
    def _kill_procedure(self):
        self.killed=True
        self.procedure_handler.kill()
        
    def _import_procedure(self):
        file_path = filedialog.askopenfilename(
            initialdir="src/procedures/",title="Select a File",
            filetypes=(("Yaml files","*.yml*"),))
        print(file_path)
        if file_path != "":
            file = ProcedureFile().Open(path=file_path)
            procedure = file["Procedure"]
            self.procedure_handler.set_procedure(procedure)
            procedure_name = file_path.split("/")[-1]
            self.current_procedure=procedure_name
            self.current_procedure_label.configure(text=f"Current Procedure: {self.current_procedure}")
            
