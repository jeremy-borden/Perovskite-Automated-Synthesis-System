import threading
import logging

import cv2
import customtkinter as ctk


class Camera(threading.Thread):
    def __init__(self, logger: logging.Logger):
        super().__init__(
            name="Camera",
            daemon=True)

        self.logger = logger

        self.video_capture = None
        self.frame = None

    def connect(self):
        if self.video_capture is not None:
            self.logger.error("Camera is already connected")
            return
        self.video_capture = cv2.VideoCapture(0)

    def run(self):
        while True:
            if self.video_capture is None:
                continue

            ret, frame = self.video_capture.read()
            if ret is True:
                self.frame = frame

    def stop(self):
        self.video_capture.release()
        self.logger.info("Camera stopped")

    def get_frame(self):
        return self.frame
