


from locale import currency

# TODO turn vial class into dataclass and have the vial carosel handle the rest
class Vial():
    def __init__(self, max_volume_ul: int, fluid_name: str):
        self.max_volume_ul = max_volume_ul
        self.fluid_name = fluid_name
        self.current_volume_ul = 0
        
    def refill(self):
        self.current_volume_ul = self.max_volume_ul
        
    def extract(self, volume_ul: int):
        if self.current_volume_ul < volume_ul:
            raise ValueError("Exctraction volume exceeds current volume")
        if volume_ul < 0:
            raise ValueError("Volume cannot be negative")
        
        self.current_volume_ul -= volume_ul
        
    def deposit(self, volume_ul: int):
        if self.current_volume_ul + volume_ul > self.max_volume_ul:
            raise ValueError("Deposited volume will exceed maximum volume")
        if volume_ul < 0:
            raise ValueError("Volume cannot be negative")
        
        self.current_volume_ul += volume_ul
        
    def get_current_volume(self):
        return self.current_volume_ul
    
    