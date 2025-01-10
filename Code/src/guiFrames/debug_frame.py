from venv import logger
import customtkinter as ctk
import logging


class DebugFrame(ctk.CTkFrame):
    def __init__(self, master, logger: logging.Logger):
        super().__init__(master)
        self.logger = logger

        self._setup_gui()

    def _setup_gui(self):
        # procedure console
        self.console_frame = ctk.CTkFrame(self)
        self.console_frame.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        self.console = ctk.CTkTextbox(
                                      master=self.console_frame, width=200,
                                      height=200, corner_radius=0, state="disabled")
        self.console.grid(row=0, column=0, sticky="nsew")

    # create a loop usign after to update the console every 200 ms
    def update_console(self):
        self.console.configure(state="normal")
        self.console.insert("0.0", "test\n")
        self.console.configure(state="disabled")

        self.after(200, self.update_console)


if __name__ == "__main__":
    app = ctk.CTk()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    DebugFrame(app, logger).grid(row=0, column=0,
                                 padx=10, pady=10, sticky="nsew")
    app.mainloop()
