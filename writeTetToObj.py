import sys, math
import numpy as np
# Reads an .ele and .node file (outputs from 3DMeshRepair) 
# Writes as an obj file of vertices and faces
# Only keeps boundary faces








# Find all the faces of a tetrahedron 
def getFaces(tetrahedron):
    lst = [(int(tetrahedron[2]), int(tetrahedron[0]), int(tetrahedron[3])), (int(tetrahedron[2]), int(tetrahedron[1]), int(tetrahedron[0])), (int(tetrahedron[1]), int(tetrahedron[2]), int(tetrahedron[3])), (int(tetrahedron[0]), int(tetrahedron[1]), int(tetrahedron[3]))]
    return lst






####################################### READ AND WRITE: #######################################
def writeOutputObjFile(objFile, nodes, elems):
    # Write obj vertices:
    objFile.write("# Vertices\n")
    # print nodes[0]
    for node in nodes[1:]:
        lst = node.split()
        if lst[0] != '#':
            objFile.write("v " + lst[1] + ' ' + lst[2] + ' ' + lst[3] + '\n')
    
    # Write obj faces:
    for tet in elems[1:]:
        lst = tet.split()
        faces = getFaces(lst[1:])
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
    # Read txt file for mesh info
    """name = raw_input("Mesh info (.txt): ")
    f = open(name + ".txt", 'r')
    vertices, tetrahedra, _, windingNumbers = readTxtFile(f)
    tetrahedra = segment(tetrahedra, windingNumbers)"""
    """newTets = []
    newWinding = []
    for i in range(0, len(tetrahedra)):
        if windingNumbers[i] > .2:
            newTets.append(tetrahedra[i])
            newWinding.append(windingNumbers[i])
    tetrahedra = newTets
    windingNumbers = newWinding"""

    # Export into .obj file
    objOutputName = raw_input("Export file name (.obj): ")
    outputFileName = raw_input("Node and ele file: ")
    fOutput = open(objOutputName + ".obj", 'w')
    fNode = open(outputFileName + ".node", 'r')
    nodes = fNode.readlines()
    fEle = open(outputFileName + ".ele", 'r')
    ele = fEle.readlines()
    writeOutputObjFile(fOutput, nodes, ele)
    """writeOutputObjFile(fOutput, vertices, tetrahedra)"""
    """writeOutputObjFile(fOutput, nodes, ele, graph)"""
    return

if __name__ == "__main__":
    main()