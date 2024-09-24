import customtkinter as ctk

class CameraFrame(ctk.CTkFrame):
    def __init__(self, master, cap):
        super().__init__(master)
        self.cap = cap
        
        self.imageLabel = ctk.CTkLabel(self, text = "Image", image = None)
        self.imageLabel.grid(row=0, column=0, padx=20, pady=20, sticky="")
        
    def updateImage(self):
        ret, frame = self.cap.read()
        if ret is True:
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

            # Capture the latest frame and transform to image 
            captured_image = Image.fromarray(opencv_image) 
            imagee = ctk.CTkImage(light_image = captured_image, dark_image=captured_image, size=(400, 400))
            
            self.imageLabel.configure(image = imagee, require_redraw=True)
            self.imageLabel.after(20, self.updateImage)