from random import randint, random, choice
from copy import deepcopy


GAMEOVER = 100000

i = 0

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

    def __init__(self, width=10, height=12, deadline=5):
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

        if all(self.data[self.deadline]):
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

        a = 3
        b = 0.5
        c = 10
        d = 0.05
        return 100 + a*holes(self.data) + b*max(self.top) + d*sum(self.top) - c*(len(clear)+1)**2

best = (None, GAMEOVER)


class Node:
    '''Decision tree node'''

    def __init__(self, field, parent, move=None):
        self.field = field
        self.penalty = GAMEOVER
        self.children = []
        self.parent = parent
        self.encode_move(move)

    def update(self, figure, position):
        self.penalty = self.field.put(figure, position)
        return self.penalty

    def expand(self, stack):
        if not stack:
            return
        global best
        figure = stack[0]
        check = []
        work = {}
        check.append(figure)
        work[0] = figure
        for i in range(1, 4):
            figure = rotate(figure)
            if figure not in check:
                check.append(figure)
                work[i] = figure

        for r, f in work.items():
            figure = Figure(f)
            for i in range(self.field.width - figure.width + 1):
                node = Node(deepcopy(self.field), self, (r, i))
                penalty = node.update(figure, i)
                self.children.append((r, i, node, penalty))
                if best[1] > penalty:
                    best = (node, penalty)

        self.children = sorted(self.children, key=lambda a: a[-1])
        for r, pos, node, score in self.children[:len(stack)]:
            node.expand(stack[1:])

    def encode_move(self, move):
        if not move:
            self.move = ''
            return
        rotation, position = move
        if position > 4:
            self.move = 'R'*(position - 4) + 'C'*rotation
        else:
            self.move = 'L'*(4 - position) + 'C'*rotation


class Tree:
    '''Decision tree'''

    def __init__(self):
        self.root = Node(Field(), 'root')

    def move(self, next, stack):
        self.root.expand([next] + stack)


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


tree = Tree()


def checkio(args):
    '''
    Clear - list of numbers of cleared rows.
    Map - map.
    Stack - list of future figures.
    Figure - current figure play with.

    Return value:
    L - left, R - right.
    C - turn clockwise, A - anticlockwise.
    '''
    global i
    i += 1
    print(i)
    clear = args['clear']
    field = args['map']
    future_figures = args['stack']
    figure = args['figure']

    tree.move(figure, future_figures)
    node = best[0]
    while 1:
        print("+++++", node.move)
        if node.parent == 'root':
            return node.move
        node = node.parent
    return ''
