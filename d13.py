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
                    self.outputs = []
                    result = self.outputs
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


grid = [[' '] * 44 for _ in range(21)]
def display_grid(outputs, score):
    ball_pos = (0, 0)
    pad_pos = (0, 0)
    for i in range(len(outputs) // 3):
        x = outputs[3 * i]
        y = outputs[3 * i + 1]
        tile = outputs[3 * i + 2]

        if x == -1 and y == 0:
            print("Score Update!")
            score += tile
        else:
            if tile == 0:
                grid[y][x] = '.'
            elif tile == 1:
                grid[y][x] = '|'
            elif tile == 2:
                grid[y][x] = 'X'
            elif tile == 3:
                grid[y][x] = '_'
                pad_pos = (y, x)
            elif tile == 4:
                grid[y][x] = 'O'
                ball_pos = (y, x)
            else:
                print("Error")

    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j], end=' ')
        print()
    """

    print("Score: {}".format(score))
    return ball_pos, pad_pos, score


lines = readFile("d13input.txt")

vals_orig = [int(c) for c in lines[0].split(',')]

count = 0
prog = Program(vals_orig, phase=None)
prog.vals[0] = 2
while not prog.halted:
    prog.run(stop=3)
    outputs = prog.flush_outputs()
    print(outputs)
    score = 0
    bp, pp, score = display_grid(outputs, score)
    #inp = 2
    #while inp != -1 and inp != 0 and inp != 1:
    #    inp = int(input("Enter command: "))
    if bp[1] < pp[1]:
        inp = -1
    elif bp[1] > pp[1]:
        inp = 1
    else:
        inp = 0
    prog.add_input([inp])
    prog.run(stop=4)

    """
    out_1 = prog.run(stop=2)[0]
    if out_1 is None:
        break
    out_2 = prog.run(stop=2)[0]
    out_3 = prog.run(stop=2)[0]

    if out_3 == 2:
        count += 1
    """

#print(count)
print(score)

