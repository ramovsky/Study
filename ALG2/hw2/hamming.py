from random import shuffle

SIZE = 32
to_bin = lambda i: '{:.>7}'.format(bin(i)[2:])

def int2gray(i):
    return i//2 ^ i


def gray2int(g):
    mask = g//2
    while mask:
        g = g ^ mask
        mask = mask//2
    return g


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

    lst = sorted(lst, key=lambda x: gray2int(x))

    for i in lst:
        print(i, int2gray(i), to_bin(i))


if __name__ == '__main__':
    main()
