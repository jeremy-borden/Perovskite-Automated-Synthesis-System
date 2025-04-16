from drivers.controlboard_driver import ControlBoard

class VialCarousel():
    
    VIAL_MAX_VOLUME_UL: int = 100000
    VIALS: int = 12
    def __init__(self, control_board: ControlBoard):
        self.control_board = control_board
        
        self.current_vial = 0
        self.vial_volumes_ul = [0]*self.VIALS
    
    def home(self):
        self.control_board.send_message("G28 A")
    
    def remove_fluid(self, vial_num: int, volume_ul: int):
        """ Removes fluid from the specified vial. Returns True if the 
        entire volume can be removed, and removes it.Otherwise return 
        False and do not change the fluid in the vial"""
        #return if outside of vial range
        if vial_num >= self.VIALS or vial_num < 0: 
            return False
        
        if self.vial_volumes_ul[vial_num] - volume_ul < 0:
            return False
        
        self.vial_volumes_ul[vial_num] -= volume_ul
        return True
    
    def add_fluid(self, vial_num: int, volume_ul: int):
        """ Adds fluid in the specified vial. Returns true if sum of volumes
        do not exceed the max amount the vials can hold. Otherwise it retuns false"""
        
        #return if outside of vial range
        if vial_num >= self.VIALS or vial_num < 0: 
            return False
        if self.vial_volumes_ul[vial_num]+volume_ul > self.VIAL_MAX_VOLUME_UL:
            return False
        return True
    
    def set_fluid(self, vial_num: int, volume_ul: int):
        """ Sets the amount of fluid in the specified vial. Returns true if volume
        doesnt exceed the max amount the vials can hold. Otherwise it retuns false"""
        #return if outside of vial range
        if vial_num >= self.VIALS or vial_num < 0: 
            return False
        if volume_ul > self.VIAL_MAX_VOLUME_UL:
            return False
        
        self.vial_volumes_ul[vial_num] = volume_ul
        return True

    def clear_fluid(self, vial_num: int):
        #return if outside of vial range
        if vial_num >= self.VIALS or vial_num < 0: 
            return False
        
        self.vial_volumes_ul[vial_num] = 0
        return True
        
    def set_vial(self, vial_num: int):
        if vial_num >12:
            vial_num = 11
        initial_offset = 0.4
        next_vial_offset = 2.65
        self.control_board.move_axis("A", initial_offset + (vial_num * next_vial_offset), finish_move=True)
        self.current_vial = vial_num

