from textwrap import wrap
import numpy as np
import cv2
import pickle

FRAME_WIDTH_PIXEL = 640
FRAME_HEIGHT_PIXEL = 480
# Load Aruco detector
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
print("Loaded Aruco Dictionary")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
print("Loaded Camera")



print("Loading Camera Coefficients...",end = "")
camera_coefficients = np.load('Code/Experiments/camera_coefficients.npy')
print("Loading Distortion Coefficients...",end = "")
distortion_coefficients = np.load('Code/Experiments/dist_coefficients.npy')
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(camera_coefficients, distortion_coefficients, (FRAME_WIDTH_PIXEL, FRAME_HEIGHT_PIXEL), 1, (FRAME_WIDTH_PIXEL, FRAME_HEIGHT_PIXEL))
print("Loaded Camera And Distortion Coefficients")



def aruco_centers(img, corners):
    corners, ids, rejected = detector.detectMarkers(img)
    x_centers, y_centers = [], []
    perms = []
    i = 0
    for corner in corners:
        # Aruco Marker Perimeter
        aruco_perimeter = cv2.arcLength(corner[0], True)
        perms.append(aruco_perimeter)
        # Aruco marker center
        x_center = (corner[0][0][0] + corner[0][1][0] + corner[0][2][0] + corner[0][3][0]) / 4
        y_center = (corner[0][0][1] + corner[0][1][1] + corner[0][2][1] + corner[0][3][1]) / 4
        x_centers.append(x_center)
        y_centers.append(y_center)
        #cv2.circle(img, (int(x_center), int(y_center)), 4, (0, 0, 255), -1)
        pixel_cm_ratio = aruco_perimeter / 20
        
        # Pixel to cm ratio, perimeter of 5cm wide marker is 20cm
        
        i+=1
    return np.array(x_centers), np.array(y_centers), np.array(perms)
    
    
    
while True:
    _, img = cap.read()
    
    
    h,  w = img.shape[:2]


    dst = cv2.undistort(img, camera_coefficients, distortion_coefficients, None, newCameraMatrix)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    
    
    
    # Get Aruco marker
    corners, ids, rejected = detector.detectMarkers(img)
    x_centers, y_centers, perms = aruco_centers(img, corners)
    #cv2.polylines(img, np.intp(corners), True, (0, 255, 0), 1)
    
    # dcorners, ids, rejected = detector.detectMarkers(dst)
    # dx_centers, dy_centers, dperms = aruco_centers(dst, dcorners)
    #cv2.polylines(dst, np.intp(dcorners), True, (0, 255, 0), 1)

    # if(len(x_centers)>= 2):
    #     distance = cv2.norm(np.array([x_centers[1], y_centers[1]]) - np.array([x_centers[0], y_centers[0]]))
    #     print("img", distance/(perms[0]/20))
    #     if(len(dx_centers)>= 2):
    #         ddistance = cv2.norm(np.array([dx_centers[1], dy_centers[1]]) - np.array([dx_centers[0], dy_centers[0]]))
    #         #print("dst", ddistance/(dperms[0]/20))
    #         print("diff", abs(ddistance/(dperms[0]/20.2) - distance/(perms[0]/20.2)))
    
    

    for corner in corners:

        rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corner, 0.050, camera_coefficients, distortion_coefficients)


        e = cv2.drawFrameAxes(dst, camera_coefficients, distortion_coefficients, rvec, tvec, 0.025) 
        R = cv2.Rodrigues(rvec)
        img = e
        e = cv2.putText(img, str(R[0]), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, 1)
        img = e
            

            
    cv2.imshow("Image", img)
    
  
    # press esc to exit
    key = cv2.waitKey(1)
    if key == 27:
        break




cap.release()
cv2.destroyAllWindows()
