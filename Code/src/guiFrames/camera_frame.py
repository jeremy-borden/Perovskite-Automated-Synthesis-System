import customtkinter as ctk
import cv2
from PIL import Image
import sys
import os

# get current directory so we can import from outside guiFrames folder
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)
from drivers.camera_driver import Camera

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
        self.after(int(1000/20), self.update_image)
