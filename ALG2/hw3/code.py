import sys
from collections import defaultdict


def main():

    if sys.argv[-1] == '2':
        pass

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
                    size = v+1
                    items = w
                else:
                    values.append(v)
                    weights.append(w)

        cache = defaultdict(int)
        print(len(values), len(weights))
        for i in range(1, items):
            for j in range(size):
                if j >= weights[i]:
                    cache[(i, j)] = max(
                        cache[(i-1, j)],
                        cache[(i-1, j-weights[i])] + values[i])
                else:
                    cache[(i, j)] = cache[(i-1, j)]

        print(max(cache.values()))


if __name__ == '__main__':
    main()
