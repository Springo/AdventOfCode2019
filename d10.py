from fractions import Fraction

def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def compute_slope(p1, p2):
    sign = 0
    if p1[1] >= p2[1]:
        sign += 1
    if p1[0] > p2[0]:
        sign += 5
    if p2[0] - p1[0] != 0:
        return Fraction(p2[1] - p1[1], p1[0] - p2[0]), sign
    return Fraction(1000, 1), sign


def count_reachable(p, grid):
    x = p[0]
    y = p[1]
    reachable = dict()
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '#' and (i != y or j != x):
                slope = compute_slope(p, (j, i))
                if slope not in reachable:
                    reachable[slope] = 1
                    count += 1
    return count


def parse_quad(quad):
    if quad == 0:
        return 1
    elif quad == 1:
        return 2
    elif quad == 5:
        return 0
    elif quad == 6:
        return 3


def get_reachable(p, grid):
    x = p[0]
    y = p[1]
    quadrant = dict()
    quadrant[0] = dict()
    quadrant[1] = dict()
    quadrant[2] = dict()
    quadrant[3] = dict()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '#' and (i != y or j != x):
                slope, quad = compute_slope(p, (j, i))
                quad = parse_quad(quad)
                if slope not in quadrant[quad]:
                    quadrant[quad][slope] = []
                quadrant[quad][slope].append((j, i))
    return quadrant


lines = readFile("d10input.txt")
#lines = readFile("test.txt")
grid = []
for line in lines:
    grid.append([c for c in line])

best = 0
loc_x = -1
loc_y = -1
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '#':
            reachable = count_reachable((j, i), grid)
            if reachable > best:
                best = reachable
                loc_x = j
                loc_y = i

print(best)
print((loc_x, loc_y))

reachable = get_reachable((loc_x, loc_y), grid)
print(reachable[0])


for quad in range(4):
    for key in reachable[quad]:
        arr = reachable[quad][key]
        sums = [arr[i][0] + arr[i][1] for i in range(len(arr))]
        reachable[quad][key] = sorted(arr, key=lambda sums: sums[0])


done = False
count = 0
while not done:
    for quad in range(4):
        print(quad)
        keys = list(reachable[quad].keys())
        if quad == 0 or quad == 2:
            keys = sorted(keys, reverse=True)
            print(keys)
        else:
            keys = sorted(keys, reverse=True)
            print(keys)
        for key in keys:
            if len(reachable[quad][key]) > 0:
                coord = reachable[quad][key].pop(0)
                count += 1
                if count == 200:
                    done = True
                    print(coord)
                    print(coord[0] * 100 + coord[1])


