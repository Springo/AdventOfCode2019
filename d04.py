low = 183564
high = 657474

def isValid(num):
    snum = str(num)
    prevc = snum[0]
    dup = 0
    rep = 1
    for c in snum[1:]:
        if int(c) < int(prevc):
            return False
        if int(c) == int(prevc):
            rep += 1
        else:
            if rep == 2:
                dup += 1
            rep = 1
        prevc = c
    if rep == 2:
        dup += 1
    if dup == 0:
        return False
    return True


count = 0
for n in range(low, high + 1):
    if isValid(n):
        count += 1

print(count)
