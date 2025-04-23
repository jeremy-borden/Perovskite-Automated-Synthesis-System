import os
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import subprocess

class MLModelFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Run Model button
        self.run_button = ctk.CTkButton(self, text="Run ML Model", command=self.run_ml_model)
        self.run_button.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        # Canvas and scrollbar for images
        self.canvas = tk.Canvas(self)
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        # Internal scrollable frame
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.image_refs = []
        self.image_filenames = [
            "Feature Importance.png",
            "Actual vs Predicted Bandgap.png",
            "Density Distribution of Residuals.png",
            "sq_limit_with_all_samples.png",
            "adjusted_efficiency_distribution.png"
        ]
        self.image_dir = "/home/ecd515/Desktop/PASS/src"
        self.display_output_images()

    def display_output_images(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.image_refs.clear()

        for i, filename in enumerate(self.image_filenames):
            full_path = os.path.join(self.image_dir, filename)
            if os.path.exists(full_path):
                try:
                    img = Image.open(full_path)
                    img = img.resize((800, 400), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(img)
                    label = ctk.CTkLabel(self.scrollable_frame, image=photo, text="")
                    label.grid(row=i, column=0, padx=10, pady=10)
                    self.image_refs.append(photo)
                except Exception as e:
                    label = ctk.CTkLabel(self.scrollable_frame, text=f"⚠️ Error loading {filename}: {e}")
                    label.grid(row=i, column=0, padx=10, pady=10)
            else:
                label = ctk.CTkLabel(self.scrollable_frame, text=f"⚠️ {filename} not found")
                label.grid(row=i, column=0, padx=10, pady=10)

    def run_ml_model(self):
        script_path = "/home/ecd515/Desktop/PASS/src/drivers/ml_driver.py"
        try:
            subprocess.run(["python3", script_path], check=True)
            self.display_output_images()
        except subprocess.CalledProcessError as e:
            error_label = ctk.CTkLabel(self.scrollable_frame, text=f"❌ ML model failed: {e}")
            error_label.grid(row=len(self.image_filenames), column=0, padx=10, pady=10)
