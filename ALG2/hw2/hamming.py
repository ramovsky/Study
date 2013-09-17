from random import shuffle

SIZE = 32
to_bin = lambda i: '{:.>7}'.format(bin(i)[2:])


def hamming_distance(s1, s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(to_bin(s1), to_bin(s2)))


def wide_print(*pairs):
    s = ''
    previous = [p[0] for p in pairs]
    for i, p in enumerate(zip(*pairs)):
        s = '{:>3}\t'.format(i)
        for l, e in zip(previous, p):
            s += '{} {} {:<3}\t'.format(to_bin(l^e), to_bin(e), e)
        print(s)
        previous = p


def main():
    lst = list(range(SIZE))

    lst2 = [0]
    while len(lst2) < SIZE:
        for e in lst:
            if e in lst2:
                continue
            if hamming_distance(lst2[-1], e) == 1:
                lst2.append(e)
                lst.remove(e)
                break
        else:
            lst.append(lst2.pop())

    lst = list(range(SIZE))
    wide_print(lst, lst2)


if __name__ == '__main__':
    main()
