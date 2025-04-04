import numpy as np

class TipMatrix():
    def __init__(self):
        self.small_tip_rows = 5
        self.small_tip_columns= 11
        self.big_tip_columns = 10
        
        self.topleft_tip_coords = [0,0,0]
        self.topleft_big_tip_coords = [0,0,0]
        self.tips_taken = 0
        self.small_x_offset = 5
        self.small_y_offset = 5
        self.big_x_offset = 5
    def take_tip(self):
        self.tips_taken += 1
        
    def get_next_tip_coords(self, big_tip: bool):
        if not big_tip:
            x = self.topleft_tip_coords[0] - ((self.tips_taken % self.small_tip_columns) * self.small_x_offset)
            y = self.topleft_tip_coords[1] - (np.floor(self.tips_taken / self.small_tip_columns) * self.small_y_offset)
            z = self.topleft_tip_coords[2]
        else:
            x = self.topleft_big_tip_coords[0] - ((self.tips_taken % self.small_tip_columns) * self.big_x_offset)
            y = self.topleft_big_tip_coords[1]
            z = self.topleft_big_tip_coords[2]
        return x, y, z
    def refill_tips(self):
        self.tips_taken = 0