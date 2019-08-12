import sys, OpenGL, pygame, math, copy
from pygame.locals import * 
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 


# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
TITLE = "Mesh"
"""vertices = [(0, 1, 0), (0, 0, 1), (-1, 0, 0), (1, 0, 0)]
edges = [(0, 1), (1, 3), (0, 2), (1, 2), (2, 3), (3, 0)]
faces = [(0, 1, 3), (0, 2, 1), (2, 3, 1), (0, 3, 2)]"""
"""icoVertices = [(0.0, -52.5731, 85.0651), (85.0651, 0.0, 52.5731), (85.0651, 0.0, -52.5731), (-85.0651, 0.0, -52.5731), (-85.0651, 0.0, 52.5731), (-52.5731, 85.0651, 0.0), (52.5731, 85.0651, 0.0), (52.5731, -85.0651, 0.0), (-52.5731, -85.0651, 0.0), (0.0, -52.5731, -85.0651), (0.0, 52.5731, -85.0651), (0.0, 52.5731, 85.0651)]
    icoTets = [(1, 0, 2, 7), (3, 5, 4, 0), (8, 3, 4, 0), (5, 4, 0, 11), (3, 5, 0, 10), (5, 0, 10, 6), (0, 5, 11, 6), (1, 0, 11, 6), (8, 3, 0, 9), (0, 3, 10, 9), (10, 0, 9, 2), (0, 10, 6, 2), (1, 0, 6, 2), (0, 9, 2, 7), (0, 8, 9, 7)]"""
"""icoVertices = [(-2.554035, 1.702084, -1.20239), (-4.703022, 0.060423, -2.763702), (-1.733211, 0.060424, -3.72867), (0.102254, 0.060411, -1.20239), (-1.733211, 0.060424,1.323889), (-4.703022, 0.060423, 0.358922), (-3.37486, -2.595906, -3.72867), (-0.405048, -2.595905, -2.763702), (-0.405048, -2.595905, 0.358922), (-3.37486, -2.595906, 1.323889), (-5.210325, -2.595893, -1.20239), (-2.554035, -4.237566, -1.20239), (-2.071571, 1.258554, -2.687289), (-3.817169, 1.258553, -2.1201), (-3.33471, 0.293608, -3.605013), (-5.080311, 0.293603, -1.20239), (-3.817169, 1.258553, -0.28468), (-0.99271, 1.258546, -1.20239), (-0.510233, 0.293603, -2.687294), (-2.071571, 1.258554, 0.282508), (-0.510233, 0.293603, 0.282513), (-3.33471, 0.293608, 1.200233), (-5.378511, -1.267741, -2.120103), (-5.378511, -1.267741, -0.284677), (-2.554035, -1.267741, -4.172215), (-4.299656, -1.267741, -3.605028), (0.27044, -1.267741, -2.120103), (-0.808415, -1.267741, -3.605028), (-0.808415, -1.267741, 1.200248), (0.27044, -1.267741, -0.284677), (-4.299656, -1.267741, 1.200248), (-2.554035, -1.267741, 1.767435), (-4.597837, -2.829086, -2.687294), (-1.773361, -2.82909, -3.605013), (-0.02776, -2.829085, -1.20239), (-1.773361, -2.82909, 1.200233), (-4.597837, -2.829086, 0.282513), (-3.0365, -3.794036, -2.687289), (-4.115361, -3.794028, -1.20239), (-1.290901, -3.794035, -2.1201), (-1.290901, -3.794035, -0.28468), (-3.0365, -3.794036, 0.282508)]
    icoTets = [(29, 16, 19, 0), (26, 34, 39, 7), (29, 40, 26, 34), (5, 21, 4, 19), (15, 1, 16, 5), (35, 8, 29, 28), (30, 5, 36, 23), (22, 1, 15, 23), (22, 10, 36, 23), (3, 0, 18, 26), (40, 26, 34, 39), (5, 9, 30, 36), (1, 13, 15, 16), (14, 13, 0, 12), (15, 1, 5, 23), (13, 16, 29, 0), (5, 9, 35, 31), (16, 5, 29, 19), (33, 26, 39, 7), (1, 22, 36, 23), (5, 1, 36, 23), (26, 40, 11, 39), (25, 1, 33, 24), (19, 20, 0, 17), (8, 40, 29, 34), (16, 21, 5, 19), (5, 21, 30, 31), (5, 9, 36, 35), (36, 9, 41, 35), (5, 36, 41, 35), (5, 21, 31, 4), (20, 4, 29, 28), (20, 29, 19, 0), (9, 5, 30, 31), (40, 35, 8, 29), (13, 1, 14, 27), (5, 4, 29, 19), (35, 5, 31, 28), (4, 20, 29, 19), (5, 35, 29, 28), (4, 5, 29, 28), (31, 5, 4, 28), (6, 25, 33, 24), (1, 26, 33, 27), (38, 37, 32, 11), (32, 6, 25, 33), (1, 16, 5, 29), (41, 5, 35, 29),(1, 13, 16, 29), (20, 0, 17, 3), (37, 6, 32, 33), (1, 22, 33, 11), (26, 1, 33, 11), (40, 29, 26, 11), (17, 0, 12, 18), (0, 17, 3, 18), (1, 13, 26, 27), (14, 2, 12, 27), (12, 18, 26, 27), (33, 1, 27, 24), (1, 25, 14, 24), (32, 37, 33, 11), (25, 1, 22, 33), (12, 2, 18, 27), (26, 33, 27, 7), (1, 14, 27, 24), (38, 36, 41, 11), (25, 32, 33, 11), (1, 13, 29, 26), (29, 13, 0, 26), (14, 2, 27, 24), (0, 12, 18, 26), (20, 0, 3, 26), (29, 20, 3, 26), (20, 29, 0, 26), (37, 33, 11, 39), (33, 26, 11, 39), (0, 12, 26, 27), (0, 14, 12, 27), (13, 14, 0, 27), (13, 0, 26, 27), (32, 25, 22, 11), (22, 25, 33, 11), (22, 1, 36, 11), (35, 41, 29, 11), (41, 35, 40, 11), (40, 35, 29, 11), (38, 32, 10, 11), (38, 10, 36, 11), (10, 22, 36, 11), (10, 32, 22, 11), (36, 5, 41, 11), (41, 5, 29, 11), (29, 1, 26, 11), (5, 1, 29, 11), (1, 5, 36, 11)]"""


