import customtkinter as ctk


class ProcedureFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.configure(border_color="#1f6aa5", border_width=2)
        self.grid(row=0, column=0, padx=5, pady=5, sticky="")

        # Title
        self.title_label = ctk.CTkLabel(self, text="Procedure Overview", justify="center", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=1, padx=20, pady=20, sticky="n")
        
        # progress
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.start_button = ctk.CTkButton(self.progress_frame, text=">")
        self.start_button.grid(row=0, column=0, rowspan = 2, padx=20, pady=20, sticky="nsew")
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, justify="left", text="Procedure Progress: " + str(int(50)) + "%")
        self.progress_label.grid(row=0, column=1, padx=20, pady=20, sticky="sw")
        
        self.progressbar = ctk.CTkProgressBar(self.progress_frame, orientation="horizontal", )
        self.progressbar.grid(row=1, column=1, padx=20, pady=20, sticky="nw")
        self.progressbar.set(0.5)
        
        #procedure loading
        self.procedure_frame = ctk.CTkFrame(self)
        self.procedure_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        
        self.open_button = ctk.CTkButton(self.procedure_frame, text="Open Procedure")
        self.open_button.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        
        # procedure console
        self.console_frame = ctk.CTkFrame(self)
        self.console_frame.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        
        self.console = ctk.CTkTextbox(master=self.console_frame, width=200, height=200, corner_radius=0, state = "disabled")
        self.console.grid(row=0, column=0, sticky="nsew")
     
        
    def WriteToConsole(self, text):
        self.console.configure(state="normal")
        self.console.insert("0.0", text + "\n")
        self.console.configure(state="disabled")
        

        
        
        
