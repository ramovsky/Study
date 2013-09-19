import sys


def bin2gray(i):
    return i//2 ^ i


def hamming_distance(s1, s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


max_rank = 0


class Node:

    def __init__(self, bits):
        self.id = int(bits, 2)
        self.ones = bits.count('1')
        self.bits = bits
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

    def add_node(self, bits):
        node = Node(bits)
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.clusters += 1

    def find(self, node):
        while True:
            if node.parent == node:
                break
            node = node.parent

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
                print('rank', self.rank)
        else:
            root2.parent = root1
        self.clusters -= 1

    def distance(self, node1, node2):
        return hamming_distance(node1.bits, node2.bits)



def main():

    if sys.argv[-1] == '3':
        with open('edges.txt', 'rt') as f:
            pass

    else:
        union_find = UnionFind()
        with open('clustering_big.txt', 'rt') as f:
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                union_find.add_node(r.replace(' ', ''))

        lst = sorted(union_find.nodes.values())

        print(union_find.clusters)
        n = len(lst)
        for i in range(n):
            print(i, union_find.clusters)
            for j in range(i+1, n):
                node1, node2 = lst[i], lst[j]
                clustered.add({node1, node2})
                if node2.ones - node1.ones > 2:
                    break
                if union_find.distance(node1, node2) < 3:
                    union_find.union(node1, node2)

        print(max_rank)

if __name__ == '__main__':
    main()
