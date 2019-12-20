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
        self.inputs = [phase]
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
            print(com)
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
                print(result)
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


lines = readFile("d09input.txt")
vals_orig = [int(c) for c in lines[0].split(',')]
#vals_orig = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
inp = 2
prog = Program(vals_orig, inp)

prog.run()
