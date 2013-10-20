import pickle
import sys
from collections import deque

sys.setrecursionlimit(1000000)


class Graph(object):

    def __init__(self, size):
        self.nodes = {}
        self.size = size

    def __repr__(self):
        return '<Graph with {} nodes>'.format(self.size)

    def get_node(self, id):
        node = self.nodes.get(id)
        if node is None:
            node = Node(id)
            self.nodes[id] = node
        return node

    def add_data(self, origin, distination):
        o = self.get_node(-origin)
        d = self.get_node(distination)
        o.set_out(d.id)
        d.set_in(o.id)
        o = self.get_node(origin)
        d = self.get_node(-distination)
        o.set_out(d.id)
        d.set_in(o.id)

    def calc_finish(self):
        print('First pass')
        ft = 0
        q = deque()
        first = list(sorted(self.nodes.values(), key=lambda x: x.id, reverse=True))
        for node in first:
            if node.bck:
                continue
            self.dfs(node, q, False)
            while q:
                ft += 1
                n = q.pop()
                n.set_finish(ft)

        print('Second pass')
        second = list(sorted(self.nodes.values(), key=lambda x: x.finish, reverse=True))
        for node in second:
            if node.fwd:
                continue
            q = deque()
            scc = {node.id}
            self.dfs(node, q, True, scc)

    def dfs(self, node, queue, fw=True, scc=None):
        queue.append(node)
        if fw:
            node.fwd = True
            for n in node.outgoing:
                n = self.get_node(n)
                if n.fwd:
                    continue
                scc.add(n.id)
                if -n.id in scc:
                    raise ValueError('unsatisfied')
                self.dfs(n, queue, fw, scc)
        else:
            node.bck = True
            for n in node.incoming:
                n = self.get_node(n)
                if n.bck:
                    continue
                self.dfs(n, queue, fw)


class Node(object):

    def __init__(self, id):
        self.id = id
        self.finish = None
        self.incoming = set()
        self.outgoing = set()
        self.fwd = False
        self.bck = False

    def __repr__(self):
        return '<Node {}. in:{} out:{}>'.format(self.id, self.incoming, self.outgoing)

    def set_finish(self, value):
        self.finish = value

    def set_in(self, id):
        self.incoming.add(id)

    def set_out(self, id):
        self.outgoing.add(id)


def main():
    count = None
    with open(sys.argv[1], 'rt') as f:
        for r in f.read().split('\n'):
            if not r:
                continue
            if count is None:
                count = int(r)
                graph = Graph(count)
            else:
                graph.add_data(*tuple(map(int, r.split())))
    try:
        graph.calc_finish()
    except ValueError:
        print('unsatisfied')
    else:
        print('satisfied')


if __name__ == '__main__':
    main()
