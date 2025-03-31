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
import time
from data_processor import plot_spectra, save_all_to_csv  


# debugging
logging.basicConfig(level=logging.INFO)

class Spectrometer:
    """Handles Ossila Spectrometer communication, data collection, and saving to CSV"""

    def __init__(self, integration_time=2000):
        self.logger = logging.getLogger("Main Logger")
        self.integration_time = integration_time
        self.serial = None
        self.wavelengths = []
        self.measurements = {}  # to store intensities for Background, Reference, and Sample

    def connect(self, port_num):
        """Establish connection to the spectrometer"""
        
        
        port = "/dev/ttyACM" + str(port_num)
        try:
            self.serial = serial.Serial(port, baudrate=115200, timeout=5)
            self.logger.info(f"Connected to spectrometer on {port}")
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

    def send_command(self, command):
        """Send a command to the spectrometer and return the response"""
        if self.is_connected():
            self.serial.write((command + "\n").encode())
            time.sleep(0.1)
            response = self.serial.readline().decode().strip()
            self.logger.info(f"Sent: {command}, Received: {response}")
            return response

    def set_integration_time(self):
        """Set the integration time for measurements"""
        command = f"<itime:{self.integration_time}>"
        self.send_command(command)

    def read_wavelengths(self):
        """Retrieve wavelength data from the spectrometer"""
        response = self.send_command("<wavs?>")
        self.wavelengths = np.fromstring(response, sep=',')
        self.logger.info(f"Read {len(self.wavelengths)} wavelength values.")

        return self.wavelengths


    def read_spectrum(self, measurement_type):
        """Read spectral intensity for a given measurement type"""
        if not self.is_connected():
            self.logger.warning("Spectrometer not connected.")
            return np.array([])
            
        self.serial.reset_input_buffer()
        
        self.send_command(f"<itime:{self.integration_time}>")
        time.sleep(0.3)
        
        self.serial.write(b"<read:1>\n")
        time.sleep(0.3)
        
        raw_data = self.serial.read(3204)
        
        print(f"[DEBUG] Raw data length: {len(raw_data)}")
        
        if len(raw_data) < 3204:
            self.logger.warning("Incomplete spectrum data received.")
            return np.array([])

        
        intensities = np.frombuffer(raw_data[2:3202], dtype=np.uint16)

        # Store the collected data
        self.measurements[measurement_type] = intensities
        self.logger.info(f"Read {len(intensities)} intensity values for {measurement_type}.")

        return intensities


"""1. Connects to the spectrometer

2. Sets integration time

3. Reads wavelengths

4. Collects three spectra types

5. Saves all data to CSV

6. Plots the spectral data

7. Disconnects safely
"""
