from itertools import permutations

def checkio(stones):
    '''
    minimal possible weight difference between stone piles
    '''
    diff = sum(stones)
    for s in permutations(stones):
        m = abs(sum(s[:len(s)//2]) - sum(s[len(s)//2:]))
        if m < diff:
            diff = m
    return diff


if __name__ == '__main__':
    assert checkio([10,10]) == 0, 'First, with equal weights'
    assert checkio([10]) == 10, 'Second, with a single stone'
    assert checkio([5, 8, 13, 27, 14]) == 3, 'Third'
    assert checkio([5,5,6,5]) == 1, 'Fourth'
    assert checkio([12, 30, 30, 32, 42, 49]) == 9, 'Fifth'
    print ('All is ok')
