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


def figure_to_char(figure):
    return fig_rep[tuple(tuple(i) for i in a)]


def view_to_matrix(view):
    matrix = []
    for row in view.split('\n'):
        if row:
            matrix.append([e == '#' for e in row])
    return matrix


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

    def __eq__(self, other):
        return self.data == other.data


class Field:

    def __init__(self, width=10, height=12, deadline=5):
        self.width = width
        self.height = height
        self.deadline = deadline
        self.data = [[False]*width for i in range(height)]
        self.top = [0]*width
        self.holes = [0]*width
        self.baricades = 0

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
                assert not(self.data[field_row-j-1][position+i] and a)
                self.data[field_row-j-1][position+i] |= a

        if all(self.data[self.deadline]):
            return GAMEOVER

        self.top[position:position+figure.width] = [dive+i for i in figure.top]
#        self.holes += sum(abs(sum(a)) for a in zip(top_slice, figure.bottom, [-dive]*figure.width))
        for i in range(figure.width):
            holes = top_slice[i] + figure.bottom[i] - dive
            if holes:
                self.holes[position+i] += abs(holes)
            if self.holes[position+i]:
                self.baricades += figure.top[i] + figure.bottom[i]

        clear = []
        for i, row in enumerate(self.data):
            if sum(row) == self.width:
                clear.append(i)
        for c in clear:
            self.data.pop(c)
            self.data.insert(0, [False]*self.width)

        if clear:
            self.calc_holes()
            self.calc_baricades()
            self.top = [self.deadline+1]*self.width
            for j in range(self.width):
                for i in range(self.height):
                    if self.data[i][j]:
                        break
                    self.top[j] -= 1

        a = 0.6
        b = 1
        c = 10
        d = 0.5
        p = 1.5
        return 100 + a*sum(self.holes) + b*max(self.top) + d*sum(self.top) - c*(len(clear)+1)**2

    def calc_holes(self):
        self.holes = [0]*self.width
        for i in range(self.width):
            found = False
            for j in range(self.height):
                if found and not self.data[j][i]:
                    self.holes[i] += 1
                if self.data[j][i]:
                    found = True

    def calc_baricades(self):
        self.baricades = 0
        for i in range(self.width):
            if not self.holes[i]:
                continue
            found = False
            for j in reversed(range(self.height)):
                if found and self.data[j][i]:
                    self.baricades += 1
                if not self.data[j][i]:
                    found = True

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


# test
figures = list(map(view_to_matrix, [
"""
.##
##.
""",
"""
##
.#
.#
""",
"""
#
#
#
#
"""
]))

field = Field(5, 6, 5)
field.put(Figure(figures[1]))
field.put(Figure(figures[1]), 1)
field.put(Figure(figures[1]), 2)

assert field.data == view_to_matrix("""
.....
..##.
.###.
####.
.##..
.#..."""), 'Put'

assert field.top == [3, 4, 5, 5, 0], 'Top 1'
assert field.holes == [2, 0, 1, 2, 0], 'Holes 1'
assert field.baricades == 8, 'Baricades 1'

field.put(Figure(figures[2]), 4)

assert field.data == view_to_matrix("""
.....
.....
..##.
.####
.##.#
.#..#"""), 'Clear'

assert field.top == [0, 3, 4, 4, 3], 'Top after clear'
assert field.holes == [0, 0, 1, 2, 0], 'Holes after clear'
assert field.baricades == 5, 'Baricades after clear'

field.put(Figure(figures[1]))

assert field.data == view_to_matrix("""
##...
.#...
.###.
.####
.##.#
.#..#"""), 'Mega hole'
assert field.holes == [5,0,1,2,0], 'Big holes'
assert field.baricades == 6, 'Big hole Baricades'


field = Field(5, 6, 5)
field.put(Figure(figures[1]))
field.put(Figure(figures[1]))
assert field.data == view_to_matrix("""
##...
.#...
.#...
##...
.#...
.#..."""), 'two holes'
assert field.holes == [4,0,0,0,0], 'Two holes'
assert field.baricades == 2, 'Two hole Baricades'

