from random import randint, random

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
    print(i)
    clear = args['clear']
    field = args['map']
    future_figures = args['stack']
    figure = args['figure']
    checks = ['R', 'L']
    check = random() > .5
    if check:
        count = randint(0, 4)
    else:
        count = randint(0, 3)
    return (checks[check] * count)