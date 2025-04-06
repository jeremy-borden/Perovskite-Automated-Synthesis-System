import logging
import customtkinter as ctk
import os
import sys

# get current directory so we can import from outside guiFrames folder
pp=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(pp)
from src.drivers.procedure_file_driver import ProcedureFile

class LocationFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master=master, width=300)
        self.location_entries = []
        self._load_locations()
        
        # save button
        self.save_button = ctk.CTkButton(master=self, text="Save",
                                         command=self._save_locations)
        self.save_button.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        # new entry button
        self.new_entry_button = ctk.CTkButton(master=self, text="New Entry", 
                                              command=self._new_entry)
        self.new_entry_button.grid(row=0, column=1, padx=5, pady=5,sticky="nw")
        
        
    def _new_entry(self):
        location_entry = LocationEntry(master=self)
        location_entry.grid(row=len(self.location_entries)+1, column=0, columnspan=2, padx=5, pady=5)
        self.location_entries.append(location_entry)
        return location_entry
        
        
    def _save_locations(self):
        location_data = []
        
        for entry in self.location_entries:
            location = entry.get_entry()
            if (location[0] != ""):
                location_data.append(location)
        
        ProcedureFile().Save("persistant/locations", location_data)
        
    def _load_locations(self):
        location_data = ProcedureFile().Open("persistant/locations.yml")
        for location in location_data:
            new_location = self._new_entry()
            new_location.load_entry(location[0], location[1],location[2],location[3])
            
            
class LocationEntry(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        
        self.location_name = ctk.CTkEntry(master=self, width = 100, placeholder_text="Location Name")
        self.location_name.grid(row=0, column=0,padx=5,pady=5)
        
        self.x_coord = ctk.CTkEntry(master=self, width=50, placeholder_text="X")
        self.x_coord.grid(row=0, column=1,padx=5,pady=5)
        
        self.y_coord = ctk.CTkEntry(master=self,width=50,placeholder_text="Y")
        self.y_coord.grid(row=0, column=2,padx=5,pady=5)
        
        self.z_coord = ctk.CTkEntry(master=self,width=50, placeholder_text="Z")
        self.z_coord.grid(row=0, column=3,padx=5,pady=5)
        
    def get_entry(self):
        location = self.location_name.get()
        x = self.x_coord.get()
        y = self.y_coord.get()
        z = self.z_coord.get()
        
        for coord in (x,y,z):
            if coord == "":
                coord = 0
        
        return [location, x, y, z]
    
    def load_entry(self, name, x, y, z):
        self.location_name.insert(0, name)
        self.x_coord.insert(0, x)
        self.y_coord.insert(0, y)
        self.z_coord.insert(0, z)
        
        
if __name__ == "__main__":
    app = ctk.CTk()
    ctk.set_appearance_mode("dark")
    app.geometry("1200x1000")
    lf = LocationFrame(app)
    lf.grid(row=0, column=0)
    app.mainloop()