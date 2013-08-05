from random import choice, shuffle


#kargerMinCut

def main():
    with open('kargerMinCut.txt', 'rt') as f:
        edges = set()
        dset = {}
        for r in f.read().split('\n'):
            if not r:
                continue
            for i, v in enumerate(r.split('\t')):
                if not v:
                    continue
                v = int(v)
                if i == 0:
                    s = v
                    dset[v] = {v}
                else:
                    e = tuple(sorted((s, v)))
                    edges.add(e)

        elist = list(edges)
        shuffle(elist)

        while len(dset) > 2:
            e = elist.pop()
            edges.discard(e)
            v1, v2 = None, None
            for k, v in dset.items():
                if e[0] in v:
                    v1 = k
                if e[1] in v:
                    v2 = k
                if v1 and v2:
                    break
            dset[v1] |= dset.pop(v2)

        l, r = dset
        minc = 0
        for v1, v2 in edges:
            if v1 in dset[l] and v2 in dset[r]:
                minc += 1
            elif v2 in dset[l] and v1 in dset[r]:
                minc += 1
#        print(edges)
#        print(dset)
#        print(minc)
        return minc


if __name__ == '__main__':
    mm = 23
    for i in range(2000):
        mm = min(main(), mm)
    print(mm)
