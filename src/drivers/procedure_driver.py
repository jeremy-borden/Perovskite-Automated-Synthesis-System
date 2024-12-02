
from numpy import double
import yaml
from controlboard_driver import ControlBoard

PIPETTE_X_OFFSET = 0
PIPETTE_Y_OFFSET = 0
PIPETTE_Z_OFFSET = 0

CAMERA_Y_OFFSET = 0
CAMERA_X_OFFSET = 0
CAMERA_Z_OFFSET = 0

GRIPPER_X_OFFSET = 0
GRIPPER_Y_OFFSET = 0
GRIPPER_Z_OFFSET = 0


class ProcedureDriver:
    def __init__(self, gantry_driver: GantryDriver):
        
        #upon creation, load default procedure
        self.procedure = ProcedureLoader("src/default_procedure.yml")
        self.procedure.Open()
        self.procedure.Load()
        
    def GoTo(self, x: double, y: double, z: double, center_reference = None):
        if center_reference == "pipette":
            x+= PIPETTE_X_OFFSET
            y+= PIPETTE_Y_OFFSET
            z+= PIPETTE_Z_OFFSET
        elif center_reference == "camera":
            x+= CAMERA_X_OFFSET
            y+= CAMERA_Y_OFFSET
            z+= CAMERA_Z_OFFSET
        elif center_reference == "gripper":
            x+= GRIPPER_X_OFFSET
            y+= GRIPPER_Y_OFFSET
            z+= GRIPPER_Z_OFFSET
            
        self.gantry_driver.sendGCode(f"G0 X{x} Y{y} Z{z}")
        
            
        
        
        
class ProcedureLoader:
    def __init__(self, path):

        #upon creation, load default procedure
        self.path = path
        self.Open()

        self.config = None
        self.bake_time_seconds = None
        self.bake_temp_celsius = None
        self.procedure = None
        
        
    def Open(self):
        with open(self.path, 'r') as f:
            self.config = yaml.safe_load(f)
            print(type(self.config))

    
    def Load(self):
        self.bake_time_seconds = self.config['Settings']['bakeTimeSeconds']
        self.bake_temp_celsius = self.config['Settings']['bakeTempCelsius']
        
        self.procedure = self.config['Procedure']
        
    
class ProcedureParser:
    def __init__(self, gantry_driver: GantryDriver):
        self.gantry_driver = gantry_driver
        
        
        
    def CompleteMove(self, move_num: int, move_list: list[str]):
        move = move_list[move_num]
        
        match move:
            case "HOME":
                pass
            case "GOTO":
                pass
            case "GRIPPERHAND":
                pass
        
        
if __name__ == "__main__": 
    pl = ProcedureLoader("src/default_procedure.yml")
    f = pl.Open()
    pl.Load()

    print(pl.bake_time_seconds)
    print(pl.bake_temp_celsius)
    print(pl.procedure)
    print(pl.config)