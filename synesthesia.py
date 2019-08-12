import sys, random, pygame, math
import numpy as np
from pygame.locals import *

# To run: use python 2.7 (not python3)

# Initialize random
random.seed()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
RADIUS = 1 # radius of vertex (when rendering)
LINEWIDTH = 2 # thickness of edges (when rendering)

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
    
    def drawEdge(self):
        pygame.draw.line(DISPLAYSURF, black, self.start.posn, self.end.posn, LINEWIDTH)
        return

# A vertex is a position
class Vertex:
    def __init__(self, x, y):
        self.posn = (x, y)

    def drawVertex(self):
        # pygame.draw.circle(DISPLAYSURF, black, self.posn, RADIUS, 0)
        DISPLAYSURF.set_at(self.posn, black)
        return


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
def toCartesianCoordinates(posn):
    newX = posn[0] - (SCREEN_WIDTH / 2)
    newY = -1 * (posn[1] - (SCREEN_HEIGHT / 2))
    return (newX, newY)

# Convert cartesian to pygame coordinates (top left corner in pygame is (0,0))
def toPygameCoordinates(posn):
   newX = posn[0] + (SCREEN_WIDTH / 2)
   newY = (-1 * posn[1]) + (SCREEN_HEIGHT / 2)
   return (newX, newY)


# CALCULATION FUNCTIONS:
# Determine direction of arc formed by angle between the starting and end point w/ respect to a center point
# Assigns a (+) or (-) value to theta for CCW and CW direction, respectively 
# Input: tuple (x, y), NOT vertices
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

# Calculate distance btwn 2 points...distance formula
# tuple -> int
def distance(posn1, posn2):
    deltaX = posn2[0] - posn1[0]
    deltaY = posn2[1] - posn1[1]
    d = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
    return d

# Calculates the angle created by the endpoints of an edge connected to a center point
# lenC is the distance beween the start and endpoints. Angle C is the angle opposing lenC. 
def calcAngle(startPoint, endPoint, centerPoint):
    """def transformToOrigin(start, end, center):
        deltaX = center[0]
        deltaY = center[1]
        center = (center[0] - deltaX, center[1] - deltaY)
        start = (start[0] - deltaX, start[1] - deltaY)
        end = (end[0] - deltaX, end[1] - deltaY)
        return start, end, center"""
    lenA = distance(centerPoint, startPoint)
    lenB = distance(centerPoint, endPoint) 
    lenC = distance(startPoint, endPoint)
    # If any of the three input points are equal, the three points (2 distinct points)
    # are collinear, and the angle formed between them is 0
    if lenA == 0 or lenB == 0:
        # print("a: " + str(centerPoint))
        return 0
    cosC = (math.pow(lenA, 2) + math.pow(lenB, 2) - math.pow(lenC, 2)) / (2 * lenA * lenB)
    # Prevents domain errors w/ arccos (might be better to use arctan)
    # Domain errors might occur when points are collinear
    if cosC < -1 or cosC > 1:
        # print("b: " + str(centerPoint))
        return 0
    angleC = math.acos(cosC)
    """a = toCartesianCoordinates(startPoint)
    b = toCartesianCoordinates(endPoint)
    p = toCartesianCoordinates(centerPoint)
    a, b, p = transformToOrigin(a, b, p)
    det = (a[0] * b[1]) - (a[1] * b[0])
    dot = (a[0] * b[0]) + (a[1] * b[1])
    if dot == 0:
        print("b: " + str(centerPoint))
        return 0
    tan = det / dot
    angleC = math.atan(tan)"""
    return angleC

# Calculate the winding number at a point 
# Integrate around the curve (a polygon) with respect to the point
def windingNumber(graph, point):
    angleSum = 0.0 
    for edge in graph.edges: 
        theta = calcAngle(edge.start.posn, edge.end.posn, point)
        if calcAngle == -20: # TEST
            return -20 # TEST
        angleSum += directionalize(edge.start.posn, edge.end.posn, point, theta)
    finalNum = angleSum / (2 * math.pi)
    return finalNum


# INITIALIZATION OF DATA REPRESENTATION
# Generate one vertex (random coordinates)
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

# Calculate the max and min x and y coordinates in the graph
def calculateMaxAndMin(vertices):
    xCoordinates = map(lambda x: x.posn[0], vertices)
    yCoordinates = map(lambda x: x.posn[1], vertices)
    minX = min(xCoordinates)
    maxX = max(xCoordinates)
    minY = min(yCoordinates)
    maxY = max(yCoordinates)
    return minX, minY, maxX, maxY

