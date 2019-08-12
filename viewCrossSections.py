import sys, math, pygame, OpenGL, copy
from pygame.locals import * 
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Basic Colors
black = [0.0, 0.0, 0.0]
white = [1.0, 1.0, 1.0]
red = [1.0, 0.0, 0.0]

############################################ CLASS DEFINITIONS: ############################################
class Graph:
    def __init__(self, listVertices, listFaces, listTetrahedra, listWindingNums):
        self.vertices = listVertices
        self.faces = listFaces # a face contains 3 elements, each pointing to an index in listVertices. Faces are triangles, CCW orientation
        self.tetrahedra = listTetrahedra # a tetrahedra contains 4 elements, each an index for listVertices. 
        self.windingNumbers = listWindingNums # Calculated winding number corresponding to each tetrahedra in th elist of tetrahedra

class Instance:
    def __init__(self, occurences, w):
        self.occurences = occurences
        self.windingNum = w

############################################ READING FUNCTIONS: ############################################
# Process txt file with mesh description
# (vertices, tetrahedra, and winding numbers)
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



#################### FIND EXTERIOR FACES: ####################
# Find all the faces of a tetrahedron 
def getFaces(tetrahedron):
    lst = [(int(tetrahedron[3]), int(tetrahedron[0]), int(tetrahedron[2])), (int(tetrahedron[0]), int(tetrahedron[1]), int(tetrahedron[2])), (int(tetrahedron[3]), int(tetrahedron[2]), int(tetrahedron[1])), (int(tetrahedron[3]), int(tetrahedron[1]), int(tetrahedron[0]))]
    return lst

# Create a dictionary (key = normalized face, value = Instance)
def createDictionary(faces, winding):
    d = dict()
    for f in faces:
        # print f # TEST
        f = list(f)
        f.sort()
        f = tuple(f)
        if d.has_key(f):
            d[f].occurences += 1
        else:
            d[f].occurences = 1
            d[f].windingNum = winding
    return d

def exteriorFaces(elems, windingNums):
    d = dict()
    index = 0
    for tet in elems:
        facesOfTet = getFaces(tet)
        for f in facesOfTet:
            # print f # TEST
            f = list(f)
            f.sort()
            f = tuple(f)
            if d.has_key(f):
                d[f].occurences += 1
            else:
                d[f] = Instance(1, windingNums[index])
        index += 1

    repairedFaces = []
    wn = []
    for key, val in d.iteritems():
        if val.occurences == 1:
            repairedFaces.append(key)
            wn.append(val.windingNum)
            
    return repairedFaces, wn









############################################ SHAPE PROCESSING ############################################
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

# Calculate the center of mass of a tetrahedra of the CDT
def calculateCenterMass(t, vertices):
    v1 = vertices[t[0]]
    v2 = vertices[t[1]]
    v3 = vertices[t[2]]
    v4 = vertices[t[3]]
    x = (v1[0] + v2[0] + v3[0] + v4[0]) / 4
    y = (v1[1] + v2[1] + v3[1] + v4[1]) / 4
    z = (v1[2] + v2[2] + v3[2] + v4[2]) / 4
    return (x, y, z)

# DEFAULT: Get rid of tets with +z coordinate
# ELSE: cuts along any axis
def sortTets(cdtTets, processedVertices, windingNums, cutOff, threshold):
    """tetList = []
    wnList = []
    index = 0
    for t in cdtTets:
        cm = calculateCenterMass(t, processedVertices)
        # Z-axis: if cm[2] <= cutOff:
        # X-axis: if cm[0] <= cutOff:
        # if cm[1] <= cutOff: # Y-axis
        if cm[2] <= cutOff:
            tetList.append(t)
            wnList.append(windingNums[index])
        index += 1"""
    tetList = []
    wnList = []
    index = 0
    for t in cdtTets:
        cm = calculateCenterMass(t, processedVertices)
        # Z-axis: if cm[2] <= cutOff:
        # X-axis: if cm[0] <= cutOff:
        # if cm[1] <= cutOff: # Y-axis
        if cm[2] <= cutOff:
            tetList.append(t)
            wnList.append(windingNums[index])
        elif windingNums[index] >= threshold:
            tetList.append(t)
            wnList.append(windingNums[index])
        index += 1
    return tetList, wnList









######################################## RENDERING FUNCTIONS: ########################################
# Calculate Distance
def distance(posn1, posn2):
    dist = math.sqrt(math.pow(posn2[0] - posn1[0], 2) + math.pow(posn2[1] - posn1[1], 2) + math.pow(posn2[2] - posn1[2], 2))
    return dist

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
        blueValue = int(n / incrementValue(1.0))
        rgb = [1.0, 0.0, (blueValue / 255.0)]
        # print(rgb) # TEST
    elif n > .5:
        n = n - .5
        greenValue = 255 - int(round(n / incrementValue(.5)))
        # print("Green value: " + str(greenValue)) # TEST
        rgb = [1.0, float(greenValue / 255.0), 0.0]
        """print greenValue
        print float(greenValue / 255.0)"""
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
    elif n >= -1:
        n = n + .5
        # print("N: " + str(n)) # TEST
        redValue = -1 * int(round(n / (.5/123)))
        # print("RedValue: " + str(redValue)) # TEST
        rgb = [float(redValue / 255.0), 0.0, 1.0]
        # print(rgb) # TEST
    else:
        print(n)
        print("ERROR: WINDING NUMBER NOT IN COLOR RANGE!")
        rgb = [0.0, 0.0, 0.0]
    return rgb

