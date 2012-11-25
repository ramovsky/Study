from random import randint, random, choice
from copy import deepcopy
from emulator import Field, Figure, GAMEOVER


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

best = None

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
        global best
        
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
            if node.penalty == GAMEOVER:
                best_leave = GAMEOVER # exclude GameOver nodes
            self.best_leave = best_leave
        if len(stack) == 1:
            if best.penalty > self.children[0].penalty:
                best = self.children[0]
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
        global best
        best = self.root

    def move(self, next, stack):
        global best
        best.penalty = GAMEOVER
        s = [next] + list(reversed(stack))
        self.root.expand(s)
        node = sorted(self.root.children, key=lambda c: c.best_leave)[0]
        self.root = node
        return node.move

