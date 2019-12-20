def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines

lines = readFile("d01input.txt")


total = 0
for line in lines:
    num = int(line)
    res = num
    while res > 0:
        res = (res // 3) - 2
        if res > 0:
            total += res

print(total)
