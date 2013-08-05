import pickle
from random import choice, shuffle


class Graph(object):

    def __init__(self):
        self.nodes = {}

    def __repr__(self):
        return '<Graph with {} nodes>'.format(len(self.nodes))

    def get_node(self, id):
        node = self.nodes.get(id)
        if node is None:
            node = Node(id)
            self.nodes[id] = node
        return node

    def add_data(self, origin, distination):
        o = self.get_node(origin)
        d = self.get_node(distination)
        o.set_out(d.id)
        d.set_in(o.id)

    def calc_finish(self):
        pass


class Node(object):

    def __init__(self, id):
        self.id = id
        self.finish = None
        self.incoming = set()
        self.outgoing = set()

    def __repr__(self):
        return '<Node {}. in:{} out:{}>'.format(self.id, self.incoming, self.outgoing)

    def set_finish(self, value):
        self.finish = value

    def set_in(self, id):
        self.incoming.add(id)

    def set_out(self, id):
        self.outgoing.add(id)



def main():
    try:
        with open('graph', 'rb') as f:
            graph = pickle.load(f)
    except:
        graph = Graph()
        with open('SCC.txt', 'rt') as f:
            i = 0
            for r in f.read().split('\n'):
                if not r:
                    continue
                graph.add_data(*tuple(map(int, r.split(' ', 1))))
                i += 1
                if i < 0:
                    break

        with open('graph', 'wb') as f:
            pickle.dump(graph, f)

    print(graph.nodes[1])


if __name__ == '__main__':
    main()
