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
                print(v1)
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


lines = readFile("d17input.txt")
vals_orig = [int(c) for c in lines[0].split(',')]
vals_orig[0] = 2

prog = Program(vals_orig, phase=None)

out_str = ""
overall = "B,B,C,A,C,A,C,A,A,B"
A = "R,10,R,4,R,4"
B = "R,8,L,4,R,4,R,10,R,8"
C = "L,12,L,12,R,8,R,8"
inp = [ord(c) for c in overall]
inp.append(10)
inp.extend([ord(c) for c in A])
inp.append(10)
inp.extend([ord(c) for c in B])
inp.append(10)
inp.extend([ord(c) for c in C])
inp.append(10)
inp.append(ord('n'))
inp.append(10)
prog.add_input(inp)
"""
inp_ind = 0

while True:
    prog.run(stop=3)
    outs = prog.flush_outputs()
    for out in outs:
        out_str = out_str + chr(out)
    for c in out_str:
        print(c, end=' ')
    input("-> ")
    prog.add_input([inp[inp_ind]])
    inp_ind += 1
    prog.run(stop=4)
"""
prog.run()
outs = prog.flush_outputs()
for out in outs:
    out_str = out_str + chr(out)
for c in out_str:
    print(c, end=' ')
print(outs[-1])
"""
grid = []
line = []
for c in out_str:
    if c == "\n":
        grid.append(line)
        line = []
    else:
        line.append(c)

grid.pop(-1)
"""
"""
align = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        counter = 0
        if grid[i][j] == '#':
            if j < len(grid[i]) - 1 and grid[i][j + 1] == '#':
                counter += 1
            if j > 0 and grid[i][j - 1] == '#':
                counter += 1
            if i < len(grid) - 1 and grid[i + 1][j] == '#':
                counter += 1
            if i > 0 and grid[i - 1][j] == '#':
                counter += 1
        if counter >= 3:
            align += (i * j)

print(align)
"""

"""
rob_i = 0
rob_j = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '^':
            rob_i = i
            rob_j = j


a = len(grid)
b = len(grid[0])

dir = 1
count = 0
t = 'R'
moves = []
done = False
while not done:
    next_i = -1
    next_j = -1
    right_i = -1
    right_j = -1
    left_i = -1
    left_j = -1
    if dir == 0:
        next_i = rob_i - 1
        next_j = rob_j
        right_i = rob_i
        right_j = rob_j + 1
        left_i = rob_i
        left_j = rob_j - 1
    if dir == 1:
        next_i = rob_i
        next_j = rob_j + 1
        right_i = rob_i + 1
        right_j = rob_j
        left_i = rob_i - 1
        left_j = rob_j
    if dir == 2:
        next_i = rob_i + 1
        next_j = rob_j
        right_i = rob_i
        right_j = rob_j - 1
        left_i = rob_i
        left_j = rob_j + 1
    if dir == 3:
        next_i = rob_i
        next_j = rob_j - 1
        right_i = rob_i - 1
        right_j = rob_j
        left_i = rob_i + 1
        left_j = rob_j

    if 0 <= next_i < len(grid) and 0 <= next_j < len(grid[next_i]) and grid[next_i][next_j] == '#':
        count += 1
        rob_i = next_i
        rob_j = next_j
    else:
        moves.append(t + str(count))
        count = 0
        if 0 <= left_i < a and 0 <= left_j < b and grid[left_i][left_j] == '#':
            t = 'L'
            dir = (dir - 1) % 4
        elif 0 <= right_i < a and 0 <= right_j < b and grid[right_i][right_j] == '#':
            t = 'R'
            dir = (dir + 1) % 4
        else:
            done = True

print(moves)
"""


