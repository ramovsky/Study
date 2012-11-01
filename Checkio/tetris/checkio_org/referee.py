class FailTest(Exception):

    def __init__(self, data, *args, **kwargs):
        super(FailTest, self).__init__(*args, **kwargs)
        self.data = data

    def __str__(self):
        return 'Fail Test: %s' % self.data

class DoneTest(Exception):

    def __init__(self, data, *args, **kwargs):
        super(DoneTest, self).__init__(*args, **kwargs)
        self.data = data

    def __str__(self):
        return 'Done Test: %s' % self.data

def badge_info():
    pass

#### clear code ####
import copy
import random
import re

MAP = None
KNOW_NEXT = None
FIGURES = None
POSITION = None
SCORE = None
CURFIGURE = None

LEFT, RIGHT = 'L', 'R'
CLOCKWISE, ANTICLOCKWISE = 'C', 'A'
#3.2
def figure_width(figure):
    return max(map(len, figure))

def turn_figure_clockwise(figure):
    new_figure = []
    for j in range(len(figure[0])):
        new_figure.append([])
        for i in reversed(range(len(figure))):
            new_figure[j].append(figure[i][j])
    return new_figure


def turn_figure_anticlockwise(figure):
    new_figure = []
    col_count = len(figure[0])
    for j in reversed(range(col_count)):
        new_figure.append([])
        for i in range(len(figure)):
            new_figure[col_count - j - 1].append(figure[i][j])
    return new_figure


def turn_figure(figure, clockwise=True):
    if clockwise:
        return turn_figure_clockwise(figure)
    return turn_figure_anticlockwise(figure)

def gen_map(width, height):
    return [[False] * width for _ in range(height)]


def gen_checkio(data):
    clockwise = random.random() > .5
    turn_count = random.randint(0, 2)
    figure = random.choice(data['figures'])
    for _ in range(turn_count):
        figure = turn_figure(figure, clockwise)
    return figure

def initial_checkio(next_in):
    global MAP
    global KNOW_NEXT
    global FIGURES
    global POSITION
    global SCORE
    global CURFIGURE

    width, height = next_in['width'], next_in['height']
    MAP = gen_map(width, height)
    FIGURES = next_in['figures']
    POSITION = next_in['position']
    SCORE = 0

    KNOW_NEXT = []
    for item in range(next_in['know_next']):
        KNOW_NEXT.insert(0,random.choice(FIGURES))

    CURFIGURE = random.choice(FIGURES)
    return {
        'clear': [],
        'stack': KNOW_NEXT,
        'map': view_map(MAP),
        'figure': CURFIGURE,
        'score':SCORE
    }


def put_figure(figure, gmap, x_position):
    height = len(gmap)
    start_y = y_position = height - 1 - len(figure)
    new_map = copy.deepcopy(gmap)
    while y_position >= 0:
        cur_map = copy.deepcopy(gmap)
        good_position = True
        for i, row in enumerate(reversed(figure)):
            for j, el in enumerate(row):
                if not el:
                    continue
                if el and gmap[y_position + i][x_position + j]:
                    good_position = False
                    break
                if el:
                    cur_map[y_position + i][x_position + j] = el
        if not good_position:
            if y_position == start_y:
                return False, new_map
            return True, new_map
        y_position -= 1
        new_map = copy.deepcopy(cur_map)
    return True, new_map


def burn_lines(gmap):
    num_rows = [i for i, row in enumerate(gmap) if all(row)]
    gmap = [row for row in gmap if not all(row)]
    count = len(num_rows)
    for _ in range(count):
        gmap.append([False] * len(gmap[0]))
    return num_rows, gmap



def view_map(gmap, width=None):
    if width is None:
        width = len(gmap[0])
    empty_row = [False] * width
    result_map = [row for row in gmap if any(row)]
    result_map.append(empty_row)
    return result_map

def checkio(next_in):
    global MAP
    global KNOW_NEXT
    global FIGURES
    global POSITION
    global SCORE
    global CURFIGURE



    if not isinstance(next_in, str):
        raise FailTest('checkio() function must return string')

    next_in = next_in.upper()

    if re.search('[^%s]' % ''.join((LEFT, RIGHT, CLOCKWISE,
ANTICLOCKWISE)), next_in, re.I):
        raise FailTest('Got invalid params')

    figure = CURFIGURE
    position = POSITION


    position -= next_in.count(LEFT)
    position += next_in.count(RIGHT)
    clockwises = next_in.count(CLOCKWISE) - next_in.count(ANTICLOCKWISE)

    for i in range(abs(clockwises)):
        figure = turn_figure(figure, clockwises > 0)

    if position < 0 or position + figure_width(figure) > len(MAP[0]):
        raise FailTest('Wrong position')
    put, MAP = put_figure(figure, MAP, position)
    if not put:
        raise DoneTest(SCORE)

    clear, MAP = burn_lines(MAP)
    SCORE += len(clear)
    CURFIGURE = KNOW_NEXT.pop()
    KNOW_NEXT.insert(0, random.choice(FIGURES))

    return {
        'clear': clear,
        'stack': KNOW_NEXT,
        'map': view_map(MAP),
        'figure': CURFIGURE,
        'score':SCORE
    }