# Returns a list of faces of the tetrahedron
def getFacesWN(tetrahedron):
    lst = [(tetrahedron[3], tetrahedron[0], tetrahedron[2]), (tetrahedron[0], tetrahedron[1], tetrahedron[2]), (tetrahedron[3], tetrahedron[2], tetrahedron[1]), (tetrahedron[3], tetrahedron[1], tetrahedron[0])]
    return lst 

# Draws the tet mesh as separate tetrahedrons 
# MAY NOT HAVE CONSISTENT ORIENTATION, HAS OVERLAPPING FACES OOPS
def Tetrahedron(vertices, faces, windingList): #isFirst):
    glBegin(GL_TRIANGLES)
    listFaces = []
    index = 0
    for f in faces:
        color = assignRGBValue(windingList[index])
        glColor3fv(color)
        listFaces.append(f)
        for vertex in f:
            glVertex3fv(vertices[vertex])
        index += 1
    glEnd()
    """glBegin(GL_LINES)
    glColor3fv(black)
    for face in listFaces:
        edges = [(face[0], face[1]), (face[1], face[2]), (face[0], face[2])]
        for e in edges:
            glVertex3fv(vertices[e[0]])
            glVertex3fv(vertices[e[1]])
    glEnd()"""
    return

"""# Draws the tet mesh as separate tetrahedrons 
# MAY NOT HAVE CONSISTENT ORIENTATION, HAS OVERLAPPING FACES OOPS
def Tetrahedron(vertices, tetrahedra, windingList):
    glBegin(GL_TRIANGLES)
    listFaces = []
    index = 0
    for t in tetrahedra:
        color = assignRGBValue(windingList[index])
        glColor3fv(color)
        faces = getFaces(t)
        for face in faces:
            listFaces.append(face)
            for vertex in face:
                glVertex3fv(vertices[vertex])
        index += 1
    glEnd()
    glBegin(GL_LINES)
    glColor3fv(black)
    for face in listFaces:
        edges = [(face[0], face[1]), (face[1], face[2]), (face[0], face[2])]
        for e in edges:
            glVertex3fv(vertices[e[0]])
            glVertex3fv(vertices[e[1]])
    glEnd()
    return""" 

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

# Visualization of winding number and mesh
def render(cdtMesh):
    
    ## ONLY RENDER THE MESH ITSELF:
    """index = 0
    tetrahedra = []
    wns = []
    for t in cdtMesh.tetrahedra:
        if cdtMesh.windingNumbers[index] >= .50:
            tetrahedra.append(t)
            wns.append(cdtMesh.windingNumbers[index])
        index += 1
    cdtMesh.tetrahedra = tetrahedra
    cdtMesh.windingNumbers = wns"""

    pygame.init()
    display = (SCREEN_HEIGHT, SCREEN_WIDTH)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("View + Cut Mesh")
    glClearColor(1.0, 1.0, 1.0, 0.0)
    
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    lightdiffuse = [1.0, 1.0, 1.0, 1.0]
    lightposition = [1.0, 1.0, 1.0, 1.0]
    lightambient = [0.30, 0.30, 0.30, 0.30]
    lightspecular = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightdiffuse)
    glLightfv(GL_LIGHT1, GL_POSITION, lightposition)
    glLightfv(GL_LIGHT1, GL_AMBIENT, lightambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, lightdiffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, lightspecular)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Process shape (fit within a 10 by 10 cube, translate to origin)
    bbox, vertices = processShape(cdtMesh.vertices)
    glTranslatef(0.0,0.0, -40)
    zLengthBbox = distance(bbox[0], bbox[4]) # depth of bbox for cutting along z-axis
    # xLengthBbox = distance(bbox[4], bbox[5])
    # yLengthBbox = distance(bbox[3], bbox[1])
    # print zLengthBbox # TEST
    # print "Render Vertices:", vertices
    # print "Render bbox:", bbox
    # print(vertices) # TEST

    # Process tets for exterior faces and corresponding winding numbers
    faces, windingNums = exteriorFaces(cdtMesh.tetrahedra, cdtMesh.windingNumbers)
    # isFirst = True
    count = 0
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
                elif event.key == K_SPACE:
                    # print count # TEST
                    cutOff = bbox[4][2] + count * -.01 * zLengthBbox
                    # cutOff = bbox[5][0] + count * -.01 * xLengthBbox
                    # cutOff = bbox[3][1] + count * -.01 * yLengthBbox
                    # print cutOff # TEST
                    tetrasToDisplay, newWindingNums = sortTets(cdtMesh.tetrahedra, vertices, cdtMesh.windingNumbers, cutOff, .38) # FOR TORUS
                    """cdtMesh.tetrahedra = tetrasToDisplay
                    cdtMesh.windingNumbers = newWindingNums"""
                    faces, windingNums = exteriorFaces(tetrasToDisplay, newWindingNums)
                    count += 1
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            Tetrahedron(vertices, faces, windingNums)
            """Tetrahedron(vertices, cdtMesh.tetrahedra, cdtMesh.windingNumbers)"""
            BBox(bbox)
            pygame.display.flip()
            # isFirst = False
    return









def main():
    # Process Mesh
    name = raw_input("Mesh info (.txt): ")
    f = open(name + ".txt", 'r')
    v, t, _, w = readTxtFile(f)
    cdtMesh = Graph(v, [], t, w)

    # Default view: cut plane along x-axis, i.e., only display tets
    # whose CM are along the negative z axis
    # _, vertices = processShape(cdtMesh.vertices)
    # tetrasToDisplay, newWindingNums = sortTets(cdtMesh.tetrahedra, vertices, cdtMesh.windingNumbers)

    # Rendering 
    # cdtMesh.vertices = vertices
    # cdtMesh.tetrahedra = tetrasToDisplay
    # cdtMesh.windingNumbers = newWindingNums
    render(cdtMesh)

    return

if __name__ == "__main__":
    main()