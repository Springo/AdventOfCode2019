def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


class Program:
    def __init__(self, vals_orig, phase):
        self.vals = dict()
        for i in range(len(vals_orig)):
            self.vals[i] = vals_orig[i]
        self.ind = 0
        self.inputs = []
        if phase is not None:
            self.inputs.append(phase)
        self.outputs = []
        self.halted = False
        self.relative = 0
        #self.run(stop=1)

    def add_input(self, inps):
        for i in inps:
            self.inputs.append(i)

    def get_mem(self, i):
        if i in self.vals:
            return i
        self.vals[i] = 0
        return i

    def flush_outputs(self):
        outputs = self.outputs[:]
        self.outputs = []
        return outputs

    def run(self, stop=0):
        done = False
        while not done:
            com = self.vals[self.get_mem(self.ind)]
            strcom = str(com)
            for i in range(5 - len(strcom)):
                strcom = '0' + strcom

            op = int(strcom[-2:])
            if op == 3 and stop == 3:
                return

            v1 = None
            v1_addr = None
            v2 = None
            v3 = None
            v3_addr = None
            if op != 99:
                if strcom[2] == '0':
                    v1 = self.vals[self.get_mem(self.vals[self.get_mem(self.ind + 1)])]
                    v1_addr = self.get_mem(self.vals[self.get_mem(self.ind + 1)])
                elif strcom[2] == '1':
                    v1 = self.vals[self.get_mem(self.ind + 1)]
                    v1_addr = self.get_mem(self.vals[self.get_mem(self.ind + 1)])
                elif strcom[2] == '2':
                    v1 = self.vals[self.get_mem(self.relative + self.vals[self.get_mem(self.ind + 1)])]
                    v1_addr = self.get_mem(self.relative + self.vals[self.get_mem(self.ind + 1)])
                else:
                    v1 = None
            if op == 1 or op == 2 or op == 5 or op == 6 or op == 7 or op == 8:
                if strcom[1] == '0':
                    v2 = self.vals[self.get_mem(self.vals[self.get_mem(self.ind + 2)])]
                elif strcom[1] == '1':
                    v2 = self.vals[self.get_mem(self.ind + 2)]
                elif strcom[1] == '2':
                    v2 = self.vals[self.get_mem(self.relative + self.vals[self.get_mem(self.ind + 2)])]
                else:
                    v2 = None
            if op == 1 or op == 2 or op == 7 or op == 8:
                if strcom[0] == '0':
                    v3 = self.vals[self.get_mem(self.vals[self.get_mem(self.ind + 3)])]
                    v3_addr = self.get_mem(self.vals[self.get_mem(self.ind + 3)])
                elif strcom[0] == '1':
                    v3 = self.vals[self.get_mem(self.ind + 3)]
                    v3_addr = self.get_mem(self.vals[self.get_mem(self.ind + 3)])
                elif strcom[0] == '2':
                    v3 = self.vals[self.get_mem(self.relative + self.vals[self.get_mem(self.ind + 3)])]
                    v3_addr = self.get_mem(self.relative + self.vals[self.get_mem(self.ind + 3)])
                else:
                    v3 = None

            if op == 1:
                self.vals[v3_addr] = v1 + v2
                self.ind += 4
            elif op == 2:
                self.vals[v3_addr] = v1 * v2
                self.ind += 4
            elif op == 3:
                inp = self.inputs.pop(0)
                self.vals[v1_addr] = inp
                self.ind += 2
                if stop == 1:
                    return
            elif op == 4:
                self.outputs.append(v1)
                self.ind += 2
                #print(result)
                if stop == 2:
                    result = self.outputs
                    self.outputs = []
                    return result
            elif op == 5:
                if v1 != 0:
                    self.ind = v2
                else:
                    self.ind += 3
            elif op == 6:
                if v1 == 0:
                    self.ind = v2
                else:
                    self.ind += 3
            elif op == 7:
                if v1 < v2:
                    self.vals[v3_addr] = 1
                else:
                    self.vals[v3_addr] = 0
                self.ind += 4
            elif op == 8:
                if v1 == v2:
                    self.vals[v3_addr] = 1
                else:
                    self.vals[v3_addr] = 0
                self.ind += 4
            elif op == 9:
                self.relative += v1
                self.ind += 2
            elif op == 99:
                done = True
                self.halted = True
            else:
                print("Error!")
                done = True

            if stop == 4:
                done = True
        return [None]


