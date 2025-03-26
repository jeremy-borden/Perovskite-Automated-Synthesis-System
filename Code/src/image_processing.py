import numpy as np
import cv2



class ImageProcessor():
    aruco_detector: cv2.aruco.ArucoDetector
    
    def get_marker_angles(image, marker_id: int) -> float:
        """Returns the average angle of all aruco markers of a specific id in the image.  
            Args:
                image: input image.
                detector: cv2 aruco marker detector.
                marker_id: the id of the aruco marker
                
            Returns: 
                float: the angle that the aruco markers are rotated in the ccw direction.
        """
        if image is None:
            return None
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #gray_image = (255-gray_image) // invert image 
        corners, ids, rejected = ImageProcessor.aruco_detector.detectMarkers(gray_image)
        
        if ids is None:                                 
            return None
        
        camera_coefficients = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) # assume pinhole camera
        distortion_coefficients = np.array([])
        roll_angles = []
        
        for (corner, id) in zip(corners, ids):
            if id == marker_id:
                rotation_vector, translation_vector, marker_points = cv2.aruco.estimatePoseSingleMarkers(corner, 0.050, camera_coefficients, distortion_coefficients)
                
                rotation_matrix = cv2.Rodrigues(rotation_vector)[0]
                
                roll = -np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
                roll = np.rad2deg(roll)
                roll = np.mod(roll, 360) # make sure the angle is between 0 and 360
                
                roll_angles.append(roll)
                
            angle = np.mean(roll_angles)
        
        return angle

    def set_detector():
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        ImageProcessor.aruco_detector = cv2.aruco.ArucoDetector(dictionary, parameters)
        
    
    
    
if __name__ == "__main__":
    # Load Aruco detector
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)
    cap = cv2.VideoCapture(0)

    while True:
        ret, image = cap.read()
        if ret is True:
            angle = ImageProcessor.get_marker_angles(image, 0)
        cv2.putText(image, str(angle), (5, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, 1)
            
        cv2.imshow("Image", image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break