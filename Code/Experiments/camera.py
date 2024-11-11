import numpy as np
import cv2

from Components import gantry_component, image_component

FRAME_WIDTH_PIXEL = 640
FRAME_HEIGHT_PIXEL = 480


# Reading in the camera matrix and distortion coefficients
print("Loading Aruco Dictionary...",end = "")
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
print("Loaded Aruco Dictionary")

print("Loading Camera Coefficients...",end = "")
camera_coefficients = np.load('Code/Experiments/camera_coefficients.npy')
print("Loading Distortion Coefficients...",end = "")
distortion_coefficients = np.load('Code/Experiments/dist_coefficients.npy')
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(camera_coefficients, distortion_coefficients, (FRAME_WIDTH_PIXEL, FRAME_HEIGHT_PIXEL), 1, (FRAME_WIDTH_PIXEL, FRAME_HEIGHT_PIXEL))
print("Loaded Camera And Distortion Coefficients")

class Camera:
    def __init__(self, camera_matrix, distortion_coefficients):
        #Parameter initialization
        self.camera_matrix = camera_matrix
        self.distortion_coefficients = distortion_coefficients
        
        #Component initialization
        self.gantry = gantry_component.gantry_component("COM3")
        self.image = image_component.image_component()

    def OpenVideoCapture(self):
        print ("Opening Camera...",end = "")
        videoCapture = cv2.VideoCapture(0)
        print("Opened Camera")
        return videoCapture
        
    def CloseVideoCapture(self, videoCapture):
        print("Closing Camera...", end = "")
        videoCapture.release()
        print("Closed Camera")
        
    def GetFrame(self, videoCapture):
        ret, frame = videoCapture.read()
        if ret is False:
            return None
        return frame

    def UndistortFrame(self, frame):
        undistorted_frame = cv2.undistort(frame, self.camera_matrix, self.distortion_coefficients, None, self.camera_matrix)
        return undistorted_frame

    def GetArucoCenters(self, frame, corners):
        x_centers = []
        y_centers = []
        
        for corner in corners:
            x_center = np.mean(corner)
            x_centers.append(x_center)
        
        return np.array(x_centers), np.array(y_centers)
        
    def ProcessFrame(self, frame):
        corners, ids, rejected = detector.detectMarkers(frame)
        
        
        