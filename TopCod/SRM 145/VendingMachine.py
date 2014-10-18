# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect
from collections import defaultdict


class State:

    def __init__(self, prices):
        self.steps = 0
        self._cursor = 0
        self._prices = defaultdict(list)
        self._cells = [map(int, row.split()) for row in prices]
        self._width = len(self._cells[0])
        self.go_high()

    def __repr__(self):
        matrix = ''
        for row in self._cells:
            matrix += '\n' + ''.join('{:>5}'.format(e) for e in row)
        return '<Machine cursor: {}, steps: {}{}>'.format(
            self._cursor, self.steps, matrix)

    def go_high(self):
        if not self._prices:
            for j, row in enumerate(self._cells):
                for i, price in enumerate(row):
                    self._prices[price].append((j, i))

        prices = self._prices[max(self._prices)]
        row, col = prices[0]
        high = self._dist(col), col
        for row, col in prices:
            high = min(high, (self._dist, col))

        dist, self._cursor = high
        self.steps += dist

    def purchase(self, row_col):
        row, col = map(int, row_col.split(','))
        price = self._cells[row][col]
        if price == 0:
            return False

        self._prices[price].remove((row, col))
        if not self._prices[price]:
            del self._prices[price]

        self._cells[row][col] = 0
        self.steps += self._dist(col)
        self._cursor = col
        return True

    def _dist(self, col):
        d = abs(self._cursor - col)
        return min(d, self._width - d)


class VendingMachine:

    def motorUse(self, prices, purchases):
        state = State(prices)
#        print(purchases)
#        print(state)

        last = 0
        for p in purchases:
            coord, time = p.split(':')
            time = int(time)
            diff = time - last
            last = time
            if diff > 4:
#                print('Hight', diff)
                state.go_high()
#                print(state)

            if not state.purchase(coord):
                return -1

#            print(state)

        if len(state._cells) < 2:
            state.go_high()
#        print(state)

        return state.steps


# CUT begin
# TEST CODE FOR PYTHON {{{
import sys, time, math

def tc_equal(expected, received):
    try:
        _t = type(expected)
        received = _t(received)
        if _t == list or _t == tuple:
            if len(expected) != len(received): return False
            return all(tc_equal(e, r) for (e, r) in zip(expected, received))
        elif _t == float:
            eps = 1e-9
            d = abs(received - expected)
            return not math.isnan(received) and not math.isnan(expected) and d <= eps * max(1.0, abs(expected))
        else:
            return expected == received
    except:
        return False

def pretty_str(x):
    if type(x) == str:
        return '"%s"' % x
    elif type(x) == tuple:
        return '(%s)' % (','.join( (pretty_str(y) for y in x) ) )
    else:
        return str(x)

def do_test(prices, purchases, __expected):
    startTime = time.time()
    instance = VendingMachine()
    exception = None
    try:
        __result = instance.motorUse(prices, purchases);
    except:
        import traceback
        exception = traceback.format_exc()
    elapsed = time.time() - startTime   # in sec

    if exception is not None:
        sys.stdout.write("RUNTIME ERROR: \n")
        sys.stdout.write(exception + "\n")
        return 0

    if tc_equal(__expected, __result):
        sys.stdout.write("PASSED! " + ("(%.3f seconds)" % elapsed) + "\n")
        return 1
    else:
        sys.stdout.write("FAILED! " + ("(%.3f seconds)" % elapsed) + "\n")
        sys.stdout.write("           Expected: " + pretty_str(__expected) + "\n")
        sys.stdout.write("           Received: " + pretty_str(__result) + "\n")
        return 0

def run_tests():
    sys.stdout.write("VendingMachine (600 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("VendingMachine.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            prices = []
            for i in range(0, int(f.readline())):
                prices.append(f.readline().rstrip())
            prices = tuple(prices)
            purchases = []
            for i in range(0, int(f.readline())):
                purchases.append(f.readline().rstrip())
            purchases = tuple(purchases)
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(prices, purchases, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1413489852
    PT, TT = (T / 60.0, 75.0)
    points = 600 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
