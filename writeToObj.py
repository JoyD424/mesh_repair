import sys, math
import numpy as np
# Reads an .ele and .node file (outputs from 3DMeshRepair) 
# Writes as an obj file of vertices and faces
# Only keeps boundary faces
    
# CLASSES
class Graph():
    def __init__(self, listVertices, listFaces, listTetrahedra, listWindingNums):
        self.vertices = listVertices
        self.faces = listFaces # a face contains 3 elements, each pointing to an index in listVertices. Faces are triangles, CCW orientation
        self.tetrahedra = listTetrahedra # a tetrahedra contains 4 elements, each an index for listVertices. 
        self.windingNumbers = listWindingNums # Calculated winding number corresponding to each tetrahedra in th elist of tetrahedra
        return 


class Instance():
    def __init__(self, occurences, originalOrientation):
        self.occurences = occurences
        self.orientedFace = originalOrientation
        return 





"""######################################## GRAPH SEGMENTATION FUNCTIONS: ########################################
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
    # print len(vertices) # TEST
    w = 0
    # printFaces(surfaceMesh.faces) # TEST
    for face in surfaceMesh.faces:
        # print face # TEST
        # print vertices[505]
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
    return w"""









#################### FIND EXTERIOR FUNCTIONS: ####################
# Find all the faces of a tetrahedron 
def getFaces(tetrahedron):
    lst = [(int(tetrahedron[3]), int(tetrahedron[0]), int(tetrahedron[2])), (int(tetrahedron[0]), int(tetrahedron[1]), int(tetrahedron[2])), (int(tetrahedron[3]), int(tetrahedron[2]), int(tetrahedron[1])), (int(tetrahedron[3]), int(tetrahedron[1]), int(tetrahedron[0]))]
    return lst

# Create a dictionary (key = normalized face, value = Instance)
def createDictionary(faces):
    d = dict()
    for f in faces:
        # print f # TEST
        face = list(f)
        face.sort()
        face = tuple(f)
        if d.has_key(face):
            d[face] += 1
        else:
            d[face] = Instance(1, f)
    return d

def exteriorFaces(elems):
    faces = []
    for tet in elems[1:]:
        lst = tet.split()
        # print lst # TEST
        facesOfTet = getFaces(lst[1:])
        for f in facesOfTet:
            faces.append(f)
    dict = createDictionary(faces)
    repairedFaces = []
    for key, val in dict.iteritems():
        if val.occurences == 1:
            oriented = list(val.orientedFace)
            oriented.reverse()
            oriented = tuple(oriented)
            repairedFaces.append(oriented)
    return repairedFaces










"""######################### REORIENT TRIANGLES: ########################
# Returns the centroid of a triangle in tuple (x, y) form
def findCentroid(triangle, vertices):
    p1 = vertices[triangle[0] - 1]
    p2 = vertices[triangle[1] - 1]
    p3 = vertices[triangle[2] - 1]
    x = (p1[0] + p2[0] + p3[0]) / 3
    y = (p1[1] + p2[1] + p3[1]) / 3
    z = (p1[2] + p2[2] + p3[2]) / 3
    centroid = (x, y, z)
    return centroid

def testPoint(face, vertices):
    # print face # TEST
    p1, p2, p3 = np.array(vertices[face[0] - 1]), np.array(vertices[face[1] - 1]), np.array(vertices[face[2] - 1])
    d1 = p2 - p1
    d2 = p3 - p2
    d1Crossd2 = np.cross(d1, d2)
    distance = math.sqrt(pow(d1Crossd2[0], 2) + pow(d1Crossd2[1], 2) + pow(d1Crossd2[2], 2))
    normal = ((d1Crossd2[0] / distance) * .01, (d1Crossd2[1] / distance) * .01 , (d1Crossd2[2] / distance) * .01)
    centroid = findCentroid(face, vertices)
    testPoint = np.array(centroid) + normal
    return testPoint

def fixOrientation(face, graph):
    point = testPoint(face, graph.vertices)
    # print point # TEST
    wnAtNormal = windingNumber(graph, point)
    # Face is oriented incorrectly --> reverse 
    if round(wnAtNormal, 2) > .5:
        # print wnAtNormal
        # print face # TEST
        face = (face[2], face[1], face[0])
        # print new
    return face

def orient(meshFaces, graph):
    faces = []
    for face in meshFaces:
        face = fixOrientation(face, graph)
        faces.append(face)
    return faces""" 









####################################### READ AND WRITE: #######################################
"""def writeOutputObjFile(objFile, nodes, elems, graph):"""
def writeOutputObjFile(objFile, nodes, elems):
    # Write obj vertices:
    objFile.write("# Vertices\n")
    # print nodes[0]
    for node in nodes[1:]:
        lst = node.split()
        if lst[0] != '#':
            objFile.write("v " + lst[1] + ' ' + lst[2] + ' ' + lst[3] + '\n')
    
    # Write obj faces:
    # Only keep the exterior faces:
    faces = exteriorFaces(elems)
    # print faces # TEST
    
    # Orient all triangles:
    # orientedFaces = orient(faces, graph)
    # print orientedFaces # TEST
    objFile.write("# Faces\n")
    # for face in orientedFaces:
    for face in faces:
        objFile.write("f " + str(face[0]) + ' ' + str(face[1]) + ' ' + str(face[2]) + '\n')
    return 

# Read a .txt file for mesh info
def readTxtFile(f):
    # Process vertices
    vertices = []
    len = f.readline()
    for i in range(0, int(len)): 
        posn = f.readline().split()
        p = (float(posn[0]), float(posn[1]), float(posn[2]))
        vertices.append(p)
    # print vertices[int(len) - 1]
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








# MAIN: 
def main():
    """# Read txt file for mesh info
    name = raw_input("Mesh info (.txt): ")
    f = open(name + ".txt", 'r')
    vertices, tetrahedra, faces, windingNums = readTxtFile(f)
    graph = Graph(vertices, faces, tetrahedra, windingNums)"""

    # Export into .obj file
    objOutputName = raw_input("Export file name (.obj): ")
    outputFileName = raw_input("Node and ele file name: ")
    fOutput = open(objOutputName + ".obj", 'w')
    fNode = open(outputFileName + ".node", 'r')
    nodes = fNode.readlines()
    fEle = open(outputFileName + ".ele", 'r')
    ele = fEle.readlines()
    writeOutputObjFile(fOutput, nodes, ele)
    """writeOutputObjFile(fOutput, nodes, ele, graph)"""
    return

if __name__ == "__main__":
    main()