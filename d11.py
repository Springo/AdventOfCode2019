
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

    def run(self, stop=0):
        done = False
        while not done:
            com = self.vals[self.get_mem(self.ind)]
            strcom = str(com)
            for i in range(5 - len(strcom)):
                strcom = '0' + strcom

            op = int(strcom[-2:])

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
                result = self.outputs
                self.outputs = []
                #print(result)
                if stop == 2:
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
        return [None]


def print_grid(row_low, row_high, col_low, col_high):
    for i in range(row_low, row_high):
        for j in range(col_low, col_high):
            val = grid[i][j]
            if val == 0:
                print(".", end=' ')
            elif val == 1:
                print("#", end=' ')
        print()


lines = readFile("d11input.txt")
vals_orig = [int(c) for c in lines[0].split(',')]

prog = Program(vals_orig, phase=None)

grid = [[0] * 20000 for _ in range(20000)]
traverse = dict()
count = 0
robrow = 10000
robcol = 10000
robdir = 0

grid[robrow][robcol] = 1

while not prog.halted:
    if count == 5:
        print_grid(9990, 10010, 9990, 10010)
    prog.add_input([grid[robrow][robcol]])
    out = prog.run(stop=2)[0]
    if out is not None:
        grid[robrow][robcol] = out
        if (robrow, robcol) not in traverse:
            traverse[(robrow, robcol)] = 1
            count += 1
        out = prog.run(stop=2)[0]
        if out is not None:
            if out == 0:
                robdir = (robdir - 1) % 4
            elif out == 1:
                robdir = (robdir + 1) % 4

            if robdir == 0:
                robrow -= 1
            elif robdir == 1:
                robcol += 1
            elif robdir == 2:
                robrow += 1
            elif robdir == 3:
                robcol -= 1

print(count)
print_grid(9800, 10200, 9800, 10200)
