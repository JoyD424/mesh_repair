import sys, OpenGL, pygame
from pygame.locals import * 
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import *

# Test Case: Simple Pyramid
vertices = [(0, 1, 0), (1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1)]
edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 3), (1, 2), (2, 3), (3, 4), (4, 1)]
colors = [(1,0,0), (0,1,0), (0,0,1), (0,1,0), (1,1,1), (0,1,1), (1,0,0), (0,1,0), (0,0,1), (1,0,0), (1,1,1), (0,1,1)]
faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (4, 3, 1), (1, 3, 2)]

# Cube specifications
verticesC = [(.1, -.1, -.1), (.1, .1, -.1), (-.1, .1, -.1), (-.1, -.1, -.1), (.1, -.1, .1), (.1, .1, .1), (-.1, -.1, .1), (-.1, .1, .1)]
edgesC = [(0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7), (5,1), (5,4), (5,7)]
facesC = [(0,1,2,3), (3,2,7,6), (6,7,5,4), (4,5,1,0), (1,5,7,2), (4,0,3,6)]

def cube():
    glBegin(GL_QUADS)
    for face in facesC:
        x = 0
        for vertex in face:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticesC[vertex])
    glEnd()
    glBegin(GL_LINES)
    for edge in edgesC:
        for vertex in edge:
            glVertex3fv(verticesC[vertex])
    glEnd()

def mesh():
    glBegin(GL_TRIANGLES)
    for face in faces:
        x = 0
        for vertex in face:
            x+=1
            glColor3fv(colors[0])
            glVertex3fv(vertices[vertex])
    glEnd()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_RIGHT: 
                    # glRotatef(10, 3, 1, 1)
                    glRotatef(10, 0, 3, 0)
                elif event.key == K_LEFT:
                    glRotatef(-10, 0, 3, 0)
                elif event.key == K_UP:
                    glRotatef(-10, 3, 0, 0)
                elif event.key == K_DOWN:
                    glRotatef(10, 3, 0, 0)
        # Render a point
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        # cube()
        mesh()
        pygame.display.flip()

if __name__ == "__main__":
    main()