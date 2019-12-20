import numpy as np

def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


lines = readFile("d16input.txt")
inp_init = lines[0]
#inp_init = "12345678"
inp = ""
for i in range(10000):
    inp = inp + inp_init
inp = [int(x) for x in list(inp)]
inp = np.array(inp)
print(len(inp))
#inp = "12345678"


def fft(inp, pattern, rep):

    """
    fft_mat = []
    for i in range(len(inp)):
        if i % 1000 == 0:
            print(i)
        patt = np.repeat(pattern, i + 1)
        i_len = len(inp)
        patt = np.tile(patt, i_len // patt.shape[0] + 1)[1:i_len + 1]
        fft_mat.append(patt)
    fft_mat = np.array(fft_mat)

    fft_mat = np.linalg.matrix_power(fft_mat, iters)

    out = fft_mat * inp
    out = np.mod(np.abs(out), 10)
    """


    out = []
    for out_i in range(len(inp)):
        if out_i % 1000 == 999:
            print(out_i)

        patt = np.repeat(pattern, out_i + 1)
        i_len = len(inp)
        patt = np.tile(patt, i_len // patt.shape[0] + 1)[1:i_len + 1]

        result = np.dot(inp, patt)
        result = np.abs(result) % 10
        out.append(result)

    return out


#for i in range(100):
    #print(inp)
    #inp = fft(inp, [0, 1, 0, -1])
#out = fft(inp, [0, 1, 0, -1], 100)
#print(inp)

offset = 0
for i in range(7):
    offset += inp[i] * (10 ** (6 - i))

print(offset)
new_inp = inp[offset:]
for i in range(100):
    print(i)
    new_new_inp = [0] * len(new_inp)
    n = len(new_new_inp)
    new_new_inp[-1] = new_inp[-1]
    for j in range(n - 1):
        new_new_inp[n - j - 2] = new_new_inp[n - j - 1] + new_inp[n - j - 2]
    new_inp = [abs(res) % 10 for res in new_new_inp]

print(new_inp[:8])

#print(inp[offset: offset + 8])
