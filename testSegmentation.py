import sys, math, copy, pygame, OpenGL
import numpy as np

class Instance():
    def __init__(self, occurences, originalOrientation):
        self.occurences = occurences
        self.orientedFace = originalOrientation
        return 










    

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





#################### SEGMENT FUNCTIONS: ####################
def segment(tetrahedra, windingNumbers):
    avg = 0
    for w in windingNumbers:
        avg += w
    avg = round(avg / len(windingNumbers), 2)
    print "Average:", avg
    if avg < .3 or avg > .5:
        avg = .5
    print "Threshold:", avg
    index = 0
    tList = []
    wList = []
    for t in tetrahedra:
        if round(windingNumbers[index], 2) >= avg:
            tList.append(t)
            wList.append(windingNumbers[index])
        index += 1
    return tList, wList









#################### READ + WRITE FUNCTIONS: ####################
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

def writeEleFile(f, tetrahedra):
    lstTet = tetrahedra
    length = len(tetrahedra)
    f.write(str(length) + " 4 0\n")
    for i in range(0, length):
        f.write(str(i + 1) + ' ' + str(lstTet[i][0] + 1) + ' ' + str(tetrahedra[i][1] + 1) + ' ' + str(tetrahedra[i][2] + 1) + ' ' + str(tetrahedra[i][3] + 1) + '\n')
    return

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







def main():
    # Read mesh info
    name = raw_input("Mesh info (.txt): ")
    f = open(name + ".txt", 'r')
    _, tetrahedra, _, windingNumbers = readTxtFile(f)

    # Remove tetrahedra whose wn does not meet the threshold
    tetrahedra, windingNumbers = segment(tetrahedra, windingNumbers)

    # Rewrite .ele file 
    # "Fix" the .ele file (remove all the removed tets from .ele)
    outputFileName = raw_input(".ele and .node file: ")
    fEle = open(outputFileName + ".ele", 'w')
    writeEleFile(fEle, tetrahedra)
    print "Repaired tet mesh exported to", outputFileName + ".ele"

    # Export new winding numbers list
    fWindingNums = open("windingNumbers.txt", 'w')
    fWindingNums.write(str(len(windingNumbers)) + '\n')
    for wn in windingNumbers:
        fWindingNums.write(str(wn) + ',\n')
    print "Updated wn list exported to windingNumbers.txt"

    # Export into .obj file
    objOutputName = raw_input("Export file name (.obj): ")
    fOutput = open(objOutputName + ".obj", 'w')
    fNode = open(outputFileName + ".node", 'r')
    nodes = fNode.readlines()
    fEle = open(outputFileName + ".ele", 'r')
    ele = fEle.readlines()
    writeOutputObjFile(fOutput, nodes, ele)

    return 

if __name__ == "__main__":
    main()
    

    