import customtkinter as ctk  # <- import the CustomTkinter module
from PIL import Image
import numpy as np
import cv2
#https://customtkinter.tomschimansky.com/documentation/windows/window

FRAME_WIDTH_PIXEL = 640
FRAME_HEIGHT_PIXEL = 480

# Create a label in the frame



# # Capture from camera
# cap = cv2.VideoCapture(0)

# def capture_stream():
#     ret, cv2image = cap.read()
#     if ret == True:
#         print("h")
#         #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

#         my_image = ctk.CTkImage(dark_image=Image.fromarray(cv2image), size=(480, 640))
        
#         label.configure(image = my_image, height = 480, width = 640)
#         label.pack()

# btn = ctk.CTkButton(app, text="Click me", corner_radius= 10, command=capture_stream)
# btn.configure(corner_radius=10, border_width=2, border_color="#333333")
# btn.pack(pady=20)
# btn.place(relx=0.5, rely=0.5, anchor="center")

print("Loading Camera Coefficients...",end = "")
camera_coefficients = np.load('camera_coefficients.npy')
print("Loading Distortion Coefficients...",end = "")
distortion_coefficients = np.load('dist_coefficients.npy')
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(camera_coefficients, distortion_coefficients, (FRAME_WIDTH_PIXEL, FRAME_HEIGHT_PIXEL), 1, (FRAME_WIDTH_PIXEL, FRAME_HEIGHT_PIXEL))
print("Loaded Camera And Distortion Coefficients")

class Camera:
    def __init__(self, camera_matrix, distortion_coefficients, width_px = FRAME_WIDTH_PIXEL, height_px = FRAME_HEIGHT_PIXEL):
        self.camera_matrix = camera_matrix
        self.distortion_coefficients = distortion_coefficients
        self.width_px = width_px
        self.height_px = height_px

    def OpenVideoCapture(self):
        print ("Opening Camera...",end = "")
        videoCapture = cv2.VideoCapture(0)
        videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width_px)
        videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height_px)
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

class UserInterface(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.geometry("600x500")
        self.title("CTk example")

        # add widgets to app
        self.button = ctk.CTkButton(self, command=self.button_click)
        self.button.grid(row=0, column=0, padx=20, pady=10)
        self.label = ctk.CTkLabel(self, text="")
        self.label.grid(row=1, column=0, padx=20, pady=10)
        
    def button_click(self):
        print("Button Clicked")
        self.label.configure(text="new text")
        
        
        
        
cam = Camera(camera_matrix=camera_coefficients, distortion_coefficients=distortion_coefficients)
videoCapture = cam.OpenVideoCapture()
frame = cam.GetFrame(videoCapture)

ui = UserInterface()

app = ctk.CTkFrame(ui)
label = ctk.CTkLabel(app, height = 200, width = 200)



ui.mainloop()

# btn = ctk.CTkButton(app, text="Click me", corner_radius= 10, command=update)
# btn.configure(corner_radius=10, border_width=2, border_color="#333333")
# btn.pack(pady=20)
# btn.place(relx=0.5, rely=0.5, anchor="center")


