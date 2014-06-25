from heapq import heappush, heappop


class Node(object):

    def __init__(self, xy, cost):
        self.xy = xy
        self.cost = cost
        self.neighbours = set()
        self.path = ''

    def __repr__(self):
        return '<Node {}: {}>'.format(self.xy, self.cost)

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def update_path(self, prev):
        diff = [c-p for p, c in zip(prev.xy, self.xy)]
        if diff == [1, 0]:
            self.path = prev.path + 'E'
        elif diff == [-1, 0]:
            self.path = prev.path + 'W'
        elif diff == [0, 1]:
            self.path = prev.path + 'S'
        elif diff == [0, -1]:
            self.path = prev.path + 'N'
        else:
            raise NotImplementedError(diff)

    @property
    def full_cost(self):
        return len(self.path) + self.cost

    def __lt__(self, other):
        return self.full_cost < other.full_cost


class Graph(dict):

    def __init__(self, data):
        w, h = len(data[0])-1, len(data)-1
        self.finish = w-1, h-1
        for i in range(h+1):
            for j in range(w+1):
                if data[i][j] == 0:
                    self._add_node(j, i, ((w-j)**2+(h-i)**2)**.5)

    def __repr__(self):
        buf = '\n'
        w, h = self.finish
        for i in range(h+2):
            for j in range(w+2):
                if (j, i) in self:
                    buf += ' '
                else:
                    buf += 'O'
            buf += '\n'
        return '<Graph: {}>'.format(buf)

    def show_path(self, path, start=(1, 1)):
        cur = start
        steps = {}
        for i, l in enumerate(path):
            cur = tuple(cur)
            if l == 'E':
                steps[cur] = '\u2192'
                cur = [p-n for p, n in zip(cur, (-1, 0))]
            elif l == 'W':
                steps[cur] = '\u2190'
                cur = [p-n for p, n in zip(cur, (1, 0))]
            elif l == 'S':
                steps[cur] = '\u2193'
                cur = [p-n for p, n in zip(cur, (0, -1))]
            elif l == 'N':
                steps[cur] = '\u2191'
                cur = [p-n for p, n in zip(cur, (0, 1))]

        buf = '\n'
        w, h = self.finish
        for i in range(h+2):
            for j in range(w+2):
                if (j, i) in steps:
                    buf += steps[j, i]
                elif (j, i) in self:
                    buf += ' '
                else:
                    buf += 'O'
            buf += '\n'
        print('<Graph: {}>'.format(buf))

    def _add_node(self, x, y, cost):
        xy = x, y
        node = Node(xy, cost)
        self[xy] = node
        neighbour = self.get((x-1, y))
        if neighbour:
            neighbour.add_neighbour(node)
            node.add_neighbour(neighbour)
        neighbour = self.get((x, y-1))
        if neighbour:
            neighbour.add_neighbour(node)
            node.add_neighbour(neighbour)

    def a_star(self, start=(1, 1)):
        src = self[start]
        visited = {src}
        queue = [src]
        while queue:
            node = heappop(queue)
#            from pdb import set_trace; set_trace()
            if node.xy == self.finish:
                return node.path

            for n in node.neighbours:
                if n in visited:
                    continue
                visited.add(n)
                n.update_path(node)
                heappush(queue, n)


def checkio(data):
    g = Graph(data)
    return g.show_path(g.a_star())


#This code using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    print(checkio([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]))
    #be careful with infinity loop
    print(checkio([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]))
    print(checkio([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]))
    print(checkio([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]))
