import unittest
from emulator import Field, Figure


def view_to_matrix(view):
    matrix = []
    for row in view.split('\n'):
        if row:
            matrix.append([e == '#' for e in row.strip()])
    return matrix

figures = list(map(view_to_matrix, [
"""
.##
##.
""",
"""
##
.#
.#
""",
"""
#
#
#
#
"""
]))

class Base(unittest.TestCase):

    def test_put(self):
        field = Field(5, 6, 5)
        field.put(Figure(figures[1]))
        field.put(Figure(figures[1]), 1)
        field.put(Figure(figures[1]), 2)

        self.assertEqual(field.data, view_to_matrix(
            """
            .....
            ..##.
            .###.
            ####.
            .##..
            .#..."""))

        self.assertEqual(field.top, [3, 4, 5, 5, 0])
        self.assertEqual(field.holes, [2, 0, 1, 2, 0])
        self.assertEqual(field.barricades, 8)

        field.put(Figure(figures[2]), 4)

        self.assertEqual(field.data, view_to_matrix(
            """
            .....
            .....
            ..##.
            .####
            .##.#
            .#..#"""))

        self.assertEqual(field.top, [0, 3, 4, 4, 3])
        self.assertEqual(field.holes, [0, 0, 1, 2, 0])
        self.assertEqual(field.barricades, 5)

        field.put(Figure(figures[1]))

        self.assertEqual(field.data, view_to_matrix(
            """
            ##...
            .#...
            .###.
            .####
            .##.#
            .#..#"""))
        
        self.assertEqual(field.holes, [5,0,1,2,0])
        self.assertEqual(field.barricades, 6)

    def test_two_holes(self):
        field = Field(5, 6, 5)
        field.put(Figure(figures[1]))
        field.put(Figure(figures[1]))
        self.assertEqual(field.data, view_to_matrix(
            """
            ##...
            .#...
            .#...
            ##...
            .#...
            .#..."""))
        self.assertEqual(field.holes, [4,0,0,0,0])
        self.assertEqual(field.barricades, 2)


if __name__ == '__main__':
    unittest.main()
