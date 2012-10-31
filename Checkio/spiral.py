def get_xy(diagonal, element):
    on_diag = min([i for i in diagonal if i > element])
    edge = diagonal.index(on_diag)
    x, y = [edge]*2
    diff = on_diag - element
    sector, shift = diff // edge, diff % edge
    if sector < 2:
        x -= shift
    elif sector < 4:
        x -= 2*edge
        y -= shift
    elif sector < 6:
        x -= 2*edge - shift
        y -= 2*edge
    else:
        y -= 2*edge - shift
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
    print(x_a, y_a, x_b, y_b)
    return 10

if __name__ == '__main__':
#    assert checkio([1, 9]) == 2, "First"
#    assert checkio([9, 1]) == 2, "Reverse First"
#    assert checkio([10, 25]) == 1, "Neighbours"
#    assert checkio([5, 9]) == 4, "Diagonal"
#    assert checio([26, 31]) == 5, "One row"
    assert checkio([50, 16]) == 10, "One more test"
