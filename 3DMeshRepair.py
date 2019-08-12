import sys, math, copy, pygame, OpenGL
import numpy as np
from pygame.locals import * 
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
# from meshpy.tet import MeshInfo, build

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WRITE_FILE = "test" # either .smesh or .node

# Basic Colors
black = [0.0, 0.0, 0.0]
white = [1.0, 1.0, 1.0]
red = [1.0, 0.0, 0.0]


# Outline:
# Given a mesh description (vertices, faces)
# Use tetgen to generate a tetrahedral mesh of the vertices and the bounding box/convex hull/just the vertices? 
    # Is the convex hull equivalent to the surface mesh? Or is the convex hull just the vertices of the input?
        # FOR NOW JUST INPUT THE VERTICES OF THE INPUT MESH DESCRIPTION
    # Use the marker -fe
    # Maybe also use the marker -c 
    # Mesh description exports into .node (vertices), .ele (tetrahedra), .face (convex hull faces), and .edge (convex hull edges) files
# Turn files into something readable and useable
# For each tetrahedron
    # Calculate the centroid's coordinates, c
    # Calculate the generalized winding number at c with respect to the original mesh description (vertices, faces)
# Refine the CDT by rejecting tetrahedron with winding number < .5 (round to 2 or 3 digits)
# Update .ele, .edge, .face, .node files
# render the image










######################################## OBJECTS: ##################################################
# A graph contains all edges and vertices 
class Graph:
    def __init__(self, listVertices, listFaces, listTetrahedra, listWindingNums):
        self.vertices = listVertices
        self.faces = listFaces # a face contains 3 elements, each pointing to an index in listVertices. Faces are triangles, CCW orientation
        self.tetrahedra = listTetrahedra # a tetrahedra contains 4 elements, each an index for listVertices. 
        self.windingNumbers = listWindingNums # Calculated winding number corresponding to each tetrahedra in th elist of tetrahedra










######################################## TESTING FUNCTIONS: ########################################
# Testing function, prints coordinates
def printVertices(lstV):
    for v in lstV:
        print(v)
    return

# Testing function, prints faces
def printFaces(lstF):
    for f in lstF:
        print(f)
    return

# Testing function, prints tetrahedron
def printTetrahedra(lstT):
    for t in lstT:
        print(t)
    return 










######################################## READING FUNCTIONS ########################################
# Read .obj file, extract vertices and faces, create a graph, return graph
# file --> Graph
def objGraph(f):
    def checkInput(lst):
        if len(lst) != 4: # If the vertex isn't a 3D coordinate --> error
            print "Incorrect dimesions:" , lst
            sys.exit(1)
        return 
    contents = f.readlines()
    vertices, faces = [], []
    for line in contents:
        parsed = line.split()
        if len(parsed) == 0: 
            continue
        if parsed[0] == '#': # Ignore comments
            continue
        if parsed[0] == 'v': # Dealing with vertices
            checkInput(parsed)
            vertex = (float(parsed[1]), float(parsed[2]), float(parsed[3]))
            vertices.append(vertex)
        elif parsed[0] == 'f':
            checkInput(parsed)
            face = (int(parsed[1]) - 1, int(parsed[2]) - 1, int(parsed[3]) - 1)
            faces.append(face)
        # Ignore all other inputs (invalid)
    graph = Graph(vertices, faces, [], [])
    return graph

# Read a .node file for the vertices, and export into the graph.vertices
def readNodeFile(f, graph):
    fstLine = f.readline().split()
    lenList = int(fstLine[0])
    if int(fstLine[1]) != 3: # if the vertices are not 3D coordinates --> error
        print "Incorrect dimensions for vertices:", fstLine[1], "but should be 3"
        sys.exit(1)
    for i in range (0, lenList):
        line = f.readline().split()
        posn = (float(line[1]), float(line[2]), float(line[3]))
        graph.vertices.append(posn)
    return

# Read a .ele file for the tetrahedron, and export into graph.tetrahedron
def readEleFile(f, graph):
    fstLine = f.readline().split()
    lenList = int(fstLine[0])
    if int(fstLine[1]) != 4: # if the tetrahedra does not have 4 nodes --> error
        print "Incorrect dimensions for a tetrahedron:", fstLine[1], "but should be 4"
        sys.exit(1)
    for i in range (0, lenList):
        line = f.readline().split()
        tet = (int(line[1]) - 1, int(line[2]) - 1, int(line[3]) - 1, int(line[4]) - 1) # Each element in tuple corresponds to an index, indexes in this program start at 0
        graph.tetrahedra.append(tet)
    return  

