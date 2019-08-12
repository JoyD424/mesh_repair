import sys, random, math, pygame
from pygame.locals import *

# TEST
# Has a loop 
loop = [(227, 165), (220, 165), (208, 164), (197, 163), (186, 161), (178, 159), (161, 158), (150, 158), (140, 158), (130, 165), (122, 173), (113, 181), (111, 191), (110, 202), (116, 209), (123, 210), (135, 210), (150, 205), (157, 205), (166, 207), (173, 214), (174, 221), (172, 228), (164, 240), (150, 243), (133, 244), (116, 244), (100, 253), (87, 261), (78, 270), (77, 283), (77, 288), (86, 294), (105, 295), (125, 295), (143, 295), (155, 291), (166, 282), (174, 276), (184, 272), (192, 270), (206, 277), (206, 287), (205, 294), (200, 303), (188, 313), (176, 321), (159, 330), (152, 332), (135, 339), (119, 348), (111, 359), (107, 371), (96, 376), (92, 393), (85, 397), (90, 413), (108, 413), (123, 407), (142, 402), (158, 402), (167, 389), (185, 382), (196, 368), (211, 364), (221, 358), (239, 352), (253, 352), (275, 339), (294, 333), (299, 320), (306, 305), (305, 298), (295, 295), (279, 289), (267, 282), (256, 271), (253, 244), (266, 236), (276, 235), (285, 236), (293, 242), (296, 253), (296, 272),(292, 280), (284, 295), (273, 304), (267, 311), (262, 319), (263, 332), (275, 346), (289, 354), (300, 364), (312, 368), (322, 371), (338, 374), (357, 376), (372, 369), (384, 367), (391, 352), (391, 339), (381, 336), (369, 324), (368, 305), (372, 302), (388, 300), (395, 290), (401, 279), (405, 266), (399, 254), (391, 248), (379, 247), (369, 247), (353, 238), (343, 229), (334, 217), (329, 208), (330, 195), (338, 179), (336, 168), (327, 160), (316, 161), (298, 173), (295, 190), (277, 193), (269, 195), (257, 192), (257, 178), (266, 165), (273, 149), (279, 130), (278, 112), (270, 105), (257, 105),(240, 121), (238, 136), (237, 150), (233, 158)]


# To run: use python 2.7 (not python3)

# Initialize random
random.seed()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
RADIUS = 2 # radius of vertex (when rendering)
LINEWIDTH = 1 # thickness of edges (when rendering)

# Colors
red =  [255, 0, 0]
white = [255, 255, 255]
black = [0, 0, 0]

# Pygame initialize screen:
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Objects:

# A graph contains all edges and vertices 
class Graph:
    def __init__(self, listVertices, listEdges):
        self.edges = listEdges
        self.vertices = listVertices

# An edge contains a start and end vertex (directed line)
class Edge:
    def __init__(self, startVertex, endVertex):
        self.start = startVertex
        self.end = endVertex
    
    def drawEdge(self, color):
        pygame.draw.line(DISPLAYSURF, color, self.start.posn, self.end.posn, LINEWIDTH)
        return

# A vertex is a position
class Vertex:
    def __init__(self, x, y):
        self.posn = (x, y)

    def drawVertex(self, color):
        pygame.draw.circle(DISPLAYSURF, color, self.posn, RADIUS, 0)
        return

class Triangle:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def drawTriangle(self, color):
        lst = [self.x, self.y, self.z]
        pygame.draw.polygon(DISPLAYSURF, color, lst, 0)


# TESTING FUNCTIONS:
# Testing function, prints vertex coordinates
def printVertex(v):
    print("(" + str(v.posn[0]) + ", " + str(v.posn[1]) + ")")
    return

# Testing function, prints edge coordinates
def printEdge(e):
    print("[(" + str(e.start.posn[0]) + ", " + str(e.start.posn[1]) + "), " + "(" + str(e.end.posn[0]) + ", " + str(e.end.posn[1]) + ")]")
    return

# Testing function, prints list of vertices' coordinates
def printVertices(vList):
    for v in vList:
        printVertex(v)
    return

