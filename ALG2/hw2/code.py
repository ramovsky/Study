import sys


def bin2gray(i):
    return i//2 ^ i


def hamming_distance(s1, s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def main():

    if sys.argv[-1] == '3':
        with open('edges.txt', 'rt') as f:
            pass

    else:
        lst = set()
        with open('clustering_big.txt', 'rt') as f:
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                b = r.replace(' ', '')
                i = int(b, 2)
                lst.add((i, b))

        clusters = 0
        while lst:
            c = lst.pop()
            lst = sorted(lst, key=lambda x: hamming_distance(x[1], c[1]))
            clusters += 1
            print(clusters, len(lst))
            for i, l in enumerate(lst):
                if hamming_distance(l[1], c[1]) > 2:
                    break
            lst = lst[i:]


if __name__ == '__main__':
    main()
