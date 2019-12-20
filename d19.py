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

    def run(self, stop=0, verbose=False):
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
            v1_str = None
            v2_str = None
            v3_str = None
            if op != 99:
                if strcom[2] == '0':
                    v1 = self.vals[self.get_mem(self.vals[self.get_mem(self.ind + 1)])]
                    v1_addr = self.get_mem(self.vals[self.get_mem(self.ind + 1)])
                    v1_str = "mem[{}]".format(self.vals[self.get_mem(self.ind + 1)])
                elif strcom[2] == '1':
                    v1 = self.vals[self.get_mem(self.ind + 1)]
                    v1_addr = self.get_mem(self.vals[self.get_mem(self.ind + 1)])
                    v1_str = str(v1)
                elif strcom[2] == '2':
                    v1 = self.vals[self.get_mem(self.relative + self.vals[self.get_mem(self.ind + 1)])]
                    v1_addr = self.get_mem(self.relative + self.vals[self.get_mem(self.ind + 1)])
                    v1_str = "mem[relative + {}]".format(self.vals[self.get_mem(self.ind + 1)])
                else:
                    v1 = None
            if op == 1 or op == 2 or op == 5 or op == 6 or op == 7 or op == 8:
                if strcom[1] == '0':
                    v2 = self.vals[self.get_mem(self.vals[self.get_mem(self.ind + 2)])]
                    v2_str = "mem[{}]".format(self.vals[self.get_mem(self.ind + 2)])
                elif strcom[1] == '1':
                    v2 = self.vals[self.get_mem(self.ind + 2)]
                    v2_str = str(v2)
                elif strcom[1] == '2':
                    v2 = self.vals[self.get_mem(self.relative + self.vals[self.get_mem(self.ind + 2)])]
                    v2_str = "mem[relative + {}]".format(self.vals[self.get_mem(self.ind + 2)])
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

            if verbose:
                print("{}: ".format(self.ind), end='')
            if op == 1:
                self.vals[v3_addr] = v1 + v2
                self.ind += 4
                if verbose:
                    print("mem[{}] = {} + {}".format(v3_addr, v1_str, v2_str))
            elif op == 2:
                self.vals[v3_addr] = v1 * v2
                self.ind += 4
                if verbose:
                    print("mem[{}] = {} * {}".format(v3_addr, v1_str, v2_str))
            elif op == 3:
                inp = self.inputs.pop(0)
                self.vals[v1_addr] = inp
                self.ind += 2
                if verbose:
                    print("mem[{}] = input({})".format(v1_addr, inp))
                if stop == 1:
                    return
            elif op == 4:
                self.outputs.append(v1)
                self.ind += 2
                if verbose:
                    print("output({})".format(v1_str))
                #print(result)
                if stop == 2:
                    result = self.outputs
                    self.outputs = []
                    return result
            elif op == 5:
                if verbose:
                    print("if {} != 0, jump to {}".format(v1_str, v2_str))
                if v1 != 0:
                    self.ind = v2
                else:
                    self.ind += 3
            elif op == 6:
                if verbose:
                    print("if {} == 0, jump to {}".format(v1_str, v2_str))
                if v1 == 0:
                    self.ind = v2
                else:
                    self.ind += 3
            elif op == 7:
                if verbose:
                    print("if {} < {}, mem[{}] = 1".format(v1_str, v2_str, v3_addr))
                if v1 < v2:
                    self.vals[v3_addr] = 1
                else:
                    self.vals[v3_addr] = 0
                self.ind += 4
            elif op == 8:
                if verbose:
                    print("if {} == {}, mem[{}] = 1".format(v1_str, v2_str, v3_addr))
                if v1 == v2:
                    self.vals[v3_addr] = 1
                else:
                    self.vals[v3_addr] = 0
                self.ind += 4
            elif op == 9:
                if verbose:
                    print("relative += {}".format(v1_str))
                self.relative += v1
                self.ind += 2
            elif op == 99:
                if verbose:
                    print("halt")
                done = True
                self.halted = True
            else:
                print("Error!")
                done = True

            if stop == 4:
                done = True
        return [None]


lines = readFile("d19input.txt")
vals_orig = [int(c) for c in lines[0].split(',')]

prog = Program(vals_orig, None)
prog.add_input([6, 5])
prog.run()
out = prog.flush_outputs()[0]


grid = [[-1] * 100 for _ in range(100)]
total = 0
min_slope = 2
max_slope = 1
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if j > 0:
            if i / j < 1.1 or i / j > 1.4:
                continue
            if i / j > 1.16 and i / j < 1.37:
                continue
        prog = Program(vals_orig, None)
        prog.add_input([j, i])
        out = prog.run(stop=2)[0]
        grid[i][j] = out
        if out == 1:
            if j != 0:
                slope = i / j
                if slope > max_slope:
                    max_slope = slope
                    print(slope)
                if slope < min_slope:
                    min_slope = slope
                    print(slope)
            total += 1

print(total)
for line in grid:
    for c in line:
        if c == 1:
            print("#", end=' ')
        else:
            print(".", end=' ')
    print()

print(min_slope)
print(max_slope)


def check_inp(x, y):
    prog = Program(vals_orig, None)
    prog.add_input([x, y])
    out = prog.run(stop=2)[0]
    return out

def check_square(x, y, size):
    if check_inp(x + size - 1, y) == 1 and check_inp(x, y + size - 1) == 1:
        return True
    return False


done = 3
x = 900
mindist = None
bestdist = None
while done > 0:
    x += 1
    print(x)
    set = done - 1
    for y in range(int(x * 1.15), int(x * 1.35)):
        if check_square(x, y, 100):
            if mindist is None or x + y < mindist:
                print("Done!")
                mindist = x + y
                bestdist = (x, y)
            done = set

print(bestdist[0] * 10000 + bestdist[1])

