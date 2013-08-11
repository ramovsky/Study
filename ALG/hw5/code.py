from heapq import heappop, heappush, heapify


class Graph(dict):

    def __repr__(self):
        return '<Graph with {} nodes>'.format(len(self.nodes))

    def get_node(self, id):
        node = self.get(id)
        if node is None:
            node = Node(id)
            self[id] = node
        return node

    def add_data(self, node, pairs):
        node = self.get_node(int(node))
        for p in pairs:
            if p:
                node.add_edge(*map(int, p.split(',')))

    def get_length(self, s, d):
        visited = set()
        qset = set([s])
        source = self.get_node(s)
        source.score = 0
        queue = [source]
        while queue:
            node = heappop(queue)
            visited.add(node.id)
            qset.discard(node.id)
            for id, l in node.edges:
                if id in visited:
                    continue
                if id in qset:
                    queue.remove(self[id])
                qset.add(id)
                self[id].update_score(node.score + l)
                heappush(queue, self[id])

        ret = self[d].score
        for n in self.values():
            n.score = 1000000
        return ret


class Node(object):

    def __init__(self, id):
        self.id = id
        self.edges = set()
        self.score = 1000000

    def __repr__(self):
        return '<Node {}. score:{} edges:{}>'.format(
            self.id, self.score, [e[0] for e in self.edges])

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def add_edge(self, node, length):
        self.edges.add((node, length))

    def update_score(self, score):
        self.score = min(self.score, score)


graph = Graph()
def main():
    with open('data.txt', 'rt') as f:
        for r in f.read().split('\n'):
            if not r:
                continue
            n, *pairs = r.split('\t')
            graph.add_data(n, pairs)



if __name__ == '__main__':
    main()
