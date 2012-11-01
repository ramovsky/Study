def get_xy(diagonal, element):
    if element == 1:
        return 0, 0
    on_diag = min([i for i in diagonal if i >= element])
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
    diagonal = [1]
    i = 3
    while diagonal[-1] < max(a, b):
        diagonal.append(i**2)
        i += 2
    x_a, y_a = get_xy(diagonal, a)
    x_b, y_b = get_xy(diagonal, b)
    return abs(x_a - x_b) + abs(y_a - y_b)

if __name__ == '__main__':
    diagonal = [i**2 for i in range(1,20)]
    for i in range(1, 100):
        print('{}\t{}'.format(i, get_xy(diagonal, i)))
    assert checkio([1, 9]) == 2, "First"
    assert checkio([9, 1]) == 2, "Reverse First"
    assert checkio([10, 25]) == 1, "Neighbours"
    assert checkio([5, 9]) == 4, "Diagonal"
    assert checkio([26, 31]) == 5, "One row"
    assert checkio([50, 16]) == 10, "One more test"
    print('Ok')