# Testing function, prints list of edges' coordinates
def printEdges(eList):
    for e in eList:
        printEdge(e)
    return


# COORDINATE CONVERSION FUNCTIONS: 
# THIS IS THE CORRECT CONVERSION FUNCTION...
# Convert from pygame coordinates to cartesian coordinates
# posn can be a tuple or a Vertex
def toCartesianCoordinates(posn):
    if isinstance(posn, Vertex):
        x, y = posn.posn[0], posn.posn[1]
    else:
        x, y, = posn[0], posn[1]
    newX = x - (SCREEN_WIDTH / 2)
    newY = -1 * (y - (SCREEN_HEIGHT / 2))
    return (newX, newY)

# Convert cartesian to pygame coordinates (top left corner in pygame is (0,0))
# posn can be a tuple or a Vertex
def toPygameCoordinates(posn):
    if isinstance(posn, Vertex):
        x, y = posn.posn[0], posn.posn[1]
    else:
        x, y, = posn[0], posn[1]
    newX = x + (SCREEN_WIDTH / 2)
    newY = (-1 * y) + (SCREEN_HEIGHT / 2)
    return (newX, newY)


# CALCULATION FUNCTIONS:
# Determine direction of arc formed by angle between the starting and end point w/ respect to a center point
# Assigns a (+) or (-) value to theta for CCW and CW direction, respectively 
# Input: tuple (x, y), NOT Vertex
def directionalize(startPoint, endPoint, centerPoint, theta):
    # c: integer value, determines direction of arc subtended by angle
    c = ((startPoint[0] - centerPoint[0]) * (endPoint[1] - centerPoint[1])) - ((startPoint[1] - centerPoint[1]) * (endPoint[0] - centerPoint[0]))
    if c > 0: #CW
        if theta > 0: 
            theta = theta * -1
    elif c < 0: #CCW
        if theta < 0:
            theta = theta * -1
    else:
        if theta != 0:
            theta = 0
    return theta

# Calculate distance btwn 2 points
# tuple -> int
def distance(posn1, posn2):
    deltaX = posn2[0] - posn1[0]
    deltaY = posn2[1] - posn1[1]
    d = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
    return d

# Calculates the angle created by the endpoints of an edge connected to a center point
# lenC is the distance beween the start and endpoints. Angle C is the angle opposing lenC. 
def calcAngle(startPoint, endPoint, centerPoint):
    lenA = distance(centerPoint, startPoint)
    lenB = distance(centerPoint, endPoint) 
    lenC = distance(startPoint, endPoint)
    # If any of the three input points are equal, the three points (2 distinct points)
    # are collinear, and the angle formed between them is 0
    if lenA == 0 or lenB == 0:
        return 0
    cosC = (math.pow(lenA, 2) + math.pow(lenB, 2) - math.pow(lenC, 2)) / (2 * lenA * lenB)
    # Prevents domain errors w/ arccos (might be better to use arctan);
    if cosC < -1 or cosC > 1:
        return 0
    angleC = math.acos(cosC) 
    return angleC

# Calculate the winding number at a point 
# Integrate around the curve (a polygon) with respect to the point
def windingNumber(graph, point):
    angleSum = 0.0 
    for edge in graph.edges: 
        theta = calcAngle(edge.start.posn, edge.end.posn, point)
        angleSum += directionalize(edge.start.posn, edge.end.posn, point, theta)
    finalNum = angleSum / (2 * math.pi)
    return finalNum


# INITIALIZATION OF DATA REPRESENTATION
# Generate one vertex (random coordinates) --> Pygame coordinate system
def generateVertex():
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    vertex = Vertex(x, y)
    return vertex

# Checks if a position is already in the list of positions 
# If posn is already in posns (list of posn), returns true.
def checkRepeatedPosn(posn, listPosn):
    for p in listPosn:
        if posn == p:
            return True
    return False


