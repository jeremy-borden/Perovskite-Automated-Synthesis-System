import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from predictor import predict_bandgap_and_efficiency 
# from ml_optimizers import genetic_algorithm, get_top_5_recipes, plot_feature_importance, plot_sq_limit_overlay
import sys
import os
import numpy as np
import subprocess
from drivers import ml_driver

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


        # Matplotlib figure for plotting
        self.figure, self.ax = plt.subplots(figsize=(4.8, 2.6))
        self.ax.set_title("Intensity vs Wavelength")
        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Intensity")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=2, column=0, padx=5, pady=5)
        self.ml_button = ctk.CTkButton(self, text="Run ML Model", command=self.run_ml_model)
        self.ml_button.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="n")


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
                intensities = (intensities / np.max(intensities)) * 100  #Normalization 
                self.ax.clear()
                self.ax.plot(wavelengths, intensities, color='blue', label="White Light Spectrum")
                self.ax.set_title("Intensity vs Wavelength")
                self.ax.set_xlabel("Wavelength (nm)")
                self.ax.set_ylabel("Intensity %")
                self.ax.set_xlim(300, 1000)  # wavelength range
                #self.ax.set_ylim(0, 105) # intensity range
                self.ax.legend()
                self.figure.tight_layout()
                self.canvas.draw()

                self.status_label.configure(text="Measurement Complete")
            else:
                self.status_label.configure(text="No data received.")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")

    
    def run_ml_model(self):
        try:
            ml_driver.run_model()
            print("[INFO] ML Model executed. Check /persistant for output.")
            done_label = ctk.CTkLabel(self, text="ML Run Complete", text_color="green")
            done_label.grid(row=4, column=0, pady=5)
        except Exception as e:
            print(f"[ERROR] ML Model failed: {e}")
            error_label = ctk.CTkLabel(self, text="ML Run Failed", text_color="red")
            error_label.grid(row=4, column=0, pady=5)
    
