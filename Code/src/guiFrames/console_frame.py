import customtkinter as ctk
import logging
from queue import Queue


class ConsoleFrame(ctk.CTkFrame):
    """ GUI Frame to display the console log """
    
    def __init__(self, master):
        super().__init__(master=master,border_color="#1f6aa5",border_width=2, height=200)
        
        self.logger = logging.getLogger("Main Logger")
        self.log_queue = Queue()
        self.console_handler = ConsoleLogHandler(self)
        self.console_handler.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s: %(message)s'))
        self.logger.addHandler(self.console_handler)

        # title label
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Console",
            justify="left",
            anchor="w",
            font=("Arial", 20, "bold"))
        self.title_label.grid(
            row=0, column=0, 
            padx=20, pady=10, 
            sticky="nw")
        
        # logging level selector
        self.log_level = ctk.CTkOptionMenu(
            master=self,
            values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            width=100,
            command=self.update_logging_level)
        self.log_level.grid(row=0, column=1, padx=20, pady=10, sticky="ne")
        
        # console
        self.console = ctk.CTkTextbox(
            master=self,
            width=400,
            height=200,
            corner_radius=0,
            state="disabled")
        self.console.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky="nsew")
        
        self.console.tag_config("DEBUG", foreground="#8df564")
        self.console.tag_config("WARNING", foreground="#e4f089")
        self.console.tag_config("ERROR", foreground="red")
        
        self._update()
    
    def destroy(self):
        """ Override the destroy method to perform cleanup tasks """
        self.logger.removeHandler(self.console_handler)
        super().destroy()
        
    def _update(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.write_to_console(msg)
            self.log_queue.task_done()
            self.console.see("end")
            
            
      
        
        self.after(50, self._update)

    def write_to_console(self, text: str):
        """ Write a message to the console

        ### Args:
            text (str): message to be logged in console
        """
        
        prefix = text.split(" ")[0]
        
        self.console.configure(state="normal")
        self.console.insert("end", text + "\n", prefix)
        self.console.configure(state="disabled")


    def update_logging_level(self, level: str):
        """ Update the logging level

        ### Args:
            level (str): logging level to set
        """
        self.logger.setLevel(level)
        self.logger.debug(f"Logging level set to {level}")

    
class ConsoleLogHandler(logging.StreamHandler):
    """ Custom log handler to write log messages to the console frame """
    def __init__(self, console):
        super().__init__()
        self.console = console

    def emit(self, record):
        self.console.log_queue.put(self.format(record))
    