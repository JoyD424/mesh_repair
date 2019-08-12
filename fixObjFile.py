import sys


def fixFile(f, contents):
    def isAcceptableLine(lst):
        if lst[0] == 'v' or lst[0] == 'f':
            return True
        return False
    def parseList(lst):
        for i in range(1, len(lst)):
            toParse = lst[i]
            for j in range(0, len(toParse)):
                if toParse[j] == '/':
                    toParse = toParse[0:j]
                    lst[i] = toParse
                    break
        return     
    for line in contents:
        # print line # TEST
        lineList = line.split()
        # print lineList # TEST
        if isAcceptableLine(lineList):
            # print "Accepted:", lineList # TEST
            parseList(lineList)
            f.write(lineList[0] + ' ' + lineList[1] + ' ' + lineList[2] + ' ' + lineList[3] + '\n')
    return 

def main():
    name = raw_input("Obj File: ")
    f = open(name + ".obj", 'r')
    contents = f.readlines()
    # print contents # TEST
    f = open(name + ".obj", 'w')
    fixFile(f, contents)
    return 


if __name__ == "__main__":
    main()