# Generate a random point for calculating the winding number: w(point)
def generatePoint(minX, minY, maxX, maxY):
    x = random.randint(minX, maxX)
    y = random.randint(minY, maxY)
    return (x, y)

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
    return pyCoordinates


# Generate list of n vertices for the polygon (no repeated vertices, random coordinates)
# Vertices must create a graph where the direction of the n-gon is oriented ccw with respect to point
def generateListVertex():
    def generatePosn():
        x = random.randint(0, 100)
        if x <= 85:
            (x, y) = (random.randint((SCREEN_WIDTH / 4), ((SCREEN_WIDTH / 4) + (SCREEN_WIDTH / 2))), random.randint((SCREEN_HEIGHT / 4), ((SCREEN_HEIGHT / 4) + (SCREEN_HEIGHT / 2))))
        else:
            (x, y) = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        return (x, y)

    def makeVertex(posn):
        newVertex = Vertex(posn[0], posn[1])
        return newVertex

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
def generateEdges(vertices):
    edges = []
    lenVertices = len(vertices)
    # print("List of Edges") # TEST
    i = 0
    while i < (lenVertices - 1):
        j = i + 1
        newEdge = Edge(vertices[i], vertices[j])
        edges.append(newEdge)
        i += 1
    # Create a closed polygon:
    # lastEdge = Edge(vertices[lenVertices - 1], vertices[0])
    # edges.append(lastEdge)
    # printEdges(edges) # TEST
    return edges

# Generate graph
def generateGraph(vertices):
    edges = generateEdges(vertices)
    graph = Graph(vertices, edges)
    return graph 


# PYGAME RELATED RENDERING FUNCTIONS:
# Return the rbg value of the winding number
# Color scale:
# Pink (5) --> Red (1) --> Yellow (1/2) --> Green (1/4) --> Sky Blue (0) --> Navy (-1/2) --> Purple (-5)
# (255, 0, 255) <-- (255,0,0) <-- (255, 255, 0) <-- (0, 255, 0) <-- (0, 255, 255) <-- (0, 0, 255) <-- (123, 0, 255)
def assignRGBValue(n):
    # print n # TEST
    def incrementValue(i):
        return i/255
    if n == -20: # TEST 
        return [255, 0, 255] # TEST
    if n > 1:
        # print("N: " + str(n)) # TEST
        n = n - 1
        # print("IncrementValue: " + str(incrementValue(2.0))) # TEST
        blueValue = int(n / incrementValue(4.0))
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
def render(graph):
    pygame.init()
    pygame.display.set_caption("Open Spiral")
    DISPLAYSURF.fill(white)
    # Fill in screen
    for x in range(0, SCREEN_WIDTH):
        for y in range(0, SCREEN_HEIGHT):
            w = windingNumber(graph, (x, y))
            # print(str(w)) # TEST
            color = assignRGBValue(w)
            # print(color) # TEST
            coordinate = (x, y)
            # pygame.draw.circle(DISPLAYSURF, color, coordinate, RADIUS, 0)
            DISPLAYSURF.set_at(coordinate, color)
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
    return

# Read file
def getPosn(line):
    elem = line.split(' ')
    nums = []
    for x in elem:
        if x != 'v' and x != '\n' and x != ' ':
            x = int(x)
            nums.append(x)
    if len(nums) == 2:
        posn = (nums[0], nums[1])
    else:
        print("More than 2 ints in list nums!")
        print(nums)
    return posn

# MAIN:
def main(): 
    # Randomly generated polygon:
    vertices = generateListVertex()

    # For test file:
    # REQUIREMENTS:
    # Each line must start w/ a 'v' followed by ' '
    # Enter individual coordinates (2 per line for 2D) with a space after EACH coordinate
    """name = raw_input() # name of test file
    f = open(name, 'r')
    if f.mode == 'r':
        contents = f.readlines()
    shape = []
    for line in contents:
        if line[0] == '#': # Ignore comments
            continue
        elif line[0] == 'v':
            posn = getPosn(line)
            shape.append(posn)
    # print(shape) # TEST
    vs = map(toPygameCoordinates, shape)
    # print(vs) # TEST
    vertices = []
    for v in vs:
        vtx = Vertex(v[0], v[1])
        vertices.append(vtx)"""

    graph = generateGraph(vertices)
    render(graph)
    return
  

# Run:
if __name__ == "__main__":
    main()