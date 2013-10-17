import sys
from random import shuffle
from collections import defaultdict, namedtuple


INF = float('inf')

class Point:

    def __init__(self, id, next, x, y):
        self.id = id
        self.next = next
        self.x = x
        self.y = y

    def __repr__(self):
        return '<P:{} {}>'.format(self.id, self.next.id, self.x, self.y)

def print_i(i, space=5):
    delete = "\b" * space
    print("{0}{1:<{2}}".format(delete, i, space), end="")
    sys.stdout.flush()


def distance(p1, p2):
    return ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**.5


def probe(i, tour):
    min_increment = INF

    for u in tour:
        v = u.next
        increment = distance(u, i) + distance(i, v) - distance(u, v)
        if increment < min_increment:
            min_increment = increment
            insert_after = u

    i.next = insert_after.next
    insert_after.next = i
    tour.append(i)
    return min_increment


def main():
    with open('tsp.txt', 'rt') as f:
        size = None
        points = []
        i = 0
        for r in f.read().split('\n'):
            if not r:
                continue
            elif r == 'stop':
                break
            if size is None:
                size = int(r)
            else:
                points.append(Point(i, None, *map(float, r.split())))
                i += 1

#    dist = 0
#    prev = points[0]
#    for i in (1,5,4,3,2,6,8,7,11,12,13,15,23,24,19,17,20,22,21,18,14,10,9, 0):
#        dist += distance(prev, points[i])
#        prev = points[i]

    min_distance = INF
    work = points[:]
    for i in range(10000):
        shuffle(work)
        point = work[0]
        dist = 0
        tour = [point]
        point.next = point
        for p in work[1:]:
            dist += probe(p, tour)
        if int(dist) == 26442:
            break

    i = 0
    while i < 25:
        print(point, end=' ')
        point = point.next
        i += 1

if __name__ == '__main__':
    main()
