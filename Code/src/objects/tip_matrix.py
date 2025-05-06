import numpy as np

class TipMatrix():
    def __init__(self):
        self.small_tip_rows = 5
        self.small_x_offset = 5
        
        self.small_tip_columns= 11
        self.small_y_offset = 5
        
        self.big_tip_columns = 11
        self.big_x_offset = 5
        
        self.tips_taken = 0
        
        
        
    def take_tip(self):
        self.tips_taken += 1
    
    def get_tip_offset(self, big_tip: bool, tip_num: int):
        if not big_tip:
            x_offset = ((tip_num % self.small_tip_columns) * self.small_x_offset)
            y_offset = (np.floor(tip_num / self.small_tip_columns) * self.small_y_offset)
        else:
            x_offset = ((tip_num % self.big_tip_columns) * self.big_x_offset)
            y_offset = 57
            
        return x_offset, y_offset
            
    def refill_tips(self):
        self.tips_taken = 0
        
        
class SlideMatrix():
    def __init__(self):
        self.slide_rows = 5
        self.matrix_x_offset = 5
        
        self.slide_columns= 3
        self.matrix_y_offset = 5
        
        self.slides_taken = 0
 
    def take_slide(self):
        self.slides_taken += 1
    
    def get_slide_offset(self, slide_num: int):
        x_offset = ((slide_num % self.slide_columns) * self.matrix_x_offset)
        y_offset = (np.floor(slide_num / self.slide_columns) * self.matrix_y_offset)
        
        return x_offset, y_offset
            
    def refill_slides(self):
        self.slides_taken = 0
        