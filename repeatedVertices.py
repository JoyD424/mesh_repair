# Process an obj file for repeated vertices 
# Get rid of the repeats
# Change the faces that reference that vertex 
# Obj file should only have v and f types
# SHOULD USE THIS BEFORE RUNNING 3DMESHREPAIR.PY AND TETGEN


###################################### READING AND WRITING FUNCTIONS: ######################################
# Read vertices and faces from file
# Create list vertices and list faces
def getVandF(file):
    vertices = []
    faces = []
    contents = file.readlines()
    for line in contents:
        spliced = line.split()
        if len(spliced) != 0 and spliced[0] == 'v':
            vertex = (float(spliced[1]), float(spliced[2]), float(spliced[3]))
            vertices.append(vertex)
        elif len(spliced) != 0 and spliced[0] == 'f':
            face = (int(spliced[1]), int(spliced[2]), int(spliced[3]))
            faces.append(face)
    return vertices, faces


# Write to .obj file
def reviseObjFile(f, vertices, faces):
    # Vertices
    for vertex in vertices:
        f.write("v " + str(vertex[0]) + ' ' + str(vertex[1]) + ' ' + str(vertex[2]) + '\n')
    
    # Faces
    for face in faces:
        f.write("f " + str(face[0]) + ' ' + str(face[1]) + ' ' + str(face[2]) + '\n')
    return









###################################### RE-SORTING V AND F FUNCTIONS: ######################################
# Convert list of faces that point at a vertex into 
# a list of faces that directly stores each vertex
def convertFaces(vertices, faces):
    for i in range(0, len(faces)):
        faces[i] = (vertices[faces[i][0] - 1], vertices[faces[i][1] - 1], vertices[faces[i][2] - 1])
    return 


# Resort faces and vertices, removing repeats using a dict
# Dictionary of vertices (key = vertex, value = index)
def reSortVerticesAndFaces(vertices, faces):
    d = dict()
    newFaces = []
    newVertices = []

    # Fill in newFaces: pointer to vertices, pointer index starts at 1
    index = 1
    for face in (faces):
        face = list(face)
        for i in range(0, len(face)): 
            point = face[i]
            if d.has_key(point):
                face[i] = d[point]
            else:
                d[point] = index
                face[i] = index
                index += 1
        newFaces.append(face)

    # Fill in newVertices: all repeats removed, list form
    for key, value in sorted(d.iteritems(), key=lambda (k,v): (v,k)):
        newVertices.append(key)
    return newVertices, newFaces


def main():
    print("This program fixes an obj file with repeated vertices")
    name = raw_input("File to fix (.obj): ")
    f = open(name + ".obj", 'r')

    # Vertices index starts at 0, faces index starts at 1! 
    # Also, vertices and faces are turned into floats and ints, respectively
    initialVertices, initialFaces = getVandF(f)
    """print initialVertices
    print initialFaces
    print '\n\n\n'"""
    # Turns initialFaces into a list of faces that directly stores each vertex
    convertFaces(initialVertices, initialFaces) 
    """print initialVertices
    print initialFaces
    print '\n\n\n'"""
    # Fix initialVertices and initialFaces, removing repeats of vertices
    revisedVertices, revisedFaces = reSortVerticesAndFaces(initialVertices, initialFaces)
    """print revisedVertices
    print revisedFaces"""

    # Write to obj
    f = open(name + ".obj", 'w')
    reviseObjFile(f, revisedVertices, revisedFaces)
    return

if __name__ == "__main__":
    main()