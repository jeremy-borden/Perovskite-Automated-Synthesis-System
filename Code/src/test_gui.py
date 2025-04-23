import customtkinter as ctk
from guiFrames.ml_model_frame import MLModelFrame

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1000x700")
    app.title("ML Model Test")

    ml_frame = MLModelFrame(app)
    ml_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    app.mainloop()
