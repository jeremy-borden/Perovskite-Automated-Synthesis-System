import os
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

class MLModelFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Configure grid for resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Create internal frame for images
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Track image objects to avoid garbage collection
        self.image_refs = []

        # Load and display output graphs
        self.display_output_images()

    def display_output_images(self):
        image_filenames = [
            "Feature Importance.png",
            "Actual vs Predicted Bandgap.png",
            "Density Distribution of Residuals.png",
            "sq_limit_with_all_samples.png",
            "adjusted_efficiency_distribution.png"
        ]

        image_dir = "/home/ecd515/Desktop/PASS/src"  # Adjust if saved elsewhere

        for i, filename in enumerate(image_filenames):
            full_path = os.path.join(image_dir, filename)
            if os.path.exists(full_path):
                img = Image.open(full_path)
                img = img.resize((800, 400), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                label = ctk.CTkLabel(self.scrollable_frame, image=photo, text="")
                label.grid(row=i, column=0, padx=10, pady=10)
                self.image_refs.append(photo)
            else:
                label = ctk.CTkLabel(self.scrollable_frame, text=f"⚠️ {filename} not found")
                label.grid(row=i, column=0, padx=10, pady=10)
