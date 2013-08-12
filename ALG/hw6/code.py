from heapq import heappop, heappush, heapify



def main():
    with open('2sum.txt', 'rt') as f:
        data = set()
        for r in f.read().split('\n'):
            if not r:
                continue
            data.add(int(r))

    c = 0
    for t in range(-1000, 1001):
        print(t)
        for e in data:
            if t - e in data:
                c += 1
    print(c, c//2)


if __name__ == '__main__':
    main()
