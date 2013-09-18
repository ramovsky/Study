import sys


def bin2gray(i):
    return i//2 ^ i


def hamming_distance(s1, s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


class Node:

    def __init__(self, bits):
        self.id = int(bits, 2)
        self.ones = bits.count('1')
        self.bits = bits
        self.parent = None
        self.rank = 0

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.ones < other.ones

    def __gt__(self, other):
        return self.ones > other.ones

    def __repr__(self):
        return '<Node:{} {} ones:{}>'.format(self.id, self.bits, self.ones)


class UnionFind:

    def __init__(self):
        self.nodes = {}

    def find(self, id):
        if id not in seld.nodes:
            return
        parent = node = self.nodes[id]
        while parent:
            node = node.parent
            parent = node.parent
        return node

    def union(self, id1, id2):
        node1 = self.find(id1)
        node2 = self.find(id2)



def main():

    if sys.argv[-1] == '3':
        with open('edges.txt', 'rt') as f:
            pass

    else:
        lst = set()
        with open('clustering_big.txt', 'rt') as f:
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                lst.add(Node(r.replace(' ', '')))

        lst = sorted(lst)
        c = lst[0]
        for i, l in enumerate(lst):
            if hamming_distance(l.bits, c.bits) < 3:
                print('{:>10} {}'.format(i, l))


if __name__ == '__main__':
    main()
