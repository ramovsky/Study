from itertools import *

def get_xy(element):
    if element == 1:
        return 0, 0
    diagonal = [(i+1)**2 for i in takewhile(
        lambda i: (i-1)**2 < element, count(step=2)
        )]
    on_diag = max(diagonal)
    edge = diagonal.index(on_diag)
    x, y = [edge]*2
    diff = on_diag - element

    sector, shift = diff // edge, diff % edge
    if sector < 2:
        y -= sector*edge + shift
    elif sector < 4:
        y -= 2*edge
        x -= (sector-2)*edge + shift
    elif sector < 6:
        y -= 2*edge - shift - (sector-4)*edge
        x -= 2*edge
    else:
        x -= 2*edge - shift - (sector-6)*edge
    return x, y


def checkio(data):
    "Find the destination"
    a, b = data
    x_a, y_a = get_xy(a)
    x_b, y_b = get_xy(b)
    return abs(x_a - x_b) + abs(y_a - y_b)


if __name__ == '__main__':
    for i in range(1, 50):
        print('{}\t{}'.format(i, get_xy(i)))
    assert checkio([1, 9]) == 2, "First"
    assert checkio([9, 1]) == 2, "Reverse First"
    assert checkio([10, 25]) == 1, "Neighbours"
    assert checkio([5, 9]) == 4, "Diagonal"
    assert checkio([26, 31]) == 5, "One row"
    assert checkio([50, 16]) == 10, "One more test"
    print('Ok')
