import customtkinter as ctk
from src.drivers.ml_driver import main as run_ml_model  # ✅ Direct call, no subprocess

class MLModelFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.title_label = ctk.CTkLabel(
            self, text="Run Machine Learning Model", font=("Arial", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(
            self, text="Status: Waiting", font=("Arial", 14), wraplength=400
        )
        self.status_label.grid(row=1, column=0, padx=10, pady=10)

        self.run_button = ctk.CTkButton(
            self, text="Run ML Pipeline", command=self.run_model
        )
        self.run_button.grid(row=2, column=0, padx=10, pady=10)

    def run_model(self):
        self.status_label.configure(text="Status: Running ML Model...")
        try:
            run_ml_model()  # 💡 This calls your entire ML script
            self.status_label.configure(text="Status: Completed. Output saved.")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
