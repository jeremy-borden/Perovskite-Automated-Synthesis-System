import os
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
from drivers import ml_driver
import io
import sys

class MLModelFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.run_button = ctk.CTkButton(self, text="Run ML Model", command=self.run_ml_model)
        self.run_button.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.canvas = tk.Canvas(self)
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.image_refs = []
        self.image_filenames = [
            "Feature Importance.png",
            "Actual vs Predicted Bandgap.png",
            "Density Distribution of Residuals.png",
            "sq_limit_with_all_samples.png",
            "adjusted_efficiency_distribution.png"
        ]
        self.image_dir = os.path.join(os.path.dirname(__file__), "..", "persistant")

        self.output_text = ctk.CTkTextbox(self, width=880, height=180)
        self.output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.display_output_images()

    def display_output_images(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()

        for i, filename in enumerate(self.image_filenames):
            full_path = os.path.join(self.image_dir, filename)
            if os.path.exists(full_path):
                img = Image.open(full_path).resize((850, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label = ctk.CTkLabel(self.scrollable_frame, image=photo, text="")
                label.grid(row=i, column=0, padx=10, pady=10)
                self.image_refs.append(photo)
            else:
                label = ctk.CTkLabel(self.scrollable_frame, text=f"⚠️ {filename} not found")
                label.grid(row=i, column=0, padx=10, pady=10)

    def run_ml_model(self):
        self.output_text.delete("1.0", tk.END)
        buffer = io.StringIO()
        sys.stdout = buffer

        try:
            ml_driver.run_model()
            self.display_output_images()
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ ML model failed: {e}\n")

        sys.stdout = sys.__stdout__
        result = buffer.getvalue()
        filtered_lines = [line for line in result.splitlines() if "iter" not in line and "target" not in line]
        self.output_text.insert(tk.END, "\n".join(filtered_lines))
        buffer.close()
