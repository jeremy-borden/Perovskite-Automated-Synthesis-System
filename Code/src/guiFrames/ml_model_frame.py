import customtkinter as ctk
from drivers.ml_driver import main as run_ml_model  # Importing from ml_driver.py

class MLModelFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(border_color="#1f6aa5", border_width=2)

        title = ctk.CTkLabel(self, text="Machine Learning Model", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Idle", font=("Arial", 14), wraplength=400)
        self.status_label.pack(pady=10)

        self.run_button = ctk.CTkButton(self, text="Run ML Analysis", command=self.run_ml)
        self.run_button.pack(pady=10)

    def run_ml(self):
        self.status_label.configure(text="Status: Running...")
        try:
            run_ml_model()
            self.status_label.configure(text="Status: Completed. Results saved.")
        except Exception as e:
            self.status_label.configure(text=f"Status: Failed.\n{str(e)}")
