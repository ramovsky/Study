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

MAPS = {
    1: [(0, 100),  (1000, 500),  (1500, 100),  (3000, 100),  (5000, 1500),  (6999, 1000)],
    2: [(0, 100),  (1000, 500),  (1500, 1500),  (3000, 1000),  (4000, 150),  (5500, 150),  (6999, 800)],

    3: [(0, 100),  (1000, 500),  (1500, 100),  (3000, 100),  (3500, 500),  (3700, 200),  (5000, 1500),  (5800, 300),  (6000, 1000),  (6999, 2000)],
    4: [(0, 100),  (1000, 500),  (1500, 1500),  (3000, 1000),  (4000, 150),  (5500, 150),  (6999, 800)],
    5: [(0, 1000),  (300, 1500),  (350, 1400),  (500, 2000),  (800, 1800),  (1000, 2500),  (1200, 2100),  (1500, 2400),  (2000, 1000),  (2200, 500),  (2500, 100),  (2900, 800),  (3000, 500),  (3200, 1000),  (3500, 2000),  (3800, 800),  (4000, 200),  (5000, 200),  (5500, 1500),  (6999, 2800)],
    6: [(0, 1000),  (300, 1500),  (350, 1400),  (500, 2100),  (1500, 2100),  (2000, 200),  (2500, 500),  (2900, 300),  (3000, 200),  (3200, 1000),  (3500, 500),  (3800, 800),  (4000, 200),  (4200, 800),  (4800, 600),  (5000, 1200),  (5500, 900),  (6000, 500),  (6500, 300),  (6999, 500)],

    7: [(0, 450),  (300, 750),  (1000, 450),  (1500, 650),  (1800, 850),  (2000, 1950),  (2200, 1850),  (2400, 2000),  (3100, 1800),  (3150, 1550),  (2500, 1600),  (2200, 1550),  (2100, 750),  (2200, 150),  (3200, 150),  (3500, 450),  (4000, 950),  (4500, 1450),  (5000, 1550),  (5500, 1500),  (6000, 950),  (6999, 1750)],
    8: [(0, 1800),  (300, 1200),  (1000, 1550),  (2000, 1200),  (2500, 1650),  (3700, 220),  (4700, 220),  (4750, 1000),  (4700, 1650),  (4000, 1700),  (3700, 1600),  (3750, 1900),  (4000, 2100),  (4900, 2050),  (5100, 1000),  (5500, 500),  (6200, 800),  (6999, 600)]}


def dist(p1, p2):
    return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**.5


def points2plot(points):
    xs = [x for x, y in points]
    ys = [y for x, y in points]
    return xs, ys


def bezier(time, points):
    l = len(points)
    assert l > 1
    if l == 2:
        p1, p2 = points
        x = p1.x + (p2.x - p1.x)*time
        y = p1.y + (p2.y - p1.y)*time
        return Point(x, y)

    new_points = [bezier(time, points[i-1: i+1]) for i in range(1, l)]
    return bezier(time, new_points)


class Bezier:

    def __init__(self, points):
        assert len(points) > 1
        self.points = points

    def get(self, time):
        return bezier(time, self.points)

    def curve(self, n=20):
        return [bezier(i/n, self.points) for i in range(n)]


class Vector:

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return '<Vector X:{:.2f} Y:{:.2f}>'.format(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __eq__(self, other):
        return self.x, self.y == other.x, other.y

    def len(self):
        return (self.x**2, self.y**2)**.5

    @property
    def angle(self):
        return degrees(atan(self.x/self.y))

    @classmethod
    def from_points(cls, start, end):
        return cls(end.x - start.x, end.y - start.y)


class Ship:

    def __init__(self, x, y, angle=0, vs=0, hs=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.vs = vs
        self.hs = hs

    def __repr__(self):
        return '<Ship X:{:.2f} Y:{:.2f} A:{:.2f} VS:{:.2f} HS:{:.2f}>'.format(
            self.x, self.y, self.angle, self.vs, self.hs)

    def step(self, angle, power):
        da = angle - self.angle
        da = min(max(da, -15), 15)
        self.angle += da
        self.vs += power * cos(radians(self.angle)) + G
        self.hs += -power * sin(radians(self.angle))
        self.x += self.hs
        self.y += self.vs

    @property
    def position(self):
        return Point(self.x, self.y)

    @property
    def status(self):
        return self.x, self.y, self.vs, self.hs

    @property
    def speed(self):
        return Vector(self.hs, self.vs)

    def aim(self, point):
        return Vector.from_points(self.position, point)


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
        print(bezier(.95, (Point(0, 0), Point(1, 1), Point(1, 2))))
        print(bezier(.95, (Point(0, 0), Point(1, 2))))

    def test_ship_angle(self):
        ship = Ship(100, 100)
        ship.step(20, 4)
        self.assertEqual(15, ship.angle)
        ship.step(-20, 4)
        self.assertEqual(0, ship.angle)
        print(ship)


if __name__ == '__main__':
    unittest.main()
