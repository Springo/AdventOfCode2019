import heapq
import copy
import random

def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def find_reachable(source, loc, grid):
    row, col = loc
    adj = dict()

    q = [(row, col, 0)]
    visited = dict()
    visited[loc] = True
    while len(q) > 0:
        row, col, dist = q.pop(0)

        new_coords = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for coord in new_coords:
            row_new, col_new = coord
            if (row_new, col_new) not in visited:
                visited[(row_new, col_new)] = True
                if grid[row_new][col_new] != '#' and grid[row_new][col_new] != '.':
                    adj[grid[row_new][col_new]] = dist + 1

                if grid[row_new][col_new] == '.':
                    q.append((row_new, col_new, dist + 1))

    return adj


def get_reachable_keys(paths, cur_keys):
    keys = []
    for key in paths:
        if key != '@' and key.islower() and key not in cur_keys:
            keys.append(key)

    return keys


def shortest_path(source, adj_list, keys):
    p_q = []
    heapq.heappush(p_q, (0, source))
    dists = dict()
    dists[source] = 0

    while p_q:
        dist, node = heapq.heappop(p_q)
        if dist == dists[node]:
            if node == '@' or not (node.isupper() and node.lower() not in keys):
                for neigh in adj_list[node]:
                    edge = adj_list[node][neigh]
                    if neigh not in dists or dist + edge < dists[neigh]:
                        heapq.heappush(p_q, (dist + edge, neigh))
                        dists[neigh] = dist + edge

    return dists


def TSP(source, adj_list, keys, lookup):
    sp = shortest_path(source, adj_list, keys)
    reachable = get_reachable_keys(sp, keys)

    if len(reachable) == 0:
        return 0

    best_dist = -1
    for key in reachable:
        new_keys = copy.deepcopy(keys)
        new_keys[key] = True

        dist = sp[key]
        if (source, tuple(new_keys)) not in lookup:
            lookup[(source, tuple(new_keys))] = TSP(key, adj_list, new_keys, lookup)
        everything_else = lookup[(source, tuple(new_keys))]
        if best_dist == -1 or dist + everything_else < best_dist:
            best_dist = dist + everything_else
            #if source == '@':

    return best_dist


def random_greedy(source, adj_list, keys, found, threshold, lookup, rand_roll=True):
    sp = shortest_path(source, adj_list, keys)
    reachable = get_reachable_keys(sp, keys)

    if len(reachable) == 0:
        return 0

    if found > threshold:
        return TSP(source, adj_list, keys, lookup)

    dists = []
    total = 0
    for key in reachable:
        heur = sp[key] ** 2
        dists.append((key, heur))
        total += 1 / heur
    dists = sorted(dists, key=lambda tup: tup[1])
    weights = []
    for tup in dists:
        _, dist = tup
        weights.append(1 / (total * dist))
    if rand_roll:
        result = random.random()
    else:
        result = 0
    best_key = -1
    for i in range(len(weights)):
        if result <= weights[i]:
            best_key = dists[i][0]
            break
        else:
            result -= weights[i]


    new_keys = copy.deepcopy(keys)
    new_keys[best_key] = True

    dist = sp[best_key]
    everything_else = random_greedy(best_key, adj_list, new_keys, found + 1, threshold, lookup, rand_roll)

    return dist + everything_else



lines = readFile("d18input.txt")

grid = []
for line in lines:
    row = []
    for c in line:
        row.append(c)
    grid.append(row)

loc = dict()
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] != '.' and grid[i][j] != '#':
            loc[grid[i][j]] = (i, j)


adj_list = dict()
for key in loc:
    adj_list[key] = find_reachable(key, loc[key], grid)

#print(adj_list['@'])
#print(shortest_path('@', adj_list, []))
#print(get_reachable_keys(shortest_path('@', adj_list, []), dict()))
#print(TSP('@', adj_list, dict(), dict()))
#print(random_greedy('@', adj_list, dict()))

best = None
for i in range(100000):
    if i % 10 == 0:
        print(i)
        print(best)
    result = random_greedy('@', adj_list, dict(), 0, 18, dict(), rand_roll=True)
    if best is None or result < best:
        best = result
print(best)
