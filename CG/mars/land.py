import sys
import unittest
from math import *
from collections import namedtuple

# Read init information from standard input, if any
THRUSTS = list(range(5))
SAFE_HS = 20
SAFE_VS = -40
TILT_STEP = 15
G = -3.711


Point = namedtuple('Point', ['x', 'y'])


class Vector:

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return str(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __eq__(self, other):
        return self.x, self.y == other.x, other.y

    @classmethod
    def from_points(cls, start, end):
        return cls(end.x - start.x, end.y - start.y)


def dist(p1, p2):
    return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**.5


def bezier(time, *points):
    l = len(points)
    assert l > 1
    if l == 2:
        p1, p2 = points
        x = p1.x + (p2.x - p1.x)*time
        y = p1.y + (p2.y - p1.y)*time
        return Point(x, y)

    new_points = [bezier(time, *points[i-1: i+1]) for i in range(1, l)]
    print(new_points)
    return bezier(time, *new_points)


def get_target(x, y):
    left, right = flat
    if x <= left.x:
        return Point(left.x + 10, left.y)
    if x >= right.x:
        return Point(right.x - 10, right.y)
    return Point(x, left.y)


def solve(x, y, hs, vs, f, r, p):
    position = Point(x, y)
    target = get_target(x, y)
    vd = position.x - target.x
    hd = position.y - target.y
    s = vd and hd * 1.1 / vd
    tilt = degrees(asin(s))
    if tilt - r > 15:
        tilt = r + 15
    elif tilt - r < -15:
        tilt = r - 15
    if vs < SAFE_VS:
        p = 0
        if vd < 100:
            p = 4
        elif vd < 200:
            p = 3
        elif vd < 500:
            p = 2
        elif vd < 1000:
            p = 1

    return int(tilt), p


"""
N = int(input())
points = []
last = Point(0, -1)
for i in range(N):
    p = Point(*map(int, input().split()))
    points.append(p)
    if p.y == last.y:
        flat = last, p
    last = p

while 1:
    # Read information from standard input
    line = input()
    #print("Debug messages... " + line , file=sys.stderr)

    r, p = solve(*map(int, line.split()))
    print('{} {}'.format(r, p))
"""


class Test(unittest.TestCase):

    def test_vector(self):
        self.assertEqual(Vector(0, 2), Vector(0, 1) + Vector(0, 1))
        self.assertEqual(Vector(-1, 0), Vector(0, 1) - Vector(1, 1))
        self.assertEqual(Vector(1, 1),
                         Vector.from_points(Point(10, 10), Point(11, 11)))

    def test_bezier(self):
        print(bezier(.9, Point(0, 0), Point(1, 1), Point(1, 2)))
        print(bezier(.9, Point(0, 0), Point(1, 2)))
        self.assertEqual(Vector(0, 2), Vector(0, 1) + Vector(0, 1))


if __name__ == '__main__':
    unittest.main()
