import sys, OpenGL, pygame
from pygame.locals import * 
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 


# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
TITLE = "Mesh"
vertices = [(0, 1, 0), (0, 0, 1), (-1, 0, 0), (1, 0, 0)]
edges = [(0, 1), (1, 3), (0, 2), (1, 2), (2, 3), (3, 0)]
faces = [(0, 1, 3), (0, 2, 1), (2, 3, 1), (0, 3, 2)]
black = [0.0, 0.0, 0.0]
white = [1.0, 1.0, 1.0]
red = [1.0, 0.0, 0.0]

def Tetrahedron():
    glBegin(GL_TRIANGLES)
    glColor3fv(red)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    glBegin(GL_LINES)
    glColor3fv(black)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (SCREEN_HEIGHT, SCREEN_WIDTH)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_RIGHT: 
                    glRotatef(10, 3, 1, 1)
                if event.key == K_LEFT:
                    glRotatef(-10, 3, 1, 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posn = pygame.mouse.get_pos()
                print(posn)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Tetrahedron()
        pygame.display.flip()

if __name__ == "__main__":
    main()

