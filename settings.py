from main import lighting, W, H, resolution, scene, cube, circle
import mandlebulb
from lighting import LightSource
settings_on = False
menu_pos = 0
values = [8, 1.0, 0, 10.0, 300, 300, 300, 0, 0]  # power, light, color, speed, w, h, res, shape, scene

def toggle_settings():
    global settings_on
    settings_on = not settings_on

def move_menu(up):
    global menu_pos
    if up:
        menu_pos -= 1
        if menu_pos < 0:
            menu_pos = 8 #9settings
    else:
        menu_pos += 1
        if menu_pos > 8:
            menu_pos = 0

def change_value(up):
    global values, W, H, resolution, scene
    i = menu_pos
    
    if i == 0:  # power
        if up:
            values[0] += 1
        else:
            values[0] -= 1
        if values[0] < 2:
            values[0] = 2
        if values[0] > 14:
            values[0] = 14
            
    elif i == 1:  # light
        if up:
            values[1] += 0.1
        else:
            values[1] -= 0.1
        if values[1] < 0.1:
            values[1] = 0.1
        if values[1] > 3.0:
            values[1] = 3.0
        lighting.diffuse = values[1]
        
    elif i == 2:  # color
        if up:
            values[2] += 1
            if values[2] > 2:
                values[2] = 0
        else:
            values[2] -= 1
            if values[2] < 0:
                values[2] = 2
                
    elif i == 3:  # speed
        if up:
            values[3] += 2
        else:
            values[3] -= 2
        if values[3] < 2:
            values[3] = 2
        if values[3] > 100:
            values[3] = 100
            
    elif i == 4:  # width
        if up:
            values[4] += 100
        else:
            values[4] -= 100
        if values[4] < 200:
            values[4] = 200
        if values[4] > 1920:
            values[4] = 1920
        
    elif i == 5:  # height
        if up:
            values[5] += 100
        else:
            values[5] -= 100
        if values[5] < 200:
            values[5] = 200
        if values[5] > 1080:
            values[5] = 1080
        
    elif i == 6:  # resolution
        if up:
            values[6] += 25
        else:
            values[6] -= 25
        if values[6] < 50:
            values[6] = 50
        if values[6] > 500:
            values[6] = 500
        resolution = int(values[6])
        
    elif i == 7:  # shape
        if up:
            values[7] += 1
            if values[7] > 1:
                values[7] = 0
        else:
            values[7] -= 1
            if values[7] < 0:
                values[7] = 1
                
    elif i == 8:  # scene
        if up:
            values[8] += 1
            if values[8] > 2:
                values[8] = 0
        else:
            values[8] -= 1
            if values[8] < 0:
                values[8] = 2
        
        # Update scene variable
        if values[8] == 0:
            scene = mandlebulb
        elif values[8] == 1:
            scene = cube
        elif values[8] == 2:
            scene = circle

def draw_settings(draw_text_func):
    if not settings_on:
        return
        
    names = ["Power", "Light", "Color", "Speed", "W", "H", "Res", "Shape", "Scene"]
    color_names = ["Normal", "Warm", "Cool"]
    shape_names = ["Cube", "Sphere"]
    scene_names = ["Mandelbulb", "Cube", "Circle"]
    
    y = 700
    draw_text_func(50, y, "SETTINGS")
    y -= 25
    draw_text_func(50, y, "UP/DOWN: navigate, LEFT/RIGHT: change, TAB: close")
    y -= 30
    
    for i in range(9):  # 9 settings total
        if i == menu_pos:
            prefix = ">> "
        else:
            prefix = "   "
            
        name = names[i]
        val = values[i]
        
        if i == 2:
            val_text = color_names[int(val)]
        elif i == 7:
            val_text = shape_names[int(val)]
        elif i == 8:
            val_text = scene_names[int(val)]
        elif i == 1:
            val_text = str(round(val, 1))
        else:
            val_text = str(int(val))
            
        draw_text_func(60, y, prefix + name + ": " + val_text)
        y -= 25