# Calculate polar angles that are formed by each position with 
# respect to the x-axis from the reference point
# Returns a list of angle coordinate pairs
def calculatePolarAngles(posns, referencePoint):
    # Calculate polar angle of a point w respect to the reference point
    def calculatePolar(posn):
        pointA = (referencePoint[0] + SCREEN_WIDTH, referencePoint[1])
        theta = calcAngle(pointA, posn, referencePoint)
        return theta

    def assignAngleToCoordinate(angle, posn):
        return (angle, posn)
    listAngles = map(calculatePolar, posns[1:])
    angleCoordinatePairs = map(assignAngleToCoordinate, listAngles, posns[1:])
    return angleCoordinatePairs

# Find the convex hull given a set of posns.
# Pygame Coordinates
def convexHull(listPosn):
    # Sorts posns by y-value, lowest to highest.
    # Returns the bottom point
    def findBottomPoint(posns):
        posns.sort(key=lambda x: x[1])
        numRepetitions = -1
        lowestY = posns[0][1]
        for posn in posns:
            if posn[1] == lowestY:
                numRepetitions += 1
            else:
                break
        if numRepetitions == 0:
            return posns[0]
        newList = posns[0:(numRepetitions + 1)]
        newList.sort()
        return newList[0] 
    
    # Determines if direction of edges so far points right (CW) or left (CCW)
    def orientation(start, center, end):
        val = ((start[0] - center[0]) * (end[1] - center[1])) - ((start[1] - center[1]) * (end[0] - center[0]))
        # Right
        if val > 0:
            return 1
        # Left:
        elif val < 0: 
            return 2
        return val # when val = 0

    # Locate the bottom coordinate (located most bottom-left out of all the other points), and use that as the reference point
    cartesianCoordinates = map(toCartesianCoordinates, listPosn)
    bottomPoint = findBottomPoint(cartesianCoordinates) # This also sorts cartesianCoordinates
    indexOfBottomPoint = cartesianCoordinates.index(bottomPoint)
    cartesianCoordinates[0], cartesianCoordinates[indexOfBottomPoint] = cartesianCoordinates[indexOfBottomPoint], cartesianCoordinates[0]

    # Calculate and sort polar angles of all other points with respect to the reference point
    angleCoordinatePairs = calculatePolarAngles(cartesianCoordinates, bottomPoint) # Returns the angle coordinate pairs of cartesianCoordinates[1:]
    angleCoordinatePairs.sort(key=lambda x: x[0])
    cartesianCoordinates = map(lambda x: x[1], angleCoordinatePairs)
    cartesianCoordinates.insert(0, bottomPoint)

    # Add first three coordinates to a stack, because they must be part of the final hull
    edgesSoFar = cartesianCoordinates[0:3]
    
    # Loop through all the coordinates
    # Reject points that make the edges-so-far turn right 
    # (i.e. add points to the edfesSoFar if they make the shape-so-far take a left turn)
    for i in range(3, len(cartesianCoordinates)):
        current = cartesianCoordinates[i]
        while (orientation(edgesSoFar[len(edgesSoFar) - 2], edgesSoFar[(len(edgesSoFar) - 1)], current) != 2): # next to top, top, current
            edgesSoFar.pop()
        edgesSoFar.append(current)

    # Return the finalized list of coordinates
    pyCoordinates = map(toPygameCoordinates, edgesSoFar)
    # pyCoordinates currently runs in the CW direction, so make sure that the directed vertices points CCW:
    pyCoordinates.reverse() # GET RID OF THIS AND THE OTHER REVERSE?
    return pyCoordinates


# Makes a Vertex from a Posn
def makeVertex(posn):
        newVertex = Vertex(posn[0], posn[1])
        return newVertex

