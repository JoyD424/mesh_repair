import sys

# Read file
def getPosn(line):
    elem = line.split(' ')
    # print(elem) # TEST
    nums = []
    for x in elem:
        if x != 'v' and x != '\n' and x != ' ':
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
        if line[0] == '#': # Ignore comments
            continue
        elif line[0] == 'v':
            posn = getPosn(line)
            listVertices.append(posn)
        elif line[0] == 'f':
            face = getFace(line)
            listFaces.append(face)
    print(listVertices)
    print(listFaces)
if __name__ == "__main__":
    main()