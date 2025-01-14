import customtkinter as ctk
import logging

from pyparsing import col


class ConsoleFrame(ctk.CTkFrame):
    """ GUI Frame to display the console log """
    
    def __init__(self, master, logger: logging.Logger):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2)
        
        self.logger = logger
        console_handler = ConsoleLogHandler(self)
        console_handler.setFormatter(logging.Formatter('%(levelname)s\t%(asctime)s: %(message)s'))
        logger.addHandler(console_handler)
        
        # title label
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Console",
            justify="left",
            anchor="w",
            font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
        
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

    def write_to_console(self, text: str):
        """ Write a message to the console

        ### Args:
            text (str): message to be logged in console
        """
        self.console.configure(state="normal")
        self.console.insert("end", text + "\n")
        self.console.configure(state="disabled")
        self.console.see("end")

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
        self.console.write_to_console(self.format(record))