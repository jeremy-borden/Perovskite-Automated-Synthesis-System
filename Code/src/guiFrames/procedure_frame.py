import customtkinter as ctk
from procedure_handeler import ProcedureHandeler


class ProcedureFrame(ctk.CTkFrame):
    """GUI Frame to display and control the procedure."""

    def __init__(self, master, procedure_handeler: ProcedureHandeler):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2)

        self.procedure_handeler = procedure_handeler

        # title label
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Procedure Overview",
            justify="center",
            anchor="w",
            font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=20,
                              pady=20, sticky="nswe", columnspan=3)

        # start button
        self.start_button = ctk.CTkButton(
            master=self,
            text="Start",
            width=100,
            height=50,
            command=self.start_procedure)
        self.start_button.grid(row=1, column=0, padx=20, pady=20)

        # pause button
        self.pause_button = ctk.CTkButton(
            master=self,
            text="Pause",
            width=100,
            height=50,
            command=self.toggle_pause)
        self.pause_button.grid(row=1, column=1, padx=20, pady=20)

        # stop button
        self.stop_button = ctk.CTkButton(
            master=self,
            text="Stop",
            width=100,
            height=50,
            command=self._stop_procedure)
        self.stop_button.grid(row=1, column=2, padx=20, pady=20)

        self.update()

    def update(self):
        """ Update the frame """

        if not self.procedure_handeler.started.is_set():
            self.start_button.configure(state="normal")
            self.pause_button.configure(text="Pause")
            self.pause_button.configure(state="disabled")
            self.stop_button.configure(state="disabled")
        else:
            self.start_button.configure(state="disabled")
            self.pause_button.configure(state="normal")
            self.stop_button.configure(state="normal")

            if self.procedure_handeler.running.is_set():
                self.pause_button.configure(text="Pause")
            else:
                self.pause_button.configure(text="Resume")

        self.after(250, self.update)

    def start_procedure(self):
        """ Callback to begin the procedure."""
        if not self.procedure_handeler.started.is_set():
            self.procedure_handeler.begin()

    def toggle_pause(self):
        """ Toggle the pause state of the procedure  """
        if self.procedure_handeler.running.is_set():
            self.procedure_handeler.pause()
        else:
            self.procedure_handeler.resume()

        # disable button after pressing to prevent double press
        self.pause_button.configure(state="disabled")

    def _stop_procedure(self):

        self.procedure_handeler.stop()


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")

    app.mainloop()