# Generate list of n vertices for the polygon (no repeated vertices, random coordinates)
# Vertices must create a graph where the direction of the n-gon is oriented ccw with respect to point
# Pygame coordinate system
def generateListVertex():
    def generatePosn():
        """x = random.randint(0, 150)
        if x <= 90:
            (x, y) = (random.randint((SCREEN_WIDTH / 4), ((SCREEN_WIDTH / 4) + (SCREEN_WIDTH / 2))), random.randint((SCREEN_HEIGHT / 4), ((SCREEN_HEIGHT / 4) + (SCREEN_HEIGHT / 2))))
        else:
            (x, y) = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))"""
        # TEST: Limit space that points can be generated in 
        cstWidth = SCREEN_WIDTH / 10
        cstHeight = SCREEN_HEIGHT / 10
        (x, y) = (random.randint(cstWidth, SCREEN_WIDTH - cstWidth), random.randint(cstHeight, SCREEN_HEIGHT - cstHeight))
        return (x, y)

    n = random.randint(10, 40)
    # print("n = " + str(n)) # TEST
    posns = []
    while n > 0:
        newPosn = generatePosn()
        if not checkRepeatedPosn(newPosn, posns): # If the posn is not repeated, append to list of posns
            posns.append(newPosn) 
            n = n - 1
    # print("List Vertices: ") # TEST
    # printVertices(listVertices) # TEST

    # Generates convex polygon from random points
    posns = convexHull(posns)  
    vertices = map(makeVertex, posns)
    return vertices

# Generate list of edges based on the list of vertices
def generateEdges(vertices, isClosed):
    edges = []
    lenVertices = len(vertices)
    # print("List of Edges") # TEST
    i = 0
    while i < (lenVertices - 1):
        j = i + 1
        newEdge = Edge(vertices[i], vertices[j])
        edges.append(newEdge)
        i += 1
    if isClosed:
    # Create a closed polygon:
        lastEdge = Edge(vertices[lenVertices - 1], vertices[0])
        edges.append(lastEdge)
        # printEdges(edges) # TEST
    return edges

# Generate graph
def generateGraph(vertices, isClosed):
    edges = generateEdges(vertices, isClosed)
    graph = Graph(vertices, edges)
    return graph 


# PYGAME RELATED RENDERING FUNCTIONS:
# Return the rbg value of the winding number
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
        rgb = [255, 0, blueValue]
        # print(rgb) # TEST
    elif n > .5:
        n = n - .5
        greenValue = 255 - int(round(n / incrementValue(.5)))
        # print("Green value: " + str(greenValue)) # TEST
        rgb = [255, greenValue, 0]
    elif n > .25:
        n = n - .25
        redValue = int(round(n / incrementValue(.25)))
        rgb = [redValue, 255, 0]
    elif n > 0:
        blueValue = 255 - int(round(n / incrementValue(.25)))
        rgb = [0, 255, blueValue]
    elif n > -.5:
        greenValue = 255 + int(round(n / incrementValue(.5))) 
        rgb = [0, greenValue, 255]
    elif n >= -2:
        n = n + .5
        # print("N: " + str(n)) # TEST
        redValue = -1 * int(round(n / (1.5/123)))
        # print("RedValue: " + str(redValue)) # TEST
        rgb = [redValue, 0, 255]
        # print(rgb) # TEST
    else:
        print(n)
        print("ERROR: WINDING NUMBER NOT IN COLOR RANGE!")
        rgb = [0, 0, 0]
    return rgb

# Render colorful version (like synesthesia with winding numbers)
"""def render(graph):
    pygame.init()
    DISPLAYSURF.fill(white)
    # Fill in screen
    for x in range(0, SCREEN_WIDTH):
        for y in range(0, SCREEN_HEIGHT):
            coordinate = (x, y)
            w = windingNumber(graph, coordinate)
            # print(str(w)) # TEST
            color = assignRGBValue(w)
            # print(color) # TEST
            pygame.draw.circle(DISPLAYSURF, color, coordinate, RADIUS, 0)
    # Draw vertices
    for v in graph.vertices:
        v.drawVertex()
    # Draw edges
    for e in graph.edges:
        e.drawEdge()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
    return"""

# TEST RENDER: DRAW BBOX AND OPEN POLYGON
"""def renderTest(polygonGraph, bboxGrpah):
    pygame.init()
    DISPLAYSURF.fill(white)
    # Draw vertices
    for v in polygonGraph.vertices:
        v.drawVertex(black)
    for v in bboxGrpah.vertices:
        v.drawVertex(red)
    # Draw edges
    for e in polygonGraph.edges:
        e.drawEdge(black)
    for e in bboxGrpah.edges:
        e.drawEdge(red)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
    return"""

