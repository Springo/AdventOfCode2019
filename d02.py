def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines

lines = readFile("d02input.txt")

vals_orig = [int(c) for c in lines[0].split(',')]

done = False
ind = 0
#vals[1] = 12
#vals[2] = 2
#print(vals)

for v1 in range(0, 100):
    for v2 in range(0, 100):
        vals = vals_orig[:]
        vals[1] = v1
        vals[2] = v2
        done = False
        ind = 0
        while not done:
            com = vals[ind]
            if com == 1:
                vals[vals[ind + 3]] = vals[vals[ind + 1]] + vals[vals[ind + 2]]
            elif com == 2:
                vals[vals[ind + 3]] = vals[vals[ind + 1]] * vals[vals[ind + 2]]
            elif com == 99:
                done = True
                if vals[0] == 19690720:
                    print(100 * v1 + v2)
                    exit()

            else:
                print("Error!")
                done = True
            ind += 4
