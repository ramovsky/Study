import sys

class Finish(Exception): pass


def process(board, steps=1):
    print(board, steps)
    idx = board.index('E')
    board = board[:]
    board[idx] = 'C'
    length = len(board)
    if board == ['C']*length:
        return

    if 'S' in board[max(0, idx-5):idx]:
        raise Finish(steps+1)

    for j, l in enumerate(board[:idx]):
        if l == 'C':
            continue

        elif l == 'R':
            for i in range(6):
                if j+i >= length:
                    break
                board[j+i] = 'E'
                print('R clause left')
                process(board, steps+1)
                board[j+i] = 'C'

        elif l == idx-j:
            print('{} clause left'.format(l))
            if idx+l < l and board[idx+l] == 'S':
                raise Finish(steps+1)

            board[j] = 'E'
            process(board, steps+1)

    s = idx + 1
    for j, l in enumerate(board[s:]):
        if l == 'C':
            continue

        elif l == 'R':
            for i in range(6):
                if s+j+i >= length:
                    break
                board[s+j+i] = 'E'
                print('R clause right')
                process(board, steps+1)
                board[s+j+i] = 'C'

        elif l == j+1:
            print('{} clause right'.format(l))
            if idx+l < l and board[idx+l] == 'S':
                raise Finish(steps+1)
            board[j] = 'E'
            process(board, steps+1)


def main():
    board = []
    n = int(raw_input())
    for i in xrange(n):
        n = raw_input()
        try:
            n = int(n)
        except:
            pass
        board.append(n)

    try:
        process(board)
    except Finish as e:
        print(e)
    else:
        print('impossible')


if __name__ == '__main__':
    main()