# Read faces for convex hull
def readConvexHull(faceName):
    f = open(faceName + ".face", 'r')
    fst = f.readline()
    numFaces = fst.split()
    faces = []
    for i in range(0, int(numFaces[0])):
        lst = f.readline().split()
        face = (int(lst[1]) - 1, int(lst[2]) - 1, int(lst[3]) - 1)
        faces.append(face)
    return faces








######################################## WRITING FUNCTIONS ########################################
# Write to .node or .smesh file with this format:
def writeFile(fileName, graph, isSmesh):
    def writeVertices(f, vertices, length):
        index = 1
        while index <= length:
            v = vertices[index - 1]
            f.write(str(index) + " " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n")
            index += 1
        return

    # Only for .smesh files
    def writeFaces(f, faces, length):
        for face in faces:
            f.write("3 " + str(face[0] + 1) + " " + str(face[1] + 1) + " " + str(face[2] + 1) + "\n")

    f = open(fileName, 'w')
    # Vertices:
    lenVertices = len(graph.vertices)
    f.write(str(lenVertices) + " " + "3 0 0\n") # No attributes, no boundary markers
    writeVertices(f, graph.vertices, lenVertices)

    # Only for .poly file:
    if isSmesh:
        # Faces
        lenFaces = len(graph.faces)
        f.write(str(lenFaces) + " 0\n")
        writeFaces(f, graph.faces, lenFaces)
        # Write holes (none)
        f.write("0\n")
        f.write("0")
    return


# Read convex hull faces and add to .smesh file
def addFaceToFile(fileName, faceName, graph):
    def writeVertices(f, vertices, length):
        index = 1
        while index <= length:
            v = vertices[index - 1]
            f.write(str(index) + " " + str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n")
            index += 1
        return

    # Only for .smesh files
    def writeFaces(f, faces, length):
        for face in faces:
            f.write("3 " + str(face[0] + 1) + " " + str(face[1] + 1) + " " + str(face[2] + 1) + "\n")

    f = open(fileName + ".smesh", 'w')
    # Vertices:
    lenVertices = len(graph.vertices)
    f.write(str(lenVertices) + " " + "3 0 0\n") # No attributes, no boundary markers
    writeVertices(f, graph.vertices, lenVertices)
    
    # Faces:
    # .face convex hull
    faces = readConvexHull(faceName)
    lengthCH = len(faces)
    # graph faces:
    """lenFaces = len(graph.faces)"""
    # together:
    """f.write(str(lenFaces + lengthCH) + " 0\n")
    writeFaces(f, graph.faces, lenFaces)
    writeFaces(f, faces, lengthCH)"""
    f.write(str(lengthCH) + " 0\n")
    writeFaces(f, faces, lengthCH)

    
    # Write holes (none)
    f.write("0\n")
    f.write("0")
    return 
    
# Rewrite .ele file without the removed tets after mesh segmentation
def writeEleFile(f, cdtMesh):
    lstTet = cdtMesh.tetrahedra
    length = len(cdtMesh.tetrahedra)
    f.write(str(length) + " 4 0\n")
    for i in range(0, length):
        f.write(str(i + 1) + ' ' + str(lstTet[i][0] + 1) + ' ' + str(cdtMesh.tetrahedra[i][1] + 1) + ' ' + str(cdtMesh.tetrahedra[i][2] + 1) + ' ' + str(cdtMesh.tetrahedra[i][3] + 1) + '\n')
    return 

# Export to .txt files
def exportToTxt(cdtMesh):
    name = raw_input("Export file for processing (.txt): ")
    f = open(name + ".txt", 'w')
    # f.write("# vertices, tetrahedra, winding nums of tetrahedra\n")

    # Vertices
    f.write(str(len(cdtMesh.vertices)) + '\n')
    for v in cdtMesh.vertices:
        f.write(str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n')
    
    # Tets
    f.write(str(len(cdtMesh.tetrahedra)) + '\n')
    for t in cdtMesh.tetrahedra:
        f.write(str(t[0]) + ' ' + str(t[1]) + ' ' + str(t[2]) + ' ' + str(t[3]) + '\n')
    
    # Winding Nums
    f.write(str(len(cdtMesh.windingNumbers)) + '\n')
    for w in cdtMesh.windingNumbers:
        f.write(str(w) + '\n')
    print "Mesh info exported to", name + ".txt"
    return 









######################################## GRAPH SEGMENTATION FUNCTIONS: ########################################
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

# Norm of a 3D vector (fake vector here)
def length(posn): 
    len = math.sqrt(math.pow(posn[0], 2) + math.pow(posn[1], 2) + math.pow(posn[2], 2))
    return len

# Shift everything to be centered around Posn (located at origin)
def translateToOrigin(vertexPosns, posn):
    deltaX = posn[0]
    deltaY = posn[1]
    deltaZ = posn[2]
    posn = (posn[0] - deltaX, posn[1] - deltaY, posn[2] - deltaZ)
    vertexPosns = map(lambda x: (x[0] - deltaX, x[1] - deltaY, x[2] - deltaZ), vertexPosns)
    return vertexPosns


# Calculate the generalized winding number of a 3D coordinate with 
# respect to the surface mesh (input mesh description)
def windingNumber(surfaceMesh, posn):
    # TRANSLATE POSN TO ORIGIN AND ALSO SURFACE MESH 
    vertices = translateToOrigin(surfaceMesh.vertices, posn)
    w = 0
    # printFaces(surfaceMesh.faces) # TEST
    for face in surfaceMesh.faces:
        v1 = vertices[face[0]]
        v2 = vertices[face[1]]
        v3 = vertices[face[2]]
        arr = np.array([v1, v2, v3]) 
        # Calculate the triple scalar product of the 3 vertices
        tripleScalar = np.linalg.det(arr)
        # From wikipedia and the winding numbers paper: 
        denom = (length(v1) * length(v2) * length(v3)) + (np.dot(v1, v2) * length(v3)) + (np.dot(v2, v3) * length(v1)) + (np.dot(v3, v1) * length(v2)) 
        angle = math.atan2(tripleScalar, denom) * 2
        # print "Solid Angle:", str(angle) # TEST
        w += angle
    w = w / (4 * math.pi)
    return w

# Calculate winding number of the CM of each tet with respect to the input surface mesh
# Delete if it is "outside"
def segmentMesh(surfaceMesh, cdt):
    newTetList = []
    numSoFar = 0
    total = len(cdt.tetrahedra)
    for tet in cdt.tetrahedra:
        cm = calculateCenterMass(tet, cdt.vertices)
        w = windingNumber(surfaceMesh, cm)
        if round(w, 5) > .5:
            newTetList.append(tet)
            cdt.windingNumbers.append(w) # Winding num of tet can be found at the same index of tet in the tet list
        # else:
            # print w # TEST
            # print tet # TEST
        # print "Winding Number:", str(w) # TEST
        if numSoFar % 100 == 0 and numSoFar != 0: # TEST
            print numSoFar, "tetrahedra evaluated so far out of", total, "tetrahedra"
        numSoFar += 1
    cdt.tetrahedra = newTetList
    return









################################# SHAPE PROCESSING FOR RENDERING #################################
# Takes in a list of max and mins 
# Translates the original list of postions to origin
def translateMeshToOrigin(xList, yList, zList, processedVerticies):
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
    processedVerticies = map(lambda x: (x[0] - centerX, x[1] - centerY, x[2] - centerZ), processedVerticies)
    # print(vertices) #TEST
    bbox = map(lambda x: (x[0] - centerX, x[1] - centerY, x[2] - centerZ), bbox)
    return bbox, processedVerticies
    
# Scale the list of vertices so that it fits in a 10x10x10 box
def scale(bbox, processedVerticies, xList, yList, zList):
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
    processedVerticies = map(lambda x: (x[0] * scaleFactor, x[1] * scaleFactor, x[2] * scaleFactor), processedVerticies)
    bbox = map(lambda x: (x[0] * scaleFactor, x[1] * scaleFactor, x[2] * scaleFactor), bbox)
    return bbox, processedVerticies

# Fit mesh to screen by applying transformations
def processShape(vertices):
    length = len(vertices)
    # print "Length icoVertices:", str(length) # TEST
    processedVertices = copy.copy(vertices)
    temp = copy.copy(vertices)
    # print vertices # TEST
    temp.sort(key=lambda x: x[1])
    # print vertices # TEST
    yList = (temp[length - 1][1], temp[0][1])
    temp.sort(key=lambda x: x[0])
    xList = (temp[length - 1][0], temp[0][0])
    temp.sort(key=lambda x: x[2])
    zList = (temp[length - 1][2], temp[0][2])
    # print xList, yList, zList # TEST
    # print vertices # TEST
    bbox, processedVertices = translateMeshToOrigin(xList, yList, zList, processedVertices)
    # print(vertices) # TEST
    # print(bbox) # TEST
    bbox, processedVertices = scale(bbox, processedVertices, xList, yList, zList)
    # bbox = [] # TEST
    return bbox, processedVertices








######################################## RENDERING FUNCTIONS: ########################################
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
def Tetrahedron(vertices, tetrahedra, windingList, isFirst):
    glBegin(GL_TRIANGLES)
    listFaces = []
    index = 0
    for t in tetrahedra:
        color = assignRGBValue(windingList[index])
        """if isFirst: # TEST
            print color # TEST"""
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

# Visualization of winding number and mesh
def render(cdtMesh):
    pygame.init()
    display = (SCREEN_HEIGHT, SCREEN_WIDTH)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    # Process shape (fit within a 10 by 10 cube, translate to origin)
    bbox, vertices = processShape(cdtMesh.vertices)
    glTranslatef(0.0,0.0, -30)
    # print "Render Vertices:", vertices
    # print "Render bbox:", bbox
    # print(vertices) # TEST
    isFirst = True
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
            Tetrahedron(vertices, cdtMesh.tetrahedra, cdtMesh.windingNumbers, isFirst)
            BBox(bbox)
            pygame.display.flip()
            isFirst = False
    return




######################################## MAIN: ######################################################################
def main():
    objInput = raw_input("Mesh description (.obj): ")
    f = open(objInput + ".obj", 'r') # Input mesh description
    surfaceMesh = objGraph(f) # surfaceMesh is a Graph
    # faces = checkOrientation(faces, vertices) # CCW Orientation

    # printVertices(surfaceMesh.vertices) # TEST
    # printFaces(surfaceMesh.faces) # TEST

    # Generate CDT with meshpy:
    """mesh_info = MeshInfo()
    mesh_info.set_points(surfaceMesh.vertices)
    mesh_info.set_facets(surfaceMesh.faces)
    tetMesh = build(mesh_info) 
    tetMesh.save_elements("test.1")
    tetMesh.save_nodes("test.1")"""

    # Generate CDT with node or surface file using tetgen
    # First use tetgen on a node file
    writeFile(WRITE_FILE + ".node", surfaceMesh, False)
    print "Data written to", WRITE_FILE + ".node"

    # After meshing the surface mesh (e.g. test.smesh), read .face file for convex hull
    # Go back to test.smesh (or another input surface mesh)
    # Replace all the faces in test.smesh with the faces in the .face file (or maybe just add to end of file)
    faceFileName = raw_input("Tetgen output .face file: ") # "test"
    addFaceToFile(WRITE_FILE, faceFileName, surfaceMesh) # .smesh file
    


    # After user uses tetgen on the WRITE_FILE
    # Read the .ele, .node, and .face files (MAYBE ALSO .edge)
    cdtMesh = Graph([], [], [], [])
    outputFileName = raw_input("Output file: ")
    # Read .node:
    f = open(outputFileName + ".node", 'r')
    readNodeFile(f, cdtMesh)
    # printVertices(cdtMesh.vertices) # TEST
    # Read .ele:
    f = open(outputFileName + ".ele", 'r')
    readEleFile(f, cdtMesh)
    # printTetrahedra(cdtMesh.tetrahedra) # TEST THIS PART WORKS

    # "Fix" the CDT mesh
    segmentMesh(surfaceMesh, cdtMesh)

    # "Fix" the .ele file (remove all the removed tets from .ele)
    f = open(outputFileName + ".ele", 'w')
    writeEleFile(f, cdtMesh)
    print "Repaired tet mesh exported to", outputFileName + ".ele"
    printTetrahedra(cdtMesh.tetrahedra) # TEST PROBABLY DOESN"T WORK HERE

    # Export cdtMesh to .txt file for further processing
    exportToTxt(cdtMesh)
    # print "Positions:", str(cdtMesh.vertices)
    # print "Tetrahedral Elements:", str(cdtMesh.tetrahedra)

    # Render
    render(cdtMesh)
    return 

    

if __name__ == "__main__":
    main()