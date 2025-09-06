from main import camera_pos, camera_dir, drone_pos, values, camera_speed, auto_pilot
from dronelight import update_drone_light
saved_state = None

def save_config():
    global saved_state
    saved_state = [
        camera_pos[:], camera_dir[:], drone_pos[:], values[:],
        camera_speed, auto_pilot
    ]
    print("Saved!")
    print(f"Camera: {camera_pos}")
    print(f"Drone: {drone_pos}")

def load_config():
    global saved_state, camera_pos, camera_dir, drone_pos, values, camera_speed, auto_pilot, resolution
    if not saved_state:
        print("Nothing Saved!")
        return
        
    camera_pos[:] = saved_state[0]
    camera_dir[:] = saved_state[1]
    drone_pos[:] = saved_state[2]
    values[:] = saved_state[3]
    camera_speed = saved_state[4]
    auto_pilot = saved_state[5]
    
    resolution = int(values[6])
    update_drone_light()
    print("Loaded!")