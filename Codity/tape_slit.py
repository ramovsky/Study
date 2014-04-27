
def solution(*A):
    # write your code in Python 2.6
    if len(A) == 2:
        return abs(A[0] - A[1])

    sum_all = sum(A)
    diff = float('inf')
    acc = A[0]
    for e in A[1:]:
        acc += e
        diff = min(diff, abs(2*acc - sum_all))
    return diff


def main():
#    assert solution(1,2,3,4,5) == 3, 'First'
    print(solution(1, -1, 0))
    assert solution(1, -1) == 2, 'Second'


if __name__ == '__main__':
    main()
