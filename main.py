from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os #for os.kill. mac fix for exitting
import signal

from sdf import *
from raymerch import raymerch, raygen
from time import time
from lighting import Lighting, LightSource

exit_flag = False


# Lighting variables
ls = LightSource((-100,-50,25))
lighting = Lighting(ambient=(.25,.25,.25))
lighting.addLightSource(ls)
orbit_speed=0.1
orbit_radius=8.0


fovY = 90
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423
fps = 0
ptime = time()
t0=time()
W, H = 700, 500
resolution=150


#Ishmam's department
def reset():
    # Camera-related variables
    global camera_pos, camera_dir, camera_speed, camera_radius, auto_pilot, yaw, pitch, orbit_radius, orbit_speed
    camera_pos=[1.0, -1.0, 2.0]
    # xyz didn't work so im using angles
    yaw=45     
    pitch=0    
    camera_speed=0
    auto_pilot = False
    #Autopilot zoom and speed control
    orbit_radius=8.0
    orbit_speed=0.6
    camera_radius=max(1.0, math.sqrt(camera_pos[0]**2 + camera_pos[1]**2 + camera_pos[2]**2))
    t0=time()

    update_camera() 

def update_camera():
    global camera_dir, yaw, pitch
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)

    #serial x,y,z
    camera_dir = [
        math.cos(rad_pitch) * math.cos(rad_yaw),   
        math.cos(rad_pitch) * math.sin(rad_yaw),   
        math.sin(rad_pitch)                        
    ]

def update_camera_position():
    global camera_pos, camera_dir, camera_speed, auto_pilot, orbit_radius, orbit_speed, camera_radius
    if auto_pilot:
        # Auto orbit
        t = time() - t0
        radius = max(0.5, orbit_radius)
        height = 2.0 + 1.0 * math.sin(0.2 * orbit_speed * t)

        camera_pos[0] = radius * math.sin(0.2 * orbit_speed * t)
        camera_pos[1] = radius * math.cos(0.2 * orbit_speed * t)
        camera_pos[2] = height

        # Look at the centre
        target = [0.0, 0.0, 0.0]
        dx = target[0] - camera_pos[0]
        dy = target[1] - camera_pos[1]
        dz = target[2] - camera_pos[2]
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        if length > 0:
            camera_dir[0] = dx/length
            camera_dir[1] = dy/length
            camera_dir[2] = dz/length

    else:
        # Manual (keep as you had it)
        camera_radius = max(1.0, camera_radius + camera_speed)
        rad_yaw = math.radians(yaw)
        rad_pitch = math.radians(pitch)

        camera_pos[0] = camera_radius * math.cos(rad_pitch) * math.cos(rad_yaw)
        camera_pos[1] = camera_radius * math.cos(rad_pitch) * math.sin(rad_yaw)
        camera_pos[2] = camera_radius * math.sin(rad_pitch)

        dx = -camera_pos[0]
        dy = -camera_pos[1]
        dz = -camera_pos[2]
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        if length != 0:
            camera_dir[0] = dx / length
            camera_dir[1] = dy / length
            camera_dir[2] = dz / length
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, W, 0, H)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, H-y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_shapes():

    glPushMatrix()  # Save the current matrix state
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 0)  
    glutSolidCube(60) # Take cube size as the parameter
    glTranslatef(0, 0, 100) 
    glColor3f(0, 1, 0)
    glutSolidCube(60) 

    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glTranslatef(100, 0, 100) 
    glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    glColor3f(0, 1, 1)
    glTranslatef(300, 0, 100) 
    gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

    glPopMatrix()  # Restore the previous matrix state



    
def keyboardListener(key, x, y):
    global auto_pilot, camera_speed, camera_dir, orbit_radius, orbit_speed, exit_flag, camera_radius
    if key == b'\x1b': #escape
        global exit_flag
        exit_flag = True
    if key == b'r': #reset
        reset()
    
    #Ishmam's camera controls
    #case 1: autopilot
    if key==b' ': 
        auto_pilot=not auto_pilot
    
    #Speed control when in manual mode
    if key == b'1': 
        camera_speed=max(0.0, camera_speed - 0.1)
        if not auto_pilot:
            camera_radius = max(1.0, camera_radius - 2.0) 
    if key == b'2': 
        camera_speed+=.1
        if not auto_pilot:
            camera_radius+=2.0

    #Auto pilot control radius
    if key==b'-':
        orbit_radius+=0.5
    if key==b'+':
        orbit_radius=orbit_radius-0.5
    #Speed control
    if key==b'[':
        orbit_speed=orbit_speed-0.05
    if key==b']':
        orbit_speed+=0.05