# Returns the centroid of a triangle in tuple (x, y) form
def findCentroid(triangle):
    x = (triangle.x[0] + triangle.y[0] + triangle.z[0]) / 3
    y = (triangle.x[1] + triangle.y[1] + triangle.z[1]) / 3
    centroid = (x, y)
    return centroid


# TEST RENDER 2
def renderTest(triangles, nodes, graph):
    mesh = []
    pygame.init()
    DISPLAYSURF.fill(white)
    # Draw vertices
    for v in nodes:
        v.drawVertex(black)
    # Draw triangles
    for t in triangles:
        centroid = findCentroid(t)
        windingNum = windingNumber(graph, centroid)
        if round(windingNum, 2) > .5 or round(windingNum, 2) < -.5: # Rounding might be a bit risky... think about a bigger
        # bounding box that doesn't intersect with any vertex or edge of the shape
            # print(str(windingNum)) TEST
            mesh.append(t)
        color = assignRGBValue(windingNum)
        t.drawTriangle(color)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
    return mesh

# Calculate the left/right/top/bottom-most points to create a square bounding box --> Graph
# Pygame coordinate system
def generateBbox(vertices):
    """length = len(vertices)
    # Sort by y-coordinate, smallest first
    vertices.sort(key=lambda x: x.posn[1])
    minY = vertices[0].posn[1]
    maxY = vertices[length - 1].posn[1]
    # Sort by x-coordinate, smallest first
    vertices.sort(key=lambda x: x.posn[0])
    minX = vertices[0].posn[0]
    maxX = vertices[length - 1].posn[0]
    # Return bbox coordinates... literally a square
    topLeft = (minX, minY)
    topRight = (maxX, minY)
    bottomLeft = (minX, maxY)
    bottomRight = (maxX, maxY)"""
    # Bbox is list Vertex
    vertices = map(makeVertex, [(SCREEN_WIDTH, 0), (0, 0), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)])
    bbox = generateGraph(vertices, True)
    return bbox

# FUNCTIONS FOR WRITING .NODE FILE
def writeVertices(f, vertices, length, startingIndex):
    index = 1
    while index <= length:
        v = vertices[index - 1]
        f.write(str(index + startingIndex) + " " + str(v.posn[0]) + " " + str(v.posn[1]) + "\n")
        index += 1
    return 

def modifyEdges(graph):
    def findVertex(v, vertices):
        i = 0
        length = len(vertices)
        while i < length:
            if vertices[i].posn == v.posn:
                break
            i += 1
        adjustedIndex = i + 1 # Adjusted index starts from 1 and goes to len
        return adjustedIndex
    newEdges = []
    for e in graph.edges:
        start = findVertex(e.start, graph.vertices)
        end = findVertex(e.end, graph.vertices)
        new = (start, end)
        newEdges.append(new)
    return newEdges

def writeEdges(f, graph, length, startingIndex):
    index = 1
    edges = modifyEdges(graph)
    while index <= length:
        e = edges[index - 1]
        startPoint = e[0]
        endPoint = e[1]
        f.write(str(index + startingIndex) + " " + str(startPoint) + " " + str(endPoint) + "\n")
        index += 1
    return

