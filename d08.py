def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines

lines = readFile("d08input.txt")[0]
new_lines = []
grid = [[-1] * 25 for _ in range(6)]
for i in range(len(lines) // (25 * 6)):
    line = ""
    for j in range(6 * 25):
        c = lines[i * (25 * 6) + j]
        line = line + c
        if grid[j // 25][j % 25] == -1:
            if c == '0':
                grid[j // 25][j % 25] = 0
            elif c == '1':
                grid[j // 25][j % 25] = 1
    new_lines.append(line)

best = -1
count = 0
for line in new_lines:
    zeros = 0
    ones = 0
    twos = 0
    for c in line:
        val = int(c)
        if val == 0:
            zeros += 1
        elif val == 1:
            ones += 1
        elif val == 2:
            twos += 1
    if best == -1 or zeros < best:
        best = zeros
        count = ones * twos
        print(best)

print(count)

for line in grid:
    for c in line:
        if c == 0:
            print(' ', end=' ')
        elif c == 1:
            print('X', end=' ')
        else:
            print('?', end=' ')
    print()



