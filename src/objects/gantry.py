
DEFAULT_SPEED = 1000

class GantryDriver:
    def __init__(self, controller):
        self.controller = controller
    
    def MoveToCoordinate(self, x:float = None, y:float = None, z:float = None, speed:int = DEFAULT_SPEED):
        """
        Sends G Code to move to the specified coordinates.
        At least one axis coordinate must be specified.
        Args:
            x (float, optional): _description_. Defaults to None.
            y (float, optional): _description_. Defaults to None.
            z (float, optional): _description_. Defaults to None.
            speed (int, optional): _description_. Defaults to DEFAULT_SPEED.
        """
        
        if((x==None) and (y==None) and (z==None)):
            print("no coords specified")
            return
        
        message = "G0"
        
        if(x != None): message = message + f" X{x}"
        if(y != None): message = message + f" Y{y}"
        if(z != None): message = message + f" Z{z}"
        message = message + f" F{speed}"
        
        self.controller.sendGCode(message)