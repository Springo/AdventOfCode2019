from fractions import Fraction
from math import ceil

def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def get_ores(chem, react, reserves, need):
    if chem not in reserves:
        reserves[chem] = 0

    count = 0
    for inp in react[chem][1:]:
        name, amt = inp
        amt = need * amt
        if name not in reserves:
            reserves[name] = 0

        if name == "ORE":
            count += amt
        else:
            if reserves[name] < amt:
                new_needed = ceil((amt - reserves[name]) / react[name][0])
                count += get_ores(name, react, reserves, new_needed)[0]
            reserves[name] -= amt

    reserves[chem] += need * react[chem][0]

    return count, reserves


lines = readFile("d14input.txt")
#lines = readFile("test.txt")
react = dict()
for line in lines:
    form = line.split(' => ')
    outp = form[1].split(' ')
    inp = form[0].split(', ')
    react[outp[1]] = [int(outp[0])]
    for chem in inp:
        inp_i = chem.split(' ')
        react[outp[1]].append((inp_i[1], int(inp_i[0])))

print(get_ores("FUEL", react, dict(), 1)[0])

reserves = dict()
count = 0
ore = 1000000000000
while ore > 0:
    amt = max(ore // 1000000, 1)
    res, reserves = get_ores("FUEL", react, reserves, amt)
    ore -= res
    count += amt
    if count % 1000 == 0:
        print(count)
        print(ore)
    #print("{}: {} {}".format(i + 1, res, cumul))

print(count - 1)
