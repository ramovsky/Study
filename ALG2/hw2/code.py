import sys
from itertools import combinations_with_replacement

to_bin = lambda i: '{:.>24}'.format(bin(i)[2:])

def bin2gray(i):
    return i//2 ^ i


def hamming_distance(s1, s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


class Node:

    def __init__(self, id):
        self.id = id
        self.parent = self
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
        self.clusters = 0
        self.rank = 0

    def add_node(self, id):
        if id not in self.nodes:
            node = Node(id)
            self.nodes[node.id] = node
            self.clusters += 1

    def find(self, node):
        lst = [node]
        while True:
            if node.parent == node:
                break
            node = node.parent
            lst.append(node)
        for n in lst:
            n.parent = node
        return node

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root2 == root1:
            return
        if root2.rank > root1.rank:
            root1.parent = root2
        elif root2.rank == root1.rank:
            root1.parent = root2
            root2.rank += 1
            if root2.rank > self.rank:
                self.rank = root2.rank
        else:
            root2.parent = root1
        self.clusters -= 1

    def distance(self, node1, node2):
        return hamming_distance(node1.bits, node2.bits)



def main():

    if sys.argv[-1] == '1':
        union_find = UnionFind()
        with open('clustering1.txt', 'rt') as f:
            edges = []
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                id1, id2, e = map(int, r.split(' '))
                union_find.add_node(id1)
                union_find.add_node(id2)
                edges.append((e, id1, id2))

        edges.sort(reverse=True)
        print(len(edges), union_find.clusters)
        while union_find.clusters > 3:
            e, id1, id2 = edges.pop()
            node1, node2 = union_find.nodes[id1], union_find.nodes[id2]
            union_find.union(node1, node2)

        print(e, len(edges), union_find.clusters)

    else:
        union_find = UnionFind()
        with open('clustering_big.txt', 'rt') as f:
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                id = int(r.replace(' ', ''), 2)
                union_find.add_node(id)

        masks = []
        for l, r in combinations_with_replacement(range(24), 2):
            masks.append(1 << l | 1 << r)

        print(union_find.clusters)
        for n in union_find.nodes.values():
            for m in masks:
                id2 = n.id ^ m
                if id2 in union_find.nodes:
                    node2 = union_find.nodes[id2]
                    union_find.union(n, node2)

        print(union_find.clusters)


if __name__ == '__main__':
    main()
