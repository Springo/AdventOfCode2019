def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


lines = readFile("d05input.txt")

vals_orig = [int(c) for c in lines[0].split(',')]
vals = vals_orig[:]

done = False
ind = 0
inp = 5
print(vals)

while not done:
    print(ind)
    print(vals[ind])
    com = vals[ind]
    strcom = str(com)
    for i in range(5 - len(strcom)):
        strcom = '0' + strcom

    op = int(strcom[-2:])

    v1 = None
    v2 = None
    v3 = None
    if op != 99:
        if strcom[2] == '0':
            v1 = vals[vals[ind + 1]]
        elif strcom[2] == '1':
            v1 = vals[ind + 1]
        else:
            v1 = None
    if op == 1 or op == 2 or op == 5 or op == 6 or op == 7 or op == 8:
        if strcom[1] == '0':
            v2 = vals[vals[ind + 2]]
        elif strcom[1] == '1':
            v2 = vals[ind + 2]
        else:
            v2 = None
    if op == 1 or op == 2 or op == 7 or op == 8:
        if strcom[0] == '0':
            v3 = vals[vals[ind + 3]]
        elif strcom[0] == '1':
            v3 = vals[ind + 3]
        else:
            v3 = None

    if op == 1:
        vals[vals[ind + 3]] = v1 + v2
        ind += 4
    elif op == 2:
        vals[vals[ind + 3]] = v1 * v2
        ind += 4
    elif op == 3:
        vals[vals[ind + 1]] = inp
        ind += 2
    elif op == 4:
        print(v1)
        ind += 2
    elif op == 5:
        if v1 != 0:
            ind = v2
        else:
            ind += 3
    elif op == 6:
        if v1 == 0:
            ind = v2
        else:
            ind += 3
    elif op == 7:
        if v1 < v2:
            vals[vals[ind + 3]] = 1
        else:
            vals[vals[ind + 3]] = 0
        ind += 4
    elif op == 8:
        if v1 == v2:
            vals[vals[ind + 3]] = 1
        else:
            vals[vals[ind + 3]] = 0
        ind += 4
    elif op == 99:
        done = True
    else:
        print("Error!")
        done = True
