import sys
from heapq import heappop, heappush, heapify


class MaxHeap(object):

    def __init__(self, x):
        self.heap = [-e for e in x]
        heapify(self.heap)

    def push(self, value):
        heappush(self.heap, -value)

    def pop(self):
        return -heappop(self.heap)

    def __len__(self):
        return len(self.heap)


def main():

    if sys.argv[-1] == '1':
        with open('sum.txt', 'rt') as f:
            data = set()
            for r in f.read().split('\n'):
                if not r:
                    continue
                data.add(int(r))

        sums = set()
        print(len(data))
        for t in range(-10000, 10001):
            print(t)
            for e in data:
                if t - e in data:
                    sums.add(t)
        print(len(sums))

    elif sys.argv[-1] == '2':
        with open('sum.txt', 'rt') as f:
            sdata = set()
            for r in f.read().split('\n'):
                if not r:
                    continue
                sdata.add(int(r))
                data = list(sdata)

        sums = set()
        while data:
            print(len(data))
            e = data.pop()
            sdata.discard(e)
            for t in range(-10000, 10001):
                if t - e in sdata:
                    sums.add(t)
        print(len(sums))

    else:
        with open('med.txt', 'rt') as f:
            arr = []
            for r in f.read().split('\n'):
                if not r:
                    continue
                arr.append(int(r))

        s = 0
        high = []
        low = MaxHeap(arr[:1])
        w = []
        for d in arr:
            w.append(d)
            w.sort()
            l = len(w)
            if not l%2:
                l -= 1
            s += w[l//2]
        print(s)


if __name__ == '__main__':
    main()
