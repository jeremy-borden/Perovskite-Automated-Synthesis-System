import cv2
import numpy as np

class image_Component:
    def __init__(self, image: cv2.Mat = None):
        self.image = image
        
    def Get(self):
        return self.image
    
    def Set(self, image: cv2.Mat):
        self.image = image