N = 1000000000

def solution(A):
    # write your code in Python 2.6
    ret = 0
    inc = 0
    for e in A:
        if e == 0:
            inc += 1
        else:
            ret += inc
        if ret > N:
            return -1

    return ret


def main():
    assert solution([0,1,0,1,1]) == 5


if __name__ == '__main__':
    main()
