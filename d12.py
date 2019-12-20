import math
def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def norm(p):
    return abs(p[0]) + abs(p[1]) + abs(p[2])

def get_coord(arr1, arr2, i):
    coord = []
    for j in range(len(arr1)):
        coord.append(arr1[j][i])
        coord.append(arr2[j][i])
    return tuple(coord)


lines = readFile("d12input.txt")
#lines = readFile("test.txt")
pos = []
vel = []
for line in lines:
    parse = line.split(",")
    x = int(parse[0][3:])
    y = int(parse[1][3:])
    z = int(parse[2][3:-1])
    pos.append([x, y, z])
    vel.append([0, 0, 0])


prev = dict()
orig_coord_x = get_coord(pos, vel, 0)
orig_coord_y = get_coord(pos, vel, 1)
orig_coord_z = get_coord(pos, vel, 2)
print(orig_coord_x)
x_loop = 0
y_loop = 0
z_loop = 0
for iter in range(300000):
    for b1 in range(len(pos)):
        for b2 in range(b1 + 1, len(pos)):
            for j in range(3):
                if pos[b1][j] < pos[b2][j]:
                    vel[b1][j] += 1
                    vel[b2][j] -= 1
                elif pos[b1][j] > pos[b2][j]:
                    vel[b1][j] -= 1
                    vel[b2][j] += 1
    for i in range(len(pos)):
        pos[i][0] += vel[i][0]
        pos[i][1] += vel[i][1]
        pos[i][2] += vel[i][2]
    coord_x = get_coord(pos, vel, 0)
    coord_y = get_coord(pos, vel, 1)
    coord_z = get_coord(pos, vel, 2)
    if coord_x == orig_coord_x and x_loop == 0:
        x_loop = iter + 1
        print("x: {}".format(x_loop))
        print(coord_x)
    if coord_y == orig_coord_y and y_loop == 0:
        y_loop = iter + 1
        print("y: {}".format(y_loop))
    if coord_z == orig_coord_z and z_loop == 0:
        z_loop = iter + 1
        print("z: {}".format(z_loop))

print(pos)
print(vel)

total = 0
for b in range(len(pos)):
    pot = norm(pos[b])
    kin = norm(vel[b])
    total += pot * kin
print(total)


lcm_1 = x_loop * y_loop // math.gcd(x_loop, y_loop)
lcm_2 = lcm_1 * z_loop // math.gcd(lcm_1, z_loop)
print(lcm_2)