def move_robot(robot, comm):
    robot.add_input([comm])
    out = robot.run(stop=2)[0]
    return out


def reverse(move):
    if move == 1:
        return 2
    elif move == 2:
        return 1
    elif move == 3:
        return 4
    elif move == 4:
        return 3
    else:
        print("ERROR")


def explore(robot, grid, coord_in, hist, seen):
    #print(coord_in)
    #print(hist)
    row, col = coord_in
    if grid[row][col] == -1:
        grid[row][col] = 0

    if len(hist) > 0:
        move_robot(robot, hist[-1])

    coords = [None, 0, 0, 0, 0]
    coords[1] = (row - 1, col)
    coords[2] = (row + 1, col)
    coords[3] = (row, col - 1)
    coords[4] = (row, col + 1)
    for i in range(len(coords)):
        if i == 0:
            continue

        coord = coords[i]
        if coord not in seen:
            seen[coord] = True
            out = move_robot(robot, i)
            if out == 0:
                grid[coord[0]][coord[1]] = 1
            elif out == 1:
                grid[coord[0]][coord[1]] = 0
                hist_new = hist[:]
                hist_new.append(i)
                move_robot(robot, reverse(i))
                explore(robot, grid, coord, hist_new, seen)
            elif out == 2:
                grid[coord[0]][coord[1]] = 2
                hist_new = hist[:]
                hist_new.append(i)
                move_robot(robot, reverse(i))
                explore(robot, grid, coord, hist_new, seen)
                print("Found!")

    if len(hist) > 0:
        move_robot(robot, reverse(hist[-1]))




def display_grid(grid, row_low, row_high, col_low, col_high):
    for i in range(row_low, row_high):
        for j in range(col_low, col_high):
            c = grid[i][j]
            if c == -1:
                print('?', end=' ')
            elif c == 0:
                print(' ', end=' ')
            elif c == 1:
                print('|', end=' ')
            elif c == 2:
                print('@', end=' ')
        print()


lines = readFile("d15input.txt")
vals_orig = [int(c) for c in lines[0].split(',')]

robot = Program(vals_orig, phase=None)
grid = [[-1] * 20000 for _ in range(20000)]
rob_row = 10000
rob_col = 10000

seen = dict()
seen[(rob_row, rob_col)] = True
hist = []

explore(robot, grid, (rob_row, rob_col), hist, seen)
display_grid(grid, 9950, 10050, 9950, 10050)

q = [(rob_row, rob_col, 0)]
seen = dict()
seen[(rob_row, rob_col)] = True

ox_row = 0
ox_col = 0
while len(q) > 0:
    row, col, dist = q.pop(0)
    coords = [None, 0, 0, 0, 0]
    coords[1] = (row - 1, col)
    coords[2] = (row + 1, col)
    coords[3] = (row, col - 1)
    coords[4] = (row, col + 1)
    for coord in coords[1:]:
        if coord not in seen:
            seen[coord] = True
            if grid[coord[0]][coord[1]] == 0:
                q.append((coord[0], coord[1], dist + 1))
            elif grid[coord[0]][coord[1]] == 2:
                q.append((coord[0], coord[1], dist + 1))
                ox_row = coord[0]
                ox_col = coord[1]
                print(dist + 1)


max_dist = 0
q = [(ox_row, ox_col, 0)]
seen = dict()
seen[(ox_row, ox_col)] = True

while len(q) > 0:
    row, col, dist = q.pop(0)
    if dist > max_dist:
        max_dist = dist
    coords = [None, 0, 0, 0, 0]
    coords[1] = (row - 1, col)
    coords[2] = (row + 1, col)
    coords[3] = (row, col - 1)
    coords[4] = (row, col + 1)
    for coord in coords[1:]:
        if coord not in seen:
            seen[coord] = True
            if grid[coord[0]][coord[1]] == 0:
                q.append((coord[0], coord[1], dist + 1))
            elif grid[coord[0]][coord[1]] == 2:
                q.append((coord[0], coord[1], dist + 1))
print(max_dist)
