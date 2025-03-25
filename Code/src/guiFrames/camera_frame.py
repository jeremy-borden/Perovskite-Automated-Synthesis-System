import customtkinter as ctk
import cv2
from PIL import Image
import sys
import os

# get current directory so we can import from outside guiFrames folder
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)
from src.drivers.camera_driver import Camera
from src.drivers.spectrometer_driver import Spectrometer

class CameraFrame(ctk.CTkFrame):
    def __init__(self, master, camera: Camera):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2)
        
        self.camera = camera

        # title
        self.title_label = ctk.CTkLabel(
            master=self,
            text="Camera Feed",
            justify="left",
            anchor="w",
            font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky = "w")
        
        # image label
        self.image_label = ctk.CTkLabel(
            master=self,
            text="",
            width=400,
            height=300)
        self.image_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.update_image()
        
    def update_image(self):
        frame = self.camera.get_frame()
        if frame is not None:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ctk.CTkImage(light_image=image, size=(400, 300))
            
            self.image_label.configure(image=image)
            self.image_label.image = image
        self.after(int(1000/60), self.update_image)


class SpectrometerFrame(ctk.CTkFrame):
    def __init__(self, master, spectrometer: Spectrometer):
        super().__init__(
            master=master,
            border_color="#1f6aa5",
            border_width=2)

        self.spectrometer = spectrometer

        self.title_label = ctk.CTkLabel(
            master=self,
            text="Spectrometer Live Data",  #title for spectrometer frame
            justify="left",
            anchor="w",
            font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # measurement Status
        self.status_label = ctk.CTkLabel(
            master=self,
            text="Waiting for Data...", 
            justify="left",
            anchor="w",
            font=("Arial", 14))
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
        if self.spectrometer:
            self.status_label.configure(text="Measurement in Progress...")  # Update status
            
            self.spectrometer.send_command("<read:1>")  # Trigger measurement
            intensities = self.spectrometer.read_spectrum()
            wavelengths = self.spectrometer.read_wavelengths()

            if intensities and wavelengths:
                self.ax.clear()
                self.ax.plot(wavelengths, intensities, color='blue', label="PL Spectrum")
                self.ax.set_title("Intensity vs Wavelength")
                self.ax.set_xlabel("Wavelength (nm)")
                self.ax.set_ylabel("Intensity")
                self.ax.legend()
                self.canvas.draw()

                self.status_label.configure(text="Measurement Complete")  # Ststus update 
