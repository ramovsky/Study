import sys
from heapq import heappop, heappush, heapify


def sum_comp_time(arr):
    c = 0
    s = 0
    for w, l in arr:
        c += l
        s += w*c
    return s


class Graph(dict):

    def __repr__(self):
        return '<Graph with {} nodes>'.format(len(self.nodes))

    def get_node(self, id):
        node = self.get(id)
        if node is None:
            node = Node(id)
            self[id] = node
        return node

    def add_data(self, src, dst, weight):
        node = self.get_node(src)
        node.add_edge(dst, weight)
        node = self.get_node(dst)
        node.add_edge(src, weight)

    def get_length(self):
        length = 0
        visited = set()
        qset = {1}
        source = self.get_node(1)
        source.score = 0
        queue = [source]
        while queue:
            node = heappop(queue)
            if node.id in visited:
                continue
            visited.add(node.id)
            length += node.score
            for id, w in node.edges.items():
                if id in visited:
                    continue
                node = self.get_node(id)
                if id in qset:
                    queue.remove(node)
                qset.add(id)
                node.update_score(w)
                heappush(queue, node)

        return length


class Node(object):

    def __init__(self, id):
        self.id = id
        self.edges = {}
        self.score = 10000000

    def __repr__(self):
        return '<Node {}. score:{} edges:{}>'.format(
            self.id, self.score, self.edges.keys())

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def add_edge(self, node, weight):
        self.edges[node] = weight

    def update_score(self, score):
        self.score = min(self.score, score)


def main():

    if sys.argv[-1] == '3':
        with open('edges.txt', 'rt') as f:
            graph = Graph()
            for r in f.read().split('\n'):
                if not r:
                    continue
                graph.add_data(*map(int, r.split(' ')))

        print(graph.get_length())
        print(graph[1])

    else:
        with open('jobs.txt', 'rt') as f:
            data = []
            for r in f.read().split('\n'):
                if not r:
                    continue
                w, l = map(int, r.split(' '))
                data.append((w, l))

        diff = sorted(data, key=lambda a: a[1] - a[0] - a[0]/10000)
        print(data[:10])
        print(diff[:10])
        print(sum_comp_time(diff))

        ratio = sorted(data, key=lambda a: -a[0]/a[1])
        print(ratio[:10])
        print(sum_comp_time(ratio))


if __name__ == '__main__':
    main()