black = [0.0, 0.0, 0.0]
white = [1.0, 1.0, 1.0]
red = [1.0, 0.0, 0.0]



########## Rendering ##########
# Color conversion:
# Get rbg value of the winding number --> convert to openGL
# Color scale:
# Pink (5) --> Red (1) --> Yellow (1/2) --> Green (1/4) --> Sky Blue (0) --> Navy (-1/2) --> Purple (-5)
# (255, 0, 255) <-- (255,0,0) <-- (255, 255, 0) <-- (0, 255, 0) <-- (0, 255, 255) <-- (0, 0, 255) <-- (123, 0, 255)
def assignRGBValue(n):
    def incrementValue(i):
        return i/255
    if n > 1:
        # print("N: " + str(n)) # TEST
        n = n - 1
        # print("IncrementValue: " + str(incrementValue(2.0))) # TEST
        blueValue = int(n / incrementValue(2.0))
        rgb = [1.0, 0.0, (blueValue / 255.0)]
        # print(rgb) # TEST
    elif n > .5:
        n = n - .5
        greenValue = 255 - int(round(n / incrementValue(.5)))
        # print("Green value: " + str(greenValue)) # TEST
        rgb = [1.0, float(greenValue / 255.0), 0.0]
    elif n > .25:
        n = n - .25
        redValue = int(round(n / incrementValue(.25)))
        rgb = [float(redValue / 255.0), 1.0, 0.0]
    elif n > 0:
        blueValue = 255 - int(round(n / incrementValue(.25)))
        rgb = [0.0, 1.0, float(blueValue / 255.0)]
    elif n > -.5:
        greenValue = 255 + int(round(n / incrementValue(.5))) 
        rgb = [0.0, float(greenValue / 255.0), 1.0]
    elif n >= -2:
        n = n + .5
        # print("N: " + str(n)) # TEST
        redValue = -1 * int(round(n / (1.5/123)))
        # print("RedValue: " + str(redValue)) # TEST
        rgb = [float(redValue / 255.0), 0.0, 1.0]
        # print(rgb) # TEST
    else:
        print(n)
        print("ERROR: WINDING NUMBER NOT IN COLOR RANGE!")
        rgb = [0.0, 0.0, 0.0]
    return rgb

