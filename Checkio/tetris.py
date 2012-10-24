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
            for i in range(h, 0, 1):
                if self.data[i-1][j]:
                    break
                self.bottom[j] -= 1
        print(self.top, self.bottom)

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

    def __init__(self, width=10, height=12):
        self.data = []
        self.width = width
        self.height = height
        for i in range(height):
            self.data.append([0]*width)

    def fit(self, figure, position=0):
        field = deepcopy(self.data)
        for field_row in range(self.height, 0, -1):
            for j, fig_row in enumerate(reversed(figure)):
                over = False
                for i, a in enumerate(fig_row):
                    if a and field[field_row-j-1][position+i]:
                        over = True
                        break
                if over:
                    break
            else:
                for j, fig_row in enumerate(reversed(figure)):
                    for i, a in enumerate(fig_row):
                        field[field_row-j-1][position+i] += a
                break
        self.check(field)
        return field

    def put(self, figure, position=0):
        self.data = self.fit(figure, position)
        return self.data

    def check(self, data):
        if sum(data[0]) > 0:
            raise GameOver()
        clear = []
        for i, row in enumerate(data):
            if sum(row) == self.width:
                clear.append(i)
        for c in clear:
            data.pop(c)
            data.insert(0, [0]*self.width)
        return len(clear)


class Game:

    def __init__(self):
        self.field = Field()

    def run(self):
        score = 0
        while True:
            score += 1
            figure = choice(FIGURES)
            for i in range(randrange(0, 4)):
                figure = rotate(figure)
            pprint(figure)
            self.field.put(figure, randrange(0, self.field.width - len(figure[0]) + 1))
            pprint(self.field.data)


def pprint(matrix, time=0.5):
    sleep(time)
    for i in range(len(matrix)):
        print(matrix[i])
    print('\n')
    stdout.flush()


def rotate(figure):
    assert figure, 'Empty figure'
    rotated = []
    for i in range(len(figure[0])):
        r = []
        for j in range(len(figure), 0, -1):
            r.append(figure[j-1][i])
        rotated.append(r)
    return rotated


def main():
    return


def test():
    for f in FIGURES[2:]:
        pprint(f)
        f = Figure(f)
        f.rotate()
        pprint(f.data)
#    g = Game()
#    g.run()


if __name__ == '__main__':
    test()
