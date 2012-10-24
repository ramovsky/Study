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


class Field:

    def __init__(self, width=10, height=12, deadline=0):
        self.data = []
        self.width = width
        self.height = height
        self.deadline = deadline
        for i in range(height):
            self.data.append([0]*width)
        self.top = [0]*width

    def fit(self, figure, position=0):
        field = deepcopy(self.data)
        top = self.top[:]
        old_top = self.top[position: position+figure.width]
        dive = max(map(sum, zip(old_top, figure.bottom)))
        field_row = self.height - dive
        for j, fig_row in enumerate(reversed(figure.data)):
            for i, a in enumerate(fig_row):
                field[field_row-j-1][position+i] += a
        return field

    def put(self, figure, position=0):
        self.data = self.fit(figure, position)
        clear, self.top = self.check(self.data)
        return self.data

    def check(self, data):
        if sum(data[self.deadline]) > 0:
            raise GameOver()
        clear = []
        for i, row in enumerate(data):
            if sum(row) == self.width:
                clear.append(i)
        for c in clear:
            data.pop(c)
            data.insert(0, [0]*self.width)
        top = [self.height] * self.width
        for j in range(self.width):
            for i in range(self.height):
                if data[i][j]:
                    break
                top[j] -= 1
        return len(clear), top


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


def pprint(matrix, time=0):
    sleep(time)
    for row in matrix:
        print(''.join(map(str, row)))
    stdout.flush()


def penalty(field, figure, position):
    a = 1
    b = 3
    c = 10
    d = 0.5
    try:
        fld = field.fit(figure, position)
        clr, top = field.check(fld)
    except GameOver:
        return 100000
    return a*holes(fld) + b*max(top) + d*sum(top) - c*clr


def main():
    return


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
    test()