def specialKeyListener(key, x, y):
    global yaw, pitch

    #Ishmam's Controls
    #up, down, left, right
    if key == GLUT_KEY_UP:     
        pitch = min(89, pitch + 2)
    if key == GLUT_KEY_DOWN:   
        pitch = max(-89, pitch - 2)
    if key == GLUT_KEY_LEFT:   
        yaw -= 2
    if key == GLUT_KEY_RIGHT:  
        yaw += 2
    
    update_camera()
    
    

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
        # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        # # Right mouse button toggles camera tracking mode
        # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:


def getLookAtParams():
    x, y, z = camera_pos
    a, b, c = camera_dir
    return x, y, z, x + a, y + b, z + c, 0,0,1
        
def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, W/H, 0.1, 15000)
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    gluLookAt(*getLookAtParams())


def idle():
    if exit_flag: os.kill(os.getpid(), signal.SIGTERM)
    global ptime, fps
    ntime = time()
    fps = 1/(ntime-ptime)
    ptime = ntime
    update_camera_position()
    glutPostRedisplay()



points_n_color = [((0,0,0), (0,0,0)) for _ in range(resolution*resolution)]  # capture points and colors in each frame


cube = CubeSdf((60,60,60))
circle = CircleSdf(40)
mandlebulb = MandleBulbSdf()
scene =  mandlebulb
def render():
    origin = camera_pos
    i = 0
    for d in raygen(*getLookAtParams(), resx= resolution, resy=resolution):
        p = raymerch(origin, d, scene)
        points_n_color[i] = (p, scene.getColor())
        i += 1
    for y in range(resolution-1):
        for x in range(resolution-1):
            ps = []
            tl = points_n_color[y*resolution + x]
            if tl[0]: ps.append(tl)
            tr = points_n_color[y*resolution + x + 1]
            if tr[0]: ps.append(tr)
            br = points_n_color[(y+1)*resolution + x + 1]
            if br[0]: ps.append(br)
            bl = points_n_color[(y+1)*resolution + x]
            if bl[0]: ps.append(bl)
            l = len(ps)
            if l == 4:
                glBegin(GL_QUADS)
            elif l == 3:
                glBegin(GL_TRIANGLES)
            if l > 2:
                for p, c in ps:
                    li = lighting.apply(p,c,scene.getNormal(p),camera_pos)
                    glColor3f(*li);
                    glVertex3f(*p);
                glEnd()
            
                
def draw_rays():
    glBegin(GL_LINES)
    resolution = 25
    for i in range(resolution):
        for j in range(resolution):
            p = raymerch(camera_pos, (i/resolution-0.5,1,j/resolution-0.5), CircleSdf(10))
            glVertex3d(*camera_pos)
            glVertex3d(*p)
    glEnd()
def draw_ray_dir():
    glBegin(GL_LINES)
    origin = (0,-30,0)
    for dir in raygen(*origin, 0,0,0, 0,0,1):
        glVertex3f(*origin)
        glVertex3f(*vec3_add(origin,dir))
    glEnd()
def draw_grid():
        # Draw the grid (game floor)
    glBegin(GL_QUADS)
    
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)


    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glEnd()

def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, W, H)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # # Draw a random points
    # glPointSize(20)
    # glBegin(GL_POINTS)
    # glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    # glEnd()


    # Display game info text at a fixed screen position
    draw_text(10, 20, f"fps: {fps}")
    draw_text(10, 50, f"See how the position and variable change?: {rand_var}")
    draw_text(10, 80, f"Orbit radius: {orbit_radius}")   
    draw_text(10, 110, f"Orbit speed: {orbit_speed:.2f}")

    #draw_grid()
    render()
    #draw_rays()
    #draw_ray_dir()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()



def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(W, H)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    reset()

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
