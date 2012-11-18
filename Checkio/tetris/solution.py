from random import randint, random, choice
from copy import deepcopy

GAMEOVER = 100000

fig_rep = {
 ((True, True, True, True),): 'I',
 ((True, True), (True, True)): 'o',
 ((False, True, True), (True, True, False)): 's',
 ((True, True, False), (False, True, True)): 'z',
 ((False, True, False), (True, True, True)): 'T',
 ((True, False), (True, False), (True, True)): 'L',
 ((False, True), (False, True), (True, True)): 'J'
    }


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
            self.data.append([False]*width)
        self.top = [0]*width

    def __repr__(self):
        ret = ''
        addition = ['top: {}'.format(self.top), 'Field']
        for row in self.data:
            ret += ''.join('#' if i else '.' for i in row)
            ret += '\t{}\n'.format(addition.pop()) if addition else '\n'
        return ret

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

        a = 0.6
        b = 1
        c = 50
        d = 0.5
        p = 1.5
        p_top = [t**p for t in self.top]
        return 100 + a*holes(self.data) + b*max(p_top) + d*sum(p_top) - c*(len(clear)+1)**2


class Node:
    '''Decision tree node'''

    def __init__(self, field, raw_figure=None, move=None):
        self.field = field
        self.penalty = GAMEOVER
        self.best_leave = GAMEOVER
        self.children = []
        self.raw_figure = raw_figure
        self.encode_move(move)
        self.expanded = False

    def __repr__(self):
        ret = ''
        addition = [
            'move: {}'.format(self.move),
            'penalty: {}'.format(self.penalty),
            'expanded: {}'.format(self.expanded),
            'best_leave: {}'.format(self.best_leave),
            'Node']
        for row in self.field.data:
            ret += ''.join('#' if i else '.' for i in row)
            ret += '\t{}\n'.format(addition.pop()) if addition else '\n'
        return ret

    def update(self, figure, position):
        self.penalty = self.field.put(figure, position)
        return self.penalty

    def expand(self, stack):
        if not stack:
            return self.best_leave

        figure = stack[0]

        if self.raw_figure:
            assert self.raw_figure == figure, 'Unexpected next figure'

        if len(stack) > 1:
            raw_figure = stack[1]
        else:
            raw_figure = None

        if not self.expanded:
            self.expanded = True
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
                    node = Node(deepcopy(self.field), raw_figure, (r, i))
                    penalty = node.update(figure, i)
                    self.children.append(node)

            self.children = sorted(self.children, key=lambda c: c.penalty)

        for node in self.children[:len(stack)+1]:
            best_leave = node.expand(stack[1:])
            if self.penalty == GAMEOVER:
                best_leave = GAMEOVER # exclude GameOver nodes
            self.best_leave = best_leave
        if len(stack) == 1:
            return self.children[0].penalty
        return self.best_leave

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
        self.root = Node(Field())

    def move(self, next, stack):
        s = [next] + list(reversed(stack))
        print([fig_rep[tuple(tuple(i) for i in a)] for a in s])
        self.root.expand(s)
        node = sorted(self.root.children, key=lambda c: c.best_leave)[0]
        self.root = node
        return node.move


tree = Tree()
i = 0


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
    clear = args['clear']
    field = args['map']
    future_figures = args['stack']
    figure = args['figure']
    return tree.move(figure, future_figures)
