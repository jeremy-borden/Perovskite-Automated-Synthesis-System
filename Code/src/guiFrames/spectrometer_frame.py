import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from predictor import predict_bandgap_and_efficiency 
# from ml_optimizers import genetic_algorithm, get_top_5_recipes, plot_feature_importance, plot_sq_limit_overlay
import sys
import os
import numpy as np
import subprocess


# get current directory so we can import from outside guiFrames folder
pp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)

from src.drivers.spectrometer_driver import Spectrometer

class SpectrometerFrame(ctk.CTkFrame):
    def __init__(self, master, spectrometer: Spectrometer):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2
        )

        self.spectrometer = spectrometer

        self.title_label = ctk.CTkLabel(
            master=self,
            text="Spectrometer Live Data",
            justify="left",
            anchor="w",
            font=("Arial", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.status_label = ctk.CTkLabel(
            master=self,
            text="Waiting for Data...",
            justify="left",
            anchor="w",
            font=("Arial", 14),
            wraplength=400
        )
        self.status_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # # --- INPUT CONTROLS ---
        # self.ink_var = ctk.StringVar(value="mix")
        # self.additive_var = ctk.StringVar(value="Br")
        # self.comp_type_var = ctk.StringVar(value="10% Br")

        # self.concentration_entry = ctk.CTkEntry(self, placeholder_text="Ink Conc (e.g. 1.1)")
        # self.concentration_entry.grid(row=3, column=0, padx=5, pady=2)

        # self.comp_value_entry = ctk.CTkEntry(self, placeholder_text="Comp Value (e.g. 10)")
        # self.comp_value_entry.grid(row=4, column=0, padx=5, pady=2)

        # self.ink_dropdown = ctk.CTkOptionMenu(self, variable=self.ink_var, values=["FASnI3", "MASnI3", "mix"])
        # self.ink_dropdown.grid(row=5, column=0, padx=5, pady=2)

        # self.additive_dropdown = ctk.CTkOptionMenu(self, variable=self.additive_var, values=["Br", "Zn", "MA", "EASCN", "4-MePEABr", "0"])
        # self.additive_dropdown.grid(row=6, column=0, padx=5, pady=2)

        # self.comp_dropdown = ctk.CTkOptionMenu(self, variable=self.comp_type_var, values=["10% Br", "10% Zn", "10% EA", "Baseline", "20% Br"])
        # self.comp_dropdown.grid(row=7, column=0, padx=5, pady=2)

        # self.predict_button = ctk.CTkButton(self, text="Predict Efficiency", command=self.predict_efficiency)
        # self.predict_button.grid(row=8, column=0, padx=5, pady=5)

        # self.optimize_button = ctk.CTkButton(self, text="Run Genetic Optimization", command=self.run_optimization)
        # self.optimize_button.grid(row=9, column=0, padx=5, pady=5)

        # self.feature_button = ctk.CTkButton(self, text="Show Feature Importance", command=self.plot_feature_importance)
        # self.feature_button.grid(row=10, column=0, padx=5, pady=5)

        # self.top5_button = ctk.CTkButton(self, text="Suggest Top 5 Recipes", command=self.suggest_recipes)
        # self.top5_button.grid(row=11, column=0, padx=5, pady=5)

        # self.prediction_label = ctk.CTkLabel(self, text="Prediction: --", font=("Arial", 14))
        # self.prediction_label.grid(row=12, column=0, padx=5, pady=5)

        # Matplotlib figure for plotting
        self.figure, self.ax = plt.subplots(figsize=(4.8, 2.6))
        self.ax.set_title("Intensity vs Wavelength")
        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Intensity")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=2, column=0, padx=5, pady=5)
        # self.ml_button = ctk.CTkButton(self, text="Run ML Model", command=self.run_ml_script)
        # self.ml_button.grid(row=3, column=0, padx=10, pady=10)

    # def run_ml_script(self):
    #     script_path = "/home/ecd515/Desktop/PASS/src/InkAdditiveRFR.py"
    #     try:
    #         subprocess.run(['python3', script_path], check=True)
    #         self.status_label.configure(text="ML Model Completed. Output saved.")
    #     except subprocess.CalledProcessError as e:
    #         self.status_label.configure(text=f"ML script failed: {e}")
    #         print("Full error from subprocess:", e)

    def update_plot(self):
        """Fetch new spectrometer data and update the plot in real-time."""
        if not self.spectrometer or not self.spectrometer.is_connected():
            self.status_label.configure(text="Spectrometer not connected.")
            return

        try:
            self.status_label.configure(text="Measurement in Progress...")
            if not isinstance(self.spectrometer.wavelengths, np.ndarray) or self.spectrometer.wavelengths.size == 0:
                wavelengths = self.spectrometer.read_wavelengths()
            else:
                wavelengths = self.spectrometer.wavelengths

            intensities = self.spectrometer.read_spectrum("live")

            if (isinstance(intensities, np.ndarray) and isinstance(wavelengths, np.ndarray) and
                intensities.size > 0 and wavelengths.size > 0 and intensities.shape == wavelengths.shape):
                intensities = (intensities / np.max(intensities)) * 100
                self.ax.clear()
                self.ax.plot(wavelengths, intensities, color='blue', label="White Light Spectrum")
                self.ax.set_title("Intensity vs Wavelength")
                self.ax.set_xlabel("Wavelength (nm)")
                self.ax.set_ylabel("Intensity")
                self.ax.set_xlim(300, 1000)  # Clamp wavelength range
                self.ax.legend()
                self.figure.tight_layout()
                self.canvas.draw()

                self.status_label.configure(text="Measurement Complete")
            else:
                self.status_label.configure(text="No data received.")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")

    # def predict_efficiency(self):
    #     try:
    #         ink = self.ink_var.get()
    #         additive = self.additive_var.get()
    #         comp_type = self.comp_type_var.get()
    #         concentration = float(self.concentration_entry.get())
    #         comp_value = float(self.comp_value_entry.get())
    #         intensity = 1500000  # Placeholder (replace with live avg later)

    #         bg, eff = predict_bandgap_and_efficiency(
    #             intensity=intensity,
    #             ink=ink,
    #             additive=additive,
    #             concentration=concentration,
    #             composition_value=comp_value,
    #             composition_type=comp_type
    #         )

    #         if bg is not None:
    #             plot_sq_limit_overlay(bg, eff)
    #             self.prediction_label.configure(text=f"Bandgap: {bg:.3f} eV | Eff: {eff:.2f}%")
    #         else:
    #             self.prediction_label.configure(text="Prediction Failed")
    #     except Exception as e:
    #         self.prediction_label.configure(text=f"Error: {e}")

    # def run_optimization(self):
    #     result = genetic_algorithm()
    #     self.prediction_label.configure(
    #         text=f"Top: {result['Ink']}, {result['Additive']} | Eff: {result['Efficiency']:.2f}%"
    #     )
    #     plot_sq_limit_overlay(result['Bandgap'], result['Efficiency'])

    # def plot_feature_importance(self):
    #     plot_feature_importance()
    #     self.prediction_label.configure(text="Saved: feature_importance.png")

    # def suggest_recipes(self):
    #     top5 = get_top_5_recipes()
    #     msg = f"Top 1: {top5[0]['Ink']} + {top5[0]['Additive']} → {top5[0]['Efficiency']:.2f}%"
    #     self.prediction_label.configure(text=msg)

