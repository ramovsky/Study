from solver import Tree

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

i = 0
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
    clear = args['clear']
    field = args['map']
    future_figures = args['stack']
    figure = args['figure']
    return tree.move(figure, future_figures)
