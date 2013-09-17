SIZE = 32
to_bin = lambda i: '{:>7}'.format(bin(i)[2:])


def switch(lst, start, shift, step=4):
    lst = lst[:]
    for i in range(start, SIZE, step):
        j = i + shift
        lst[i], lst[j] = lst[j], lst[i]
    return lst


def move(lst, start, shift, step=4):
    lst = lst[:]
    for i in range(start, SIZE, step):
        j = i + shift
        lst.insert(j, lst.pop(i))
    return lst


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

    if sys.argv[-1] == '3':
        with open('edges.txt', 'rt') as f:
            graph = Graph()
            for r in f.read().split('\n'):
                if not r:
                    continue
                graph.add_data(*map(int, r.split(' ')))


    else:
        lst = list(range(SIZE))
        lst2 = lst[:]
        i = 2
        while i < SIZE:
            i *= 2
            j, k  = i-1, i-2
            lst2[j], lst2[k] = lst2[k], lst2[j]

        wide_print(lst, lst2)



if __name__ == '__main__':
    main()
