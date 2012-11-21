import itertools

def player(data):
    print('player', data)

def referee(data):
    print('\nreferee')
    chs = [' . ', ' # ']
    height = len(data['map'])
    width = len(data['map'][0])
    print("Next three:")
    stack = [[[el for el in row] + [False, False] for row in figure] for figure in reversed(data['stack'])]


    combined =  [[row if row is not None else [False]*len(stack[j][0])
                                            for j, row in enumerate(rows)]
                      for i, rows in enumerate(itertools.zip_longest(*stack))]
    stack_figure = [itertools.chain(*row) for row in combined]
    print('')
    figure = data['figure']
    for row in stack_figure:
        print(''.join([chs[el] if el else '   ' for el in row]))
    print('')
    for row in figure:
        print(' \t|', ' . ' * 3, '.', ''.join([chs[el] if el else '   ' for el in row]),'.',  ' . ' * (width - len(figure[0]) - 5), '|')
    print('')
    for i, row in enumerate(reversed(data['map'])):
        print('%d.\t|' % (height - i - 1), ''.join([chs[el] for el in row]), '|', height - i - 1 in data['clear'] and ' * ' or '')
    print(' \t ', '_' * 3 * width)
    print(' \t ', ''.join([' %d ' % i for i in range(width)]))