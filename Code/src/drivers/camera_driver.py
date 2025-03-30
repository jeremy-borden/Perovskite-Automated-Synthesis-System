import threading
import logging
from time import sleep
import cv2
import customtkinter as ctk


class Camera(threading.Thread):
    def __init__(self):
        super().__init__(name="Camera",daemon=True)

        self.logger = logging.getLogger("Main Logger")

        self.video_capture = None
        self.frame = None
        
        self.running = threading.Event()
        self.release = threading.Event()
        self.start()
        

    def connect(self):
        if self.is_connected():
            self.logger.error("Camera is already connected")
            return 
        
        try:
            self.video_capture = cv2.VideoCapture(0) # DSHOW for windows only, otherwise try V42L
            self.running.set()
            self.logger.debug("Connected to camera")
        except cv2.error as e:
            self.logger.error(f"Error connecting to camera: {e}")
            
            
    def disconnect(self):
        if not self.is_connected():
            return
        
        self.running.clear()
        self.release.set()
        self.logger.debug("Camera stopped")
    
    

    def run(self):
        while True:
            self.running.wait()
            self.release.clear()
   
            while self.is_connected():
                sleep(0.0)
                try:
                    ret, frame = self.video_capture.read()
                    if ret is True:
                        self.frame = frame
                    else:
                        self.logger.error(f"Camera stopped returning frames")
                        self.video_capture = None
                        self.running.clear()
                        break
                        
                except cv2.error as e:
                    self.logger.error(f"Error while reading videocapture: {e}")

                if self.release.is_set():
                    self.video_capture.release()
                    self.video_capture = None
                
            self.running.clear()

    def get_frame(self):
        return self.frame
    
    def is_connected(self):
        return (self.video_capture is not None) and (self.video_capture.isOpened())
