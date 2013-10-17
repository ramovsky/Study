import sys
from collections import defaultdict

cache = defaultdict(dict)
nodes = []
hits = 0


def solve_knapsack(i, size):
#    print('.'*(7-i), i, size)
    global hits
    if i < 0:
        return 0

    if size in cache[i]:
        hits += 1
        return cache[i][size]

    profit = solve_knapsack(i-1, size)
    node = nodes[i]
    if size >= node[1]:
        profit = max(profit, solve_knapsack(i-1, size - node[1]) + node[0])
    cache[i][size] = profit
    return profit


def main():

    sys.setrecursionlimit(20000)

    if sys.argv[-1] == '2':
        with open('knapsack_big.txt', 'rt') as f:
            size = None
            values = []
            weights = []
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                v, w = map(int, r.split(' '))
                if size is None:
                    size = v
                    items = w
                else:
                    nodes.append((v, w))
                    values.append(v)
                    weights.append(w)

        print('ANS', solve_knapsack(items-1, size), hits)


    else:
        with open('knapsack1.txt', 'rt') as f:
            size = None
            values = []
            weights = []
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                v, w = map(int, r.split(' '))
                if size is None:
                    size = v
                    items = w
                else:
                    values.append(v)
                    weights.append(w)

        cache = defaultdict(int)
        print(len(values), len(weights))
        for i in range(1, items):
            for j in range(size, 0, -1):
                if j >= weights[i]:
                    cache[(i, j)] = max(
                        cache[(i-1, j)],
                        cache[(i-1, j-weights[i])] + values[i])
                else:
                    cache[(i, j)] = cache[(i-1, j)]

        ks, m = 0, 0
        for k, v in cache.items():
            if v > m:
                m = v
                ks = k
        print(ks, cache[ks])


if __name__ == '__main__':
    main()
