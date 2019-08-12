import sys, math, copy, pygame, OpenGL, random
import numpy as np
from pygame.locals import * 
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
# from meshpy.tet import MeshInfo, build
random.seed()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WRITE_FILE = "test.node" # either .smesh or .node

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

    
# Rewrite .ele file without the removed tets after mesh segmentation
def writeEleFile(f, cdtMesh):
    lstTet = cdtMesh.tetrahedra
    length = len(cdtMesh.tetrahedra)
    f.write(str(length) + " 4 0\n")
    for i in range(0, length):
        f.write(str(i + 1) + ' ' + str(lstTet[i][0] + 1) + ' ' + str(cdtMesh.tetrahedra[i][1] + 1) + ' ' + str(cdtMesh.tetrahedra[i][2] + 1) + ' ' + str(cdtMesh.tetrahedra[i][3] + 1) + '\n')
    return 

# Export to .txt files
def exportToTxt(cdtMesh, surfaceMesh):
    name = raw_input("Export file for processing (.txt): ")
    f = open(name + ".txt", 'w')
    # f.write("# vertices, tetrahedra, winding nums of tetrahedra\n")

    # Vertices
    f.write(str(len(cdtMesh.vertices)) + '\n')
    for v in cdtMesh.vertices:
        f.write(str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n')
    
    # Faces (of surface mesh)
    f.write(str(len(surfaceMesh.faces)) + '\n')
    for face in surfaceMesh.faces:
        f.write(str(face[0])+ ' ' + str(face[1]) + ' ' + str(face[2]) + '\n')

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

# Find a new threshold based on the winding numbers
# Sort the tetrhedra according to that threshold
def refineTetList(tetrahedra, windingNums):
    # print windingNums # TEST
    newTets = []
    newWn = []
    avg = 0
    # Calculate average of windingNums:
    for wn in windingNums:
        avg += wn
    tempList = copy.copy(windingNums)
    avg = round(avg / len(windingNums), 2)
    med = np.median(tempList)
    # range = np.ptp(tempList)
    fiftyPercentile = np.percentile(tempList, 50)
    print "50th Percentile:", fiftyPercentile
    # print "Range:", range
    print "Median:", med
    print "Threshold (Average before):", avg # TEST
    # avg = round((med + avg) / 2, 2)
    print "New MedAverage:", avg # TEST
    if avg > .5 or avg < .3:
        avg = .5
    print "Threshold (Average After):", avg # TEST
    for i in range(0, len(windingNums)):
        if round(windingNums[i], 2) >= avg:
            newTets.append(tetrahedra[i])
            newWn.append(windingNums[i])
    return newTets, newWn


# Calculate winding number of the CM of each tet with respect to the input surface mesh
# Delete if it is "outside"
def segmentMesh(surfaceMesh, cdt):
    newTetList = []
    numSoFar = 0
    total = len(cdt.tetrahedra)
    for tet in cdt.tetrahedra:
        cm = calculateCenterMass(tet, cdt.vertices)
        w = windingNumber(surfaceMesh, cm)
        """if round(w, 2) >= .5:"""
        newTetList.append(tet)
        cdt.windingNumbers.append(w) # Winding num of tet can be found at the same index of tet in the tet list
        """else:
            print w"""
        """newTetList.append(tet)
        cdt.windingNumbers.append(w)"""
        """if round(w, 2) > .3 and round(w, 2) < .5 :
            print w # TEST
            print tet # TEST"""
        # print "Winding Number:", str(w) # TEST
        if numSoFar % 100 == 0 and numSoFar != 0: # TEST
            print numSoFar, "tetrahedra evaluated so far out of", total, "tetrahedra"
        numSoFar += 1
    # newTetList, cdt.windingNumbers = refineTetList(newTetList, cdt.windingNumbers)
    cdt.tetrahedra = newTetList
    return









# Get the bbox of an input mesh
def getBbox(vertices):
    length = len(vertices)
    # print "Length icoVertices:", str(length) # TEST
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
    bbox = []
    for x in xList:
        for y in yList:
            for z in zList:
                posn = [x, y, z]
                bbox.append(posn)
    return bbox


######################################## MAIN: ######################################################################
def main():
    objInput = raw_input("Mesh description (.obj): ")
    f = open(objInput + ".obj", 'r') # Input mesh description
    surfaceMesh = objGraph(f) # surfaceMesh is a Graph
    # faces = checkOrientation(faces, vertices) # CCW Orientation

    # printVertices(surfaceMesh.vertices) # TEST
    # printFaces(surfaceMesh.faces) # TEST

    # Find bbox:
    bbox = getBbox(surfaceMesh.vertices)
    for posn in bbox:
        surfaceMesh.vertices.append(posn)
    print "BBox: ", bbox # TEST
    """bbox.sort(key=lambda x: x[0])
    minX, maxX = bbox[0][0], bbox[7][0]
    bbox.sort(key=lambda x: x[1])
    minY, maxY = bbox[0][1], bbox[7][1]
    bbox.sort(key=lambda x: x[2])
    minZ, maxZ = bbox[0][2], bbox[7][2]
    for i in range(0, 300):
        x = random.uniform(-1000, 1000)
        y = random.uniform(-1000, 1000)
        z = random.uniform(-1000, 1000)
        while x <= maxX and x >= minX:
            x = random.uniform(-100, 100)
        while y <= maxY and y >= minY:
            y = random.uniform(-100, 100)
        while z <= maxZ and z >= minZ:
            z = random.uniform(-100, 100)
        surfaceMesh.vertices.append((x, y, z))"""
    # Generate CDT with node or surface file using tetgen
    # First use tetgen on a node file
    writeFile(WRITE_FILE, surfaceMesh, False)
    print "Data written to", WRITE_FILE
    


    # After user uses tetgen on the WRITE_FILE (e.g. tetgen test.node)
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

    # Export cdtMesh to .txt file for further processing
    exportToTxt(cdtMesh, surfaceMesh)
    # print "Positions:", str(cdtMesh.vertices)
    # print "Tetrahedral Elements:", str(cdtMesh.tetrahedra)

    # Render
    # render(cdtMesh)
    return 

    

if __name__ == "__main__":
    main()