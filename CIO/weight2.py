from itertools import combinations


def checkio(batteries):
    min_diff = max(batteries)
    for combination_length in range(len(batteries)):
        for variant in combinations(batteries, combination_length):
            print(variant)
            diff = abs(2 * sum(variant) - sum(batteries))
            min_diff = diff if min_diff > diff else min_diff
    return min_diff


if __name__ == '__main__':
    assert checkio([10,10]) == 0, 'First, with equal weights'
    assert checkio([10]) == 10, 'Second, with a single stone'
    assert checkio([5, 8, 13, 27, 14]) == 3, 'Third'
    assert checkio([5,5,6,5]) == 1, 'Fourth'
    assert checkio([12, 30, 30, 32, 42, 49]) == 9, 'Fifth'
    print('All is ok')
