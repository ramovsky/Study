from random import choice, randrange
from copy import deepcopy
from time import sleep
from sys import stdout


FIGURES = (
        (
            (1,),
            (1,),
            (1,),
            (1,),
            ),
        (
            (1,1),
            (1,1),
            ),
        (
            (1,1),
            (1,0),
            (1,0),
            ),
        (
            (1,1),
            (0,1),
            (0,1),
            ),
        (
            (1,0),
            (1,1),
            (1,0),
            ),
        (
            (1,0),
            (1,1),
            (0,1),
            ),
        (
            (0,1),
            (1,1),
            (1,0),
            ),
        )

GAMEOVER = 100000


class GameOver(Exception):
    '''Game over'''


class Figure:

    def __init__(self, matrix):
        self.data = matrix
        self.updte_profile()
        self.width = len(matrix[0])
        self.height = len(matrix)

    def updte_profile(self):
        self.width = w = len(self.data[0])
        self.height = h = len(self.data)
        self.top = [h] * w
        self.bottom = [0] * w
        for j in range(w):
            for i in range(h):
                if self.data[i][j]:
                    break
                self.top[j] -= 1
            for i in range(h, 0, -1):
                if self.data[i-1][j]:
                    break
                self.bottom[j] -= 1

    def rotate(self):
        rotated = []
        for i in range(self.width):
            r = []
            for j in range(self.height, 0, -1):
                r.append(self.data[j-1][i])
            rotated.append(r)
        self.data = rotated
        self.updte_profile()
        return rotated

    def __eq__(self, other):
        return self.data == other.data


class Field:

    def __init__(self, width=10, height=12, deadline=0):
        self.data = []
        self.width = width
        self.height = height
        self.deadline = deadline
        for i in range(height):
            self.data.append([0]*width)
        self.top = [0]*width

    def put(self, figure, position=0):

        top_slice = self.top[position: position+figure.width]
        dive = max(map(sum, zip(top_slice, figure.bottom)))
        field_row = self.height - dive
        for j, fig_row in enumerate(reversed(figure.data)):
            for i, a in enumerate(fig_row):
                self.data[field_row-j-1][position+i] += a

        if sum(self.data[self.deadline]) > 0:
            raise GameOver()
            return GAMEOVER

        clear = []
        for i, row in enumerate(self.data):
            if sum(row) == self.width:
                clear.append(i)
        for c in clear:
            self.data.pop(c)
            self.data.insert(0, [0]*self.width)
        self.top = [self.height] * self.width
        for j in range(self.width):
            for i in range(self.height):
                if self.data[i][j]:
                    break
                self.top[j] -= 1

        a = 1
        b = 3
        c = 10
        d = 0.5
        return a*holes(self.data) + b*max(self.top) + d*sum(self.top) - c*len(clear)

cuted = 0
puted = 0

class Node:
    '''Decision tree node'''

    def __init__(self, field):
        self.field = field
        self.penalty = GAMEOVER
        self.children = {}

    def update(self, figure, position):
        self.penalty = self.field.put(figure, position)
        return self.penalty

    def expand(self, stack=None):
        if stack:
            figures = [stack[0]]
        else:
            figures = FIGURES
        check = []
        work = {}
        for f in figures:
            check.append(f)
            work[0] = f
            for i in range(1, 4):
                f = rotate(f)
                if f not in check:
                    check.append(f)
                    work[i] = f
        min_penalty = GAMEOVER
        for r, f in work.items():
            figure = Figure(f)
            for i in range(self.field.width - figure.width + 1):
                node = Node(deepcopy(self.field))
                try:
                    min_penalty = min(min_penalty, node.update(figure, i))
                except GameOver:
                    continue

                self.children[(r, i)] = node
        global cuted, puted
        if stack:
            for child in self.children.values():
                if child.penalty < 1.4*min_penalty:
                    node.expand(stack[1:])
                    puted += 1
                else:
                    cuted += 1


class Tree:
    '''Decision tree'''

    def __init__(self, stack):
        self.best_move = None
        self.root = Node(Field())
        self.root.expand(stack)
        print(puted, cuted)

    def move(self, next):
        self.root = self.root.children[next]


class Game:

    def __init__(self):
        self.field = Field()

    def run(self):
        score = 0
        while True:
            score += 1
            figure = Figure(choice(FIGURES))
            for i in range(randrange(0, 4)):
                figure.rotate()
            pprint(figure.data)
            self.field.put(figure, randrange(0, self.field.width - figure.width) + 1)
            pprint(self.field.data)


def holes(matrix):
    w = len(matrix[0])
    h = len(matrix)
    count = 0
    for i in range(w):
        found = False
        for j in range(h):
            if found and not matrix[j][i]:
                count += 1
            if matrix[j][i]:
                found = True
    return count


def rotate(data):
    rotated = []
    w = len(data[0])
    h = len(data)
    for i in range(w):
        r = []
        for j in range(h, 0, -1):
            r.append(data[j-1][i])
        rotated.append(r)
    return rotated


def pprint(matrix, time=0):
    sleep(time)
    for row in matrix:
        print(''.join(map(str, row)))
    stdout.flush()


def main():
    tree = Tree([choice(FIGURES) for i in range(1)])
    print_tree(tree.root)

def print_tree(node, i=0):
    print(i)
    for k, v in node.children.items():
        if v.children:
            print(v.children.keys())
            print_tree(v, i+1)

def test():
    field = Field()
    while 1:
        cmd, *args = input("\nEnter command: ").split(' ')
        if not cmd:
            cmd = 'move'
        if cmd == 'new':
            field = Field()
            print('done')
        elif cmd == 'next':
            figure = Figure(choice(FIGURES))
            pprint(figure.data)
        elif cmd == 'rot':
            figure.rotate()
            pprint(figure.data)
        elif cmd == 'put':
            field.put(figure, int(args[0]))
            pprint(field.data)
        elif cmd == 'fit':
            fld = field.fit(figure, int(args[0]))
            print(holes(fld), field.check(fld))
        elif cmd == 'top':
            pprint(field.data)
            print('top', field.top)
        elif cmd == 'move':
            figure = Figure(choice(FIGURES))
            pprint(figure.data)
            m = (10000, 0, 0)
            for i in range(4):
                for j in range(field.width - figure.width + 1):
                    p = penalty(field, figure, j)
                    if p < m[0]:
                        m = (p, i, j)
                figure.rotate()
            for i in range(m[1]):
                figure.rotate()
            print(m)
            field.put(figure, m[2])
            pprint(field.data)
        elif cmd == 'exit':
            break


if __name__ == '__main__':
    main()
