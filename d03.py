def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def mandist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

lines = readFile("d03input.txt")
wire1 = lines[0].split(',')
wire2 = lines[1].split(',')

grid = [[0] * 20000 for _ in range(20000)]
row = 10000
col = 10000
center = (row, col)

steps = 0
for word in wire1:
    c = word[0]
    lent = int(word[1:])
    for step in range(lent):
        if c == 'D':
            row -= 1
        if c == 'U':
            row += 1
        if c == 'R':
            col += 1
        if c == 'L':
            col -= 1
        steps += 1
        if grid[row][col] == 0:
            grid[row][col] = steps

row = center[0]
col = center[1]

best_man_dist = -1
best_point = None

steps = 0
best_steps = -1
for word in wire2:
    c = word[0]
    lent = int(word[1:])
    for step in range(lent):
        if c == 'D':
            row -= 1
        if c == 'U':
            row += 1
        if c == 'R':
            col += 1
        if c == 'L':
            col -= 1
        steps += 1
        if grid[row][col] != 0:
            if best_steps == -1 or steps + grid[row][col] < best_steps:
                best_steps = steps + grid[row][col]
        """
        if grid[row][col] == 1:
            point = (row, col)
            dist = mandist(point, center)
            if best_point is None or dist < best_man_dist:
                best_man_dist = dist
                best_point = point
        """

#print(best_man_dist)
print(best_steps)
