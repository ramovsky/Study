import sys
from collections import defaultdict


INF = float('inf')


def print_i(i, space=5):
    delete = "\b" * space
    print("{0}{1:<{2}}".format(delete, i, space), end="")
    sys.stdout.flush()


def main():

    sys.setrecursionlimit(20000)

    idx = sys.argv[-1]
    with open('g{}.txt'.format(idx), 'rt') as f:
        size = None
        edges = {}
        for r in f.read().split('\n'):
            if not r:
                continue
            elif r == 'stop':
                break
            if size is None:
                size, d = map(int, r.split(' '))
            else:
                s, d, l = map(int, r.split(' '))
                edges[(s, d)] = l

    prev = {}
    work = {}
    shortest = INF

    for i in range(1, size+1):
        for j in range(1, size+1):
            key = (i, j)
            if i == j:
                prev[key] = 0
            elif key in edges:
                prev[key] = edges[key]
            else:
                prev[key] = INF

    for k in range(1, size+1):
        print_i(k)
        for i in range(1, size+1):
            for j in range(1, size+1):
                key = (i, j)
                v = min(
                    prev[key],
                    prev[(i, k)] + prev[(k, j)]
                    )
                shortest = min(shortest, v)
                work[key] = v
        prev = work.copy()
        work = {}

    cycle = False
    for i in range(1, size+1):
        if prev[(i, i)] < 0:
            cycle = True
            break

    print('\nShortest: {} \nCycles: {}'.format(shortest, cycle))



if __name__ == '__main__':
    main()
