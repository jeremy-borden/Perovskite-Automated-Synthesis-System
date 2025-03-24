# -*- coding: utf-8 -*-
"""spectrometer-rasberrypi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yK9vuu3NmPzc_fxeyzYqFBAWe1YKVdny

# **Spectrometer Script for Raspberry Pi**
"""

import serial
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

# debugging
logging.basicConfig(level=logging.INFO)

class Spectrometer:
    """Handles Ossila Spectrometer communication, data collection, and saving to CSV"""

    def __init__(self, com_port: str, integration_time=1000):
        self.logger = logging.getLogger("Main Logger")
        self.com_port = com_port
        self.integration_time = integration_time
        self.serial = None
        self.wavelengths = []
        self.measurements = {}  # to store intensities for Background, Reference, and Sample

    def connect(self):
        """Establish connection to the spectrometer"""
        try:
            self.serial = serial.Serial(self.com_port, baudrate=115200, timeout=3)
            self.logger.info(f"Connected to spectrometer on {self.com_port}")
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to spectrometer: {e}")

    def disconnect(self):
        """Close the serial connection"""
        if self.is_connected():
            self.serial.close()
            self.logger.info("Spectrometer Disconnected")

    def is_connected(self):
        """Check if the spectrometer is connected"""
        return self.serial is not None and self.serial.is_open

    def send_message(self, command):
        """Send a command to the spectrometer and return the response"""
        if self.is_connected():
            self.serial.write((command + "\n").encode())
            response = self.serial.readline().decode().strip()
            self.logger.info(f"Sent: {command}, Received: {response}")
            return response

    def set_integration_time(self):
        """Set the integration time for measurements"""
        command = f"<itime:{self.integration_time}>"
        self.send_message(command)

    def read_wavelengths(self):
        """Retrieve wavelength data from the spectrometer"""
        response = self.send_message("<wavs?>")
        self.wavelengths = np.fromstring(response, sep=',')
        self.logger.info(f"Read {len(self.wavelengths)} wavelength values.")

    def read_spectrum(self, measurement_type):
        """Read spectral intensity for a given measurement type"""
        self.send_message("<read:1>")
        raw_data = self.serial.read(3204)
        intensities = np.frombuffer(raw_data[2:3202], dtype=np.uint16)

        # Store the collected data
        self.measurements[measurement_type] = intensities
        self.logger.info(f"Read {len(intensities)} intensity values for {measurement_type}.")

#TODO please move all methods that dont specifically implement spectrometer 
# commands or otherwise can be decoupled to another file, perhaps like image processor
    def plot_spectra(self):
        """Plot the collected spectra"""
        plt.figure(figsize=(8, 5))
        for measurement_type, intensities in self.measurements.items():
            plt.plot(self.wavelengths, intensities, label=measurement_type)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        plt.title("Spectra Measurements")
        plt.legend()
        plt.show()

    def save_all_to_csv(self, filename="all_spectra_data.csv"):
        """Save all collected spectral data to a single CSV file"""
        data = []

        # to check if wavelength data is available
        if not self.wavelengths:
            self.read_wavelengths()

        # Collect data
        for measurement_type, intensities in self.measurements.items():
            for wl, intensity in zip(self.wavelengths, intensities):
                data.append([wl, intensity, measurement_type])

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["Wavelength", "Intensity", "Measurement Type"])

        # save to CSV
        df.to_csv(filename, index=False)
        self.logger.info(f"All spectra data saved to {filename}")

# TODO move this one to moves
# Automated Measurement Sequence
def automated_measurement():
    """Runs a full measurement cycle (Background, Reference, Sample) and saves the data"""

    spectrometer = Spectrometer(com_port="COM18", integration_time=1000)  # need to change to our port name
    spectrometer.connect()

    # Set
    spectrometer.set_integration_time()

    # Read
    spectrometer.read_wavelengths()

    # measurements for different spectra
    measurement_types = ["Background", "Reference", "Sample"]
    for measurement in measurement_types:
        spectrometer.read_spectrum(measurement)

    # Save all spectra data to a single CSV
    spectrometer.save_all_to_csv("all_spectra_data.csv")

    # Plot spectra
    spectrometer.plot_spectra()

    # Disconnect
    spectrometer.disconnect()

# Run automated sequence
if __name__ == "__main__":
    automated_measurement()

"""1. Connects to the spectrometer

2. Sets integration time

3. Reads wavelengths

4. Collects three spectra types

5. Saves all data to CSV

6. Plots the spectral data

7. Disconnects safely
"""