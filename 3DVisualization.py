import sys, math
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 

# Global variables
screen_width = 500
screen_height = 500
init_posnx = 400
init_posny = 150
title = "Window"
keyStates = []
# yLocation = 0.0
yRotationAngle = 0.0

# initialize keyStates (256 list bool) to false 
# None of the keys are pressed
def initializeKeyState():
    global keyStates
    for i in range(0, 256):
        keyStates.append(False)
    return 



# Reshape function
def reshape(width, height):
    glViewport(0, 0, int(width), int(height))
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    gluPerspective(60, float(width) / float(height), 1.0, 100.0)  
    glMatrixMode(GL_MODELVIEW)



# Handle key press events
# char, int, int --> None
# Use chr() to convert int to char
# Use ord() to convert char to int
def keyPressed(key, x, y):
    global keyStates
    intKey = ord(key)
    keyStates[intKey] = True
    return 



# Handle key release events
def keyReleased(key, x, y):
    global keyStates
    intKey = ord(key)
    keyStates[intKey] = False
    return 



# Event update when key is pressed
def keyOperations(yLocation, yRotationAngle):
    print keyStates[int(GLUT_KEY_LEFT)] # TEST
    if keyStates[int(GLUT_KEY_LEFT)]:
        yRotationAngle -= 5.0
        print yRotationAngle # TEST
    elif keyStates[int(GLUT_KEY_RIGHT)]:
        yRotationAngle += 5.0
    elif keyStates[int(GLUT_KEY_UP)]:
        yLocation -= .5
    elif keyStates[int(GLUT_KEY_DOWN)]:
        yLocation += .5
    return yLocation, yRotationAngle



# Display function
def display():
    # Access global variables
    # global yLocation
    global yRotationAngle

    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(1.0, 1.0, 1.0, 1.0) # rgba, a = transparency --> (0 = transparent)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    gluLookAt (0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glLoadIdentity()

    # Translation and rotation
    glTranslatef(0.0, 0.0, -5.0)
    # glTranslatef(0.0, yLocation, 0.0)

    glRotatef(yRotationAngle, 0.0, 1.0, 0.0)
    
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glutSolidCube(2.0)
    

    glutSwapBuffers()

    # Change rotation:
    yRotationAngle += 0.5
    if (yRotationAngle > 360.0):
        yRotationAngle -= 360.0
    return 



# Opens a window 
def render():
    # Access and change global variables
    # global yLocation
    global yRotationAngle

    # Initialize window 
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(screen_width, screen_height)
    glutInitWindowPosition(init_posnx, init_posny)
    glutCreateWindow(title)

    # Lighting 
    glEnable (GL_DEPTH_TEST)
    glEnable (GL_LIGHTING)
    glEnable (GL_LIGHT0)

    # Call display func
    glutDisplayFunc(display) 
    glutIdleFunc(display) 

    # Call reshape func
    glutReshapeFunc(reshape)

    # Check for keyboard events
    """glutKeyboardFunc(keyPressed)
    print "Event detected"
    yLocation, yRotationAngle = keyOperations(yLocation, yRotationAngle)
    glutKeyboardUpFunc(keyReleased)"""

    # Make sure window stays open until application quits
    glutPostRedisplay()
    glutMainLoop()

    return 



def main():
    initializeKeyState()
    render()
    return 



if __name__ == "__main__":
    main()