# Returns a list of faces of the tetrahedron
def getFaces(tetrahedron):
    lst = [(tetrahedron[3], tetrahedron[0], tetrahedron[2]), (tetrahedron[0], tetrahedron[1], tetrahedron[2]), (tetrahedron[3], tetrahedron[2], tetrahedron[1]), (tetrahedron[3], tetrahedron[1], tetrahedron[0])]
    return lst 

# Draws the tet mesh as separate tetrahedrons 
# MAY NOT HAVE CONSISTENT ORIENTATION, HAS OVERLAPPING FACES OOPS
def Tetrahedron(icoVertices, icoTets, windingNums):
    glBegin(GL_TRIANGLES)
    listFaces = []
    index = 0
    for t in icoTets:
        color = assignRGBValue(windingNums[index])
        # print color # TEST
        glColor3fv(color)
        faces = getFaces(t)
        for face in faces:
            listFaces.append(face)
            for vertex in face:
                glVertex3fv(icoVertices[vertex])
        index += 1
    glEnd()
    glBegin(GL_LINES)
    glColor3fv(black)
    for face in listFaces:
        edges = [(face[0], face[1]), (face[1], face[2]), (face[0], face[2])]
        for e in edges:
            glVertex3fv(icoVertices[e[0]])
            glVertex3fv(icoVertices[e[1]])
    glEnd()
    return 

# Draws the bbox of the tet mesh
def BBox(bbox):
    squares = [(2, 3), (3, 1), (1, 0), (0, 2), (1, 5), (5, 4), (4, 0), (0, 1), (5, 1), (1, 3), (3, 7), (7, 5), (4, 5), (5, 7), (7, 6), (6, 4), (2, 0), (0, 4), (4, 6), (6, 2), (7, 3), (3, 2), (2, 6), (6, 7)]
    glBegin(GL_LINES)
    glColor3fv(black)
    for edge in squares:
        glVertex3fv(bbox[edge[0]])
        glVertex3fv(bbox[edge[1]])
    glEnd()
    return



########### SHAPE PROCESSING ###########
# Takes in a list of max and mins 
# Translates the original list of postions to origin
def translateToOrigin(xList, yList, zList, vertices):
    # print(vertices) # TEST
    bbox = []
    for x in xList:
        for y in yList:
            for z in zList:
                posn = [x, y, z]
                bbox.append(posn)
    # print(bbox) # TEST 
    # Find centroid of bbox
    bbox.sort(key=lambda x: x[0])
    centerX = bbox[0][0] + ((bbox[7][0] - bbox[0][0]) / 2)
    bbox.sort(key=lambda x: x[1])
    centerY = bbox[0][1] + ((bbox[7][1] - bbox[0][1]) / 2)
    bbox.sort(key=lambda x: x[2])
    centerZ = bbox[0][2] + ((bbox[7][2] - bbox[0][2]) / 2)
    # print "Centroid:", (centerX, centerY, centerZ) # TEST
    # Translate everything in the vertices list to origin
    # centered around the centroid of bbox
    vertices = map(lambda x: (x[0] - centerX, x[1] - centerY, x[2] - centerZ), vertices)
    # print(vertices) #TEST
    bbox = map(lambda x: (x[0] - centerX, x[1] - centerY, x[2] - centerZ), bbox)
    return bbox, vertices
    
# Scale the list of vertices so that it fits in a 10x10x10 box
def scale(bbox, vertices, xList, yList, zList):
    # print "Bbox:", bbox # TEST
    # print "Vertices:", vertices # TEST
    # Find the scaling factor 
    list = [xList[0], xList[1], yList[0], yList[1], zList[0], zList[1]]
    list.sort(key=lambda x: abs(x), reverse=True)
    parse = str(abs(list[0]))
    # print parse # TEST
    numBeforePeriod = 0
    for char in parse:
        if char == '.':
            break
        numBeforePeriod += 1
    scaleFactor = math.pow(.1, numBeforePeriod - 1)
    # print "Scale Factor:", scaleFactor # TEST
    vertices = map(lambda x: (x[0] * scaleFactor, x[1] * scaleFactor, x[2] * scaleFactor), vertices)
    bbox = map(lambda x: (x[0] * scaleFactor, x[1] * scaleFactor, x[2] * scaleFactor), bbox)
    return bbox, vertices

# Fit mesh to screen by applying transformations
def processShape(icoVertices):
    length = len(icoVertices)
    # print "Length icoVertices:", str(length) # TEST
    vertices = copy.copy(icoVertices)
    # print vertices # TEST
    icoVertices.sort(key=lambda x: x[1])
    # print vertices # TEST
    yList = (icoVertices[length - 1][1], icoVertices[0][1])
    icoVertices.sort(key=lambda x: x[0], reverse=True)
    xList = (icoVertices[length - 1][0], icoVertices[0][0])
    icoVertices.sort(key=lambda x: x[2], reverse=True)
    zList = (icoVertices[length - 1][2], icoVertices[0][2])
    # print xList, yList, zList # TEST
    # print vertices # TEST
    bbox, vertices = translateToOrigin(xList, yList, zList, vertices)
    # print(vertices) # TEST
    # print(bbox) # TEST
    bbox, vertices = scale(bbox, vertices, xList, yList, zList)
    # bbox = [] # TEST
    return bbox, vertices

def readTxtFile(f):
    # Process vertices
    vertices = []
    len = f.readline()
    for i in range(0, int(len)):
        posn = f.readline().split()
        p = (float(posn[0]), float(posn[1]), float(posn[2]))
        vertices.append(p)
    # print vertices # TEST
    
    # Process faces
    faces = []
    len = len = int(f.readline())
    for i in range(0, len):
        faceLst = f.readline().split()
        face = (int(faceLst[0]), int(faceLst[1]), int(faceLst[2]))
        faces.append(face)
    # print faces # TEST

    # Process tetrahedra
    tet = []
    len = int(f.readline())
    for i in range(0, len):
        t = f.readline().split()
        index = (int(t[0]), int(t[1]), int(t[2]), int(t[3]))
        tet.append(index)
    # print tet # TEST

    # Process winding numbers
    w = []
    len = int(f.readline())
    for i in range(0, len):
        winding = f.readline()
        w.append(float(winding))
    # print w # TEST
    
    return vertices, tet, faces, w




def main():
    # Get mesh info 
    name = raw_input("Mesh info (.txt): ")
    f = open(name + ".txt", 'r')
    icoVertices, icoTets, faces, windingNums = readTxtFile(f)

    pygame.init()
    display = (SCREEN_HEIGHT, SCREEN_WIDTH)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    # glTranslatef(0.0,0.0, -3) for monkey.test
    glTranslatef(0.0,0.0, -3)
    # Process shape (fit within a 10 by 10 cube, translate to origin)
    bbox, vertices = processShape(icoVertices)
    # print(vertices) # TEST
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_DOWN: 
                    glRotatef(-20, 0, 0, 0)
                elif event.key == K_UP:
                    glRotatef(20, 0, 0, 0)
                elif event.key == K_RIGHT:
                    glRotatef(20, 0, 1, 0)
                elif event.key == K_LEFT:
                    glRotatef(-20, 0, 1, 0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            Tetrahedron(vertices, icoTets, windingNums)
            BBox(bbox)
            pygame.display.flip()

if __name__ == "__main__":
    main()