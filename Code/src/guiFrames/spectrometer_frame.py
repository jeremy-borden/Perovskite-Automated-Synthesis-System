import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

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
            font=("Arial", 14)
        )
        self.status_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Matplotlib figure for plotting
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.ax.set_title("Intensity vs Wavelength")
        self.ax.set_xlabel("Wavelength (nm)")
        self.ax.set_ylabel("Intensity")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=2, column=0, padx=5, pady=5)

        self.update_plot()

    def update_plot(self):
        """Fetch new spectrometer data and update the plot in real-time."""
        if not self.spectrometer or not self.spectrometer.is_connected():
            self.status_label.configure(text="Spectrometer not connected.")
            return

        try:
            self.status_label.configure(text="Measurement in Progress...")

            wavelengths = self.spectrometer.read_wavelengths()
            
            self.spectrometer.send_command("<read:1>")
            intensities = self.spectrometer.read_spectrum("live")
            

            if intensities is not None and wavelengths is not None and len(intensities) == len(wavelengths):
                self.ax.clear()
                self.ax.plot(wavelengths, intensities, color='blue', label="PL Spectrum")
                self.ax.set_title("Intensity vs Wavelength")
                self.ax.set_xlabel("Wavelength (nm)")
                self.ax.set_ylabel("Intensity")
                self.ax.legend()
                self.canvas.draw()

                self.status_label.configure(text="Measurement Complete")
            else:
                self.status_label.configure(text="No data received.")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            
        if self.winfo_exists():
            self.after(1000, self.update_plot)
