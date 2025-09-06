from myutils import *
from main import lighting, W, H, resolution, scene, cube, circle
import mandlebulb
from lighting import Lighting, LightSource

drone_pos = [200, 250, 150]
settings_on = False
menu_pos = 0
values = [8, 1.0, 0, 10.0, 300, 300, 300, 0, 0]  # power,light,color,speed,w,h,res,shape,scene
saved_state = None



def move_drone(dir):
    global drone_pos
    step = 20
    if dir == 0:  # up
        drone_pos[1] += step
    elif dir == 1:  # down
        drone_pos[1] -= step
    elif dir == 2:  # left
        drone_pos[0] -= step
    elif dir == 3:  # right
        drone_pos[0] += step
    elif dir == 4:  # forward
        drone_pos[2] -= step
    elif dir == 5:  # backward
        drone_pos[2] += step

def update_drone_light():
    global lighting, drone_pos
    lighting.light_sources = []
    drone_light = LightSource(tuple(drone_pos))
    lighting.addLightSource(drone_light)

def setup_drone():
    global lighting, scene
    lighting = Lighting(ambient=(0.15, 0.15, 0.2), diffuse=values[1], shininess=32)
    update_drone_light()
    
    # Initialize scene 
    if values[8] == 0:
        scene = mandlebulb
    elif values[8] == 1:
        scene = cube
    elif values[8] == 2:
        scene = circle
