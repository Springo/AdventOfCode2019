import itertools

def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


class Program:
    def __init__(self, vals_orig, phase):
        self.vals = vals_orig[:]
        self.ind = 0
        self.inputs = [phase]
        self.outputs = []
        self.halted = False
        self.run(stop=1)

    def add_input(self, inps):
        for i in inps:
            self.inputs.append(i)

    def run(self, stop=0):
        done = False
        while not done:
            com = self.vals[self.ind]
            strcom = str(com)
            for i in range(5 - len(strcom)):
                strcom = '0' + strcom

            op = int(strcom[-2:])

            v1 = None
            v2 = None
            v3 = None
            if op != 99:
                if strcom[2] == '0':
                    v1 = self.vals[self.vals[self.ind + 1]]
                elif strcom[2] == '1':
                    v1 = self.vals[self.ind + 1]
                else:
                    v1 = None
            if op == 1 or op == 2 or op == 5 or op == 6 or op == 7 or op == 8:
                if strcom[1] == '0':
                    v2 = self.vals[self.vals[self.ind + 2]]
                elif strcom[1] == '1':
                    v2 = self.vals[self.ind + 2]
                else:
                    v2 = None
            if op == 1 or op == 2 or op == 7 or op == 8:
                if strcom[0] == '0':
                    v3 = self.vals[self.vals[self.ind + 3]]
                elif strcom[0] == '1':
                    v3 = self.vals[self.ind + 3]
                else:
                    v3 = None

            if op == 1:
                self.vals[self.vals[self.ind + 3]] = v1 + v2
                self.ind += 4
            elif op == 2:
                self.vals[self.vals[self.ind + 3]] = v1 * v2
                self.ind += 4
            elif op == 3:
                inp = self.inputs.pop(0)
                self.vals[self.vals[self.ind + 1]] = inp
                self.ind += 2
                if stop == 1:
                    return
            elif op == 4:
                self.outputs.append(v1)
                self.ind += 2
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
                    self.vals[self.vals[self.ind + 3]] = 1
                else:
                    self.vals[self.vals[self.ind + 3]] = 0
                self.ind += 4
            elif op == 8:
                if v1 == v2:
                    self.vals[self.vals[self.ind + 3]] = 1
                else:
                    self.vals[self.vals[self.ind + 3]] = 0
                self.ind += 4
            elif op == 99:
                done = True
                self.halted = True
            else:
                print("Error!")
                done = True


lines = readFile("d07input.txt")
vals_orig = [int(c) for c in lines[0].split(',')]
#vals_orig = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
#27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#phases = list(itertools.permutations([0, 1, 2, 3, 4]))
phases = list(itertools.permutations([5, 6, 7, 8, 9]))

best_res = 0
for phase_list in phases:
    prog = [Program(vals_orig, phase_list[i]) for i in range(5)]
    prog[0].add_input([0])

    done = False
    last_e = 0
    while not done:
        for i in range(len(prog)):
            outs = prog[i].run(stop=2)
            if prog[0].halted:
                done = True
                if last_e > best_res:
                    best_res = last_e
            else:
                prog[(i + 1) % 5].add_input(outs)
                if i == 4:
                    last_e = outs[-1]


print(best_res)

"""
best_res = 0
for phase_list in phases:
    done = False
    res = [0]
    cur_e = -1
    while not done:
        for phase in phase_list:
            res = run_program(vals_orig, phase, res)
            if len(res) == 0:
                done = True
                break
        if len(res) != 0:
            cur_e = res
            #print(cur_e)
    print(cur_e)
    if cur_e > best_res:
        best_res = cur_e

print(best_res)
"""

"""
def run_program(vals_orig, phase, prev_inp):
    vals = vals_orig[:]
    done = False
    ind = 0
    inp = phase
    inp_ind = 0
    output = []

    while not done:
        com = vals[ind]
        strcom = str(com)
        for i in range(5 - len(strcom)):
            strcom = '0' + strcom

        op = int(strcom[-2:])

        v1 = None
        v2 = None
        v3 = None
        if op != 99:
            if strcom[2] == '0':
                v1 = vals[vals[ind + 1]]
            elif strcom[2] == '1':
                v1 = vals[ind + 1]
            else:
                v1 = None
        if op == 1 or op == 2 or op == 5 or op == 6 or op == 7 or op == 8:
            if strcom[1] == '0':
                v2 = vals[vals[ind + 2]]
            elif strcom[1] == '1':
                v2 = vals[ind + 2]
            else:
                v2 = None
        if op == 1 or op == 2 or op == 7 or op == 8:
            if strcom[0] == '0':
                v3 = vals[vals[ind + 3]]
            elif strcom[0] == '1':
                v3 = vals[ind + 3]
            else:
                v3 = None

        if op == 1:
            vals[vals[ind + 3]] = v1 + v2
            ind += 4
        elif op == 2:
            vals[vals[ind + 3]] = v1 * v2
            ind += 4
        elif op == 3:
            vals[vals[ind + 1]] = inp
            inp = prev_inp[inp_ind]
            inp_ind += 1
            ind += 2
        elif op == 4:
            output.append(v1)
            ind += 2
        elif op == 5:
            if v1 != 0:
                ind = v2
            else:
                ind += 3
        elif op == 6:
            if v1 == 0:
                ind = v2
            else:
                ind += 3
        elif op == 7:
            if v1 < v2:
                vals[vals[ind + 3]] = 1
            else:
                vals[vals[ind + 3]] = 0
            ind += 4
        elif op == 8:
            if v1 == v2:
                vals[vals[ind + 3]] = 1
            else:
                vals[vals[ind + 3]] = 0
            ind += 4
        elif op == 99:
            done = True
        else:
            print("Error!")
            done = True

    return output
"""


