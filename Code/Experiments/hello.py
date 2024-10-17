import numpy as np
import cv2
import pickle
  
# Load Aruco detector
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
print("Loaded Aruco Dictionary")

cap = cv2.VideoCapture(0)
print("Loaded Camera")

camArray = np.array(pickle.load(open( "cameraMatrix.pkl", "rb" )))
np.save('camera_coefficients.npy', camArray)
cameraMatrix = cv2.UMat(camArray)

distArray = np.array(pickle.load(open( "dist.pkl", "rb" )))
np.save('dist_coefficients.npy', distArray)
dist = cv2.UMat(distArray)



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

    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix).get()
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
    
    
    if len(corners) > 0:
        
        for i in range(0, len(corners)):

            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.050, cameraMatrix, dist)
           

            e = cv2.drawFrameAxes(dst, cameraMatrix, dist, rvec, tvec, 0.025) 
            img = e
            e = cv2.putText(img, str(tvec.get()), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, 1)
            img = e
            

            
    cv2.imshow("Image", img)
    
  
    # press esc to exit
    key = cv2.waitKey(1)
    if key == 27:
        break




cap.release()
cv2.destroyAllWindows()
