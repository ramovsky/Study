from math import acos, degrees


def get_cos(sides):
    a, b, c = sides
    return (b**2 + c**2 - a**2)/2/b/c


def checkio(a, b, c):
    ret = []
    lst = [a, b, c]
    try:
        for i in range(3):
            ret.append(degrees(acos(get_cos(lst))))
            lst.append(lst.pop(0))
    except KeyError:
        return [0 ,0, 0]
    return sorted(ret)


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(4, 4, 4) == [60, 60, 60], "All sides are equal"
    assert checkio(3, 4, 5) == [37, 53, 90], "Egyptian triangle"
    assert checkio(2, 2, 5) == [0, 0, 0], "It's can not be a triangle"
