import sys, random, math, numpy
from pygame.locals import *


# Works with points on the inside/outside of a solid and (ALL) points incident 
# with the face of a solid
# DOES NOT WORK CORRECTLY WITH POINTS ON AN EDGE OR ON A VERTEX
# Winding number along the same edge is the same

# Test
POINT =  (-0.1, 0.8, -0.1)
# Inside:
#

# Edge points
# (-0.1, 0.9, -0.1)
# (.5, .5, .5)
# (0.5, 0.5, -0.5)
# (-0.5 ,0.5 , 0.5)
# (-0.5, 0.5, -0.5)
# Norm
def length(posn): 
    len = math.sqrt(math.pow(posn[0], 2) + math.pow(posn[1], 2) + math.pow(posn[2], 2))
    return len

# Dot product
"""def dot(posn1, posn2):
    dotProduct = (posn1[0] * posn2[0]) + (posn1[1] * posn2[1]) + (posn1[2] * posn2[2])
    return dotProduct"""

# Shift everything to be centered around Posn (located at origin)
def translateToOrigin(vertexPosns, posn):
    deltaX = posn[0]
    deltaY = posn[1]
    deltaZ = posn[2]
    posn = (posn[0] - deltaX, posn[1] - deltaY, posn[2] - deltaZ)
    vertexPosns = map(lambda x: (x[0] - deltaX, x[1] - deltaY, x[2] - deltaZ), vertexPosns)
    return vertexPosns, posn

# Read file
def getPosn(line):
    elem = line.split(' ')
    # print(elem) # TEST
    nums = []
    for x in elem:
        if x != 'v' and x != '\n' and x != ' ':
            # print(x) # TEST
            x = float(x)
            nums.append(x)
    # print(nums) # TEST
    if len(nums) == 3:
        posn = (nums[0], nums[1], nums[2])
    else:
        print("Each vertex should have 3 coordinates")
        print(nums)
    # print(posn) # TEST
    return posn

def getFace(line):
    elem = line.split(' ')
    # print(elem) # TEST
    nums = []
    for n in elem:
        if n != 'f' and n != '\n' and n != ' ':
            n = int(n) - 1
            nums.append(n)
    # print(nums) # TEST
    if len(nums) == 3:
        face = (nums[0], nums[1], nums[2])
    else:
        print("Error: each face should point to 3 vertices")
        print(nums)
    # print(face) # TEST
    return face

# Calculate dihedral angle between two faces sharing an edge. 
# p1, p2, p3 are vertices of one face, p2 and p3 are common to both faces
# q is the vertex of the other face
def dihedralAngle(p1, p2, p3, q):
    def unitVector(n, d):
        x = n[0] / d
        y = n[1] / d
        z = n[2] / d
        return (x, y, z)

    # Vector from p2 to p1
    q1 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    # Vector from p3 to p2
    q2 = (p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2])
    # Vector from a to p3
    q3 = (q[0] - p3[0], q[1] - p3[1], q[2] - p3[2])
    # Cross products
    q1Crossq2 = numpy.cross(q1, q2)
    q2Crossq3 = numpy.cross(q2, q3)
    # Normals
    n1 = unitVector(q1Crossq2, length(q1Crossq2))
    n2 = unitVector(q2Crossq3, length(q2Crossq3))
    # Orthogonal Unit vectors
    u3 = unitVector(q2, length(q2))
    u2 = numpy.cross(u3, n2)
    phi = math.atan2(numpy.dot(n1, u2), numpy.dot(n1,n2))
    solidAngle = 2 * phi
    return solidAngle

def main():
    # For test file:
    # REQUIREMENTS:
    # Each line must start w/ a 'v' followed by ' '
    # Enter individual coordinates (2 per line for 2D) with a space after EACH coordinate
    name = raw_input() # name of test file
    f = open(name, 'r')
    if f.mode == 'r':
        contents = f.readlines()
    listVertices = []
    listFaces = []
    for line in contents:
        # print(line) # TEST
        if line[0] == '#': # Ignore comments
            continue
        elif line[0] == 'v':
            posn = getPosn(line)
            listVertices.append(posn)
        elif line[0] == 'f':
            face = getFace(line)
            listFaces.append(face)
        
    vertices, posn = translateToOrigin(listVertices, POINT)

    # Using the formula (winding nums paper): 
    windNum = 0
    for face in listFaces:
        v1 = vertices[face[0]]
        v2 = vertices[face[1]]
        v3 = vertices[face[2]]
        arr = numpy.array([v1, v2, v3]) 
        # Calculate the triple scalar product of the 3 vertices
        numerator = numpy.linalg.det(arr)
        # From wikipedia and the winding numbers paper: 
        denom = (length(v1) * length(v2) * length(v3)) + (numpy.dot(v1, v2) * length(v3)) + (numpy.dot(v2, v3) * length(v1)) + (numpy.dot(v3, v1) * length(v2)) #(numpy.dot(v1, v3) * length(v2)) + (numpy.dot(v2, v3) * length(v1))
        # else: 
        angle = math.atan2(numerator, denom) * 2
        print("Solid Angle: " + str(angle))
        windNum += angle
    solidAngle = dihedralAngle((0, 1, 0), (-1, 0, 1), (1, 0, 1), (-1, 0, -1)) #dihedralAngle((1, 0, -1), (1, 0, 1), (-1, 0, -1), (-1, 0, 1))
    print(str(solidAngle))
    # windNum = (windNum + (2 * solidAngle))/ (4 * math.pi)
    windNum = (windNum)/ (4 * math.pi)
    
    print "WindNum:", str(windNum)

    
    return 

if __name__ == "__main__":
    main()