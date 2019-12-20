def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines

def count_orbits(key, orbits):
    total = len(orbits[key])
    for key2 in orbits[key]:
        total += count_orbits(key2, orbits)
    return total



lines = readFile("d06input.txt")

orbits = dict()
revorbits = dict()
for line in lines:
    objs = line.split(')')
    a = objs[0]
    b = objs[1]
    if a not in orbits:
        orbits[a] = []
        revorbits[a] = []
    if b not in orbits:
        orbits[b] = []
        revorbits[b] = []
    orbits[a].append(b)
    revorbits[b].append(a)


"""
total = 0
for key in orbits:
    total += count_orbits(key, orbits)
print(total)
"""

visited = dict()
visited["YOU"] = True
visited[revorbits["YOU"][0]] = True
goal = revorbits["SAN"][0]
q = [(revorbits["YOU"][0], 0)]
done = False
while not done:
    tup = q.pop(0)
    key, dist = tup
    if key == "SAN":
        print(dist - 1)
        done = True

    for key2 in orbits[key]:
        if key2 not in visited:
            q.append((key2, dist + 1))
            visited[key2] = True
    for key2 in revorbits[key]:
        if key2 not in visited:
            q.append((key2, dist + 1))
            visited[key2] = True