def writeToNode(inputGraph, bboxGraph):
    # Access file:
    nodeName = raw_input("File for export (.node): ") # name of test file
    f = open(nodeName, 'w')

    # First line 
    lenVInput = len(inputGraph.vertices)
    lenVBBox = len(bboxGraph.vertices)
    f.write(str(lenVInput + lenVBBox) + " " + "2 0 0\n") # No attributes, no boundary markers

    # Write vertices
    f.write("# Vertices: <current vertex num> <x> <y>\n") # Assumes no attributes and boundaries
    # Vertices for inputGraph
    f.write("# Vertices for open polygon\n")
    writeVertices(f, inputGraph.vertices, lenVInput, 0)
    f.write("# Vertices in bbox\n")
    writeVertices(f, bboxGraph.vertices, lenVBBox, lenVInput)

    # Write edges
    """lenEInput = len(inputGraph.edges)
    lenEBBox = len(bboxGraph.edges)
    f.write("# Edges: <# of edges> <# of boundary markers>\n")
    f.write(str(lenEBBox + lenEInput) + " 0\n")
    # f.write(str(lenEInput) + " 0\n")
    # Edges for inputGraph
    f.write("# Edges for open polygon\n")
    writeEdges(f, inputGraph, lenEInput, 0)
    # Edges for bboxGraph
    f.write("# Edges for bbox\n")
    writeEdges(f, bboxGraph, lenEBBox, lenEInput)

    # Write holes (none)
    f.write("# Holes (assume 0)\n")
    f.write("0")"""
    return

# Read .ele and .node files for a list of triangles
def readResultFiles():
    # Read nodes
    nodes = []
    nodeFile = raw_input(".node file: ")
    f = open(nodeFile, 'r')
    line1 = f.readline()
    lst = line1.split()
    len = int(lst[0]) # Number of nodes
    for i in range(0, len):
        line = f.readline()
        lst = line.split()
        x, y = int(lst[1]), int(lst[2])
        v = Vertex(x, y)
        nodes.append(v)
    # printVertices(nodes) TEST

    # Read edges
    triangles = []
    eleFile = raw_input(".ele file: ")
    f = open(eleFile, 'r')
    line1 = f.readline()
    lst = line1.split()
    len = int(lst[0]) # Number of triangles
    for i in range(0, len):
        line = f.readline()
        lst = line.split()
        x, y, z, = nodes[int(lst[1]) - 1].posn, nodes[int(lst[2]) - 1].posn, nodes[int(lst[3]) - 1].posn
        t = Triangle(x, y, z)
        triangles.append(t)
    return triangles, nodes


# MAIN:
def main(): 
    # Randomly deletes n edges from graph
    def takeOutEdges(graph, numEdges):
        for i in range(numEdges):
            index = random.randint(0, len(graph.edges) - 1)
            print(str(index))
            toRemove = graph.edges[index]
            graph.edges.remove(toRemove)
        return 
    # Randomly generated polygon
    """vertices = generateListVertex()
    vertices.reverse() # Ensure counterclockwise direction
    printVertices(vertices)
    inputGraph = generateGraph(vertices, False)
    printEdges(inputGraph.edges)
    bboxGraph = generateBbox(vertices)"""

    # INPUT TESTS
    vertices = []
    for v in loop:
        newV = Vertex(v[0], v[1])
        vertices.append(newV)
    inputGraph = generateGraph(vertices, True)
    print(str(len(inputGraph.edges))) # TEST
    takeOutEdges(inputGraph, 30)
    bboxGraph = generateBbox(vertices)
    printVertices(inputGraph.vertices) # TEST
    printEdges(inputGraph.edges) # TEST
    #printEdges(inputGraph.edges)
    # print(str(len(inputGraph.edges))) # TEST

    # Write graphs into a .node file
    writeToNode(inputGraph, bboxGraph)
    
    # After using triangle on the .node file, have to read 
    # in .ele and .node files to get the triangles
    triangles, nodes = readResultFiles()
    # TEST:
    mesh = renderTest(triangles, nodes, inputGraph)
    # render(graph)
    finalPosns = []
    for triangle in mesh:
        finalPosns.append(triangle.x)
        finalPosns.append(triangle.y)
        finalPosns.append(triangle.z)
    # print(finalPosns)
    # printVertices(nodes)
    # Find the winding number with respect to the inputGraph
    # of each triangle (from .ele and .node) --> evaluate
    # at barycenter of each triangle
    # Only accept triangles with w(p) > .5 as part of the polygon
    # Take the vertices of these triangles and find it's convex hull, should 
    # be the same as the vertices of inputGraph
    return 
    
# Run:
if __name__ == "__main__":
    main()