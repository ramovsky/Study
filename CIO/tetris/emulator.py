GAMEOVER = 100000


class Figure:

    def __init__(self, matrix):
        self.data = matrix
        self.updte_profile()
        self.width = len(matrix[0])
        self.height = len(matrix)

    def __repr__(self):
        ret = '\n'
        addition = ['top: {}'.format(self.top), 'Figure']        
        for row in self.data:
            ret += ''.join('#' if i else '.' for i in row)
            ret += '\t{}\n'.format(addition.pop()) if addition else '\n'
        return ret

    def updte_profile(self):
        self.width = w = len(self.data[0])
        self.height = h = len(self.data)
        self.top = [h] * w
        self.bottom = [0] * w
        for j in range(w):
            for i in range(h):
                if self.data[i][j]:
                    break
                self.top[j] -= 1
            for i in range(h, 0, -1):
                if self.data[i-1][j]:
                    break
                self.bottom[j] -= 1

    def __eq__(self, other):
        return self.data == other.data


class Field:

    def __init__(self, width=10, height=12, deadline=5):
        self.width = width
        self.height = height
        self.deadline = deadline
        self.data = [[False]*width for i in range(height)]
        self.top = [0]*width
        self.holes = [0]*width
        self.barricades = 0

    def __repr__(self):
        ret = '\n'
        addition = ['top: {}'.format(self.top), 'Field']
        for row in self.data:
            ret += ''.join('#' if i else '.' for i in row)
            ret += '\t{}\n'.format(addition.pop()) if addition else '\n'
        return ret

    def put(self, figure, position=0):
        top_slice = self.top[position: position+figure.width]
        dive = max(map(sum, zip(top_slice, figure.bottom)))
        field_row = self.height - dive

        for j, fig_row in enumerate(reversed(figure.data)):
            for i, a in enumerate(fig_row):
                try:
                    assert not(self.data[field_row-j-1][position+i] and a)
                except AssertionError:
                    from IPython.core.debugger import Pdb
                    Pdb().set_trace()
                self.data[field_row-j-1][position+i] |= a

        if any(self.data[self.deadline]):
            return GAMEOVER

        clear = self.clear()
        if not clear:
            # More light update for top, holes and barricades
            self.top[position:position+figure.width] = [dive+i for i in figure.top]

            for i in range(figure.width):
                holes = top_slice[i] + figure.bottom[i] - dive
                if holes:
                    self.holes[position+i] += abs(holes)
                if self.holes[position+i]:
                    self.barricades += figure.top[i] + figure.bottom[i]

        assert [i for i in self.top if i < 0] == [], 'Negative top'

        a = 0.6
        b = 1
        c = 10
        d = 0.5
        p = 1.5
        return 100 + a*sum(self.holes) + b*max(self.top) + d*sum(self.top) - c*(clear+1)**2

    def clear(self):
        cleared = []
        for i, row in enumerate(self.data):
            if sum(row) == self.width:
                cleared.append(i)
        for c in cleared:
            self.data.pop(c)
            self.data.insert(0, [False]*self.width)

        if cleared:
            # Updating top
            self.top = [self.height]*self.width
            for j in range(self.width):
                for i in range(self.height):
                    if self.data[i][j]:
                        break
                self.top[j] -= i

            # Updating holes
            self.holes = [0]*self.width
            for i in range(self.width):
                found = False
                for j in range(self.height):
                    if found and not self.data[j][i]:
                        self.holes[i] += 1
                    if self.data[j][i]:
                        found = True

            # Updating barricades
            self.barricades = 0
            for i in range(self.width):
                if not self.holes[i]:
                    continue
                found = False
                for j in reversed(range(self.height)):
                    if found and self.data[j][i]:
                        self.barricades += 1
                    if not self.data[j][i]:
                        found = True

        return len(cleared)
