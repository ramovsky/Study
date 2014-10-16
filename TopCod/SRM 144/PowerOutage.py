# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect
from collections import defaultdict
from functools import total_ordering
from heapq import heappop, heappush, heapify
from itertools import permutations


INF = float('inf')


@total_ordering
class Node:

    score = INF

    def __init__(self, id):
        self.id = id
        self.edges = {}

    def add_edge(self, id, length):
        self.edges[id] = length

    def update_score(self, score):
        self.score = min(self.score, score)

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score

    def __repr__(self):
        return '<Node {}. sc:{} ed:{}>'.format(
            self.id, self.score, self.edges)


class Tree(dict):

    def __init__(self, start, end, length):
        self._cache = {}
        self.leaves = set(end)
        for i, o, l in zip(start, end, length):
            dst = self.get_node(o)
            dst.add_edge(i, l)
            src = self.get_node(i)
            src.add_edge(o, l)
            self.leaves.discard(i)

    def get_node(self, id):
        node = self.get(id)
        if node is None:
            node = Node(id)
            self[id] = node
        return node

    def dijkstra(self, source, dest):
        key = tuple(sorted([source, dest]))
        ret = self._cache.get(key)
        if ret is None:
            visited = set()
            qset = set([source])
            source = self.get_node(source)
            source.score = 0
            queue = [source]
            while queue:
                node = heappop(queue)
                visited.add(node.id)
                qset.discard(node.id)
                for id, l in node.edges.items():
                    if id in visited:
                        continue
                    if id in qset:
                        queue.remove(self[id])
                    qset.add(id)
                    self[id].update_score(node.score + l)
                    heappush(queue, self[id])

            ret = self[dest].score
            for n in self.values():
                n.score = INF

            self._cache[key] = ret

        return ret


class PowerOutage:

    def estimateTimeOut(self, fromJunction, toJunction, ductLength):
        tree = Tree(fromJunction, toJunction, ductLength)
        ret = INF
        for order in permutations(tree.leaves):
            cur = 0
            dist = 0
            for leaf in order:
                diff = tree.dijkstra(cur, leaf)
                dist += diff
                cur = leaf
            ret = min(ret, dist)
        return ret

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

def do_test(fromJunction, toJunction, ductLength, __expected):
    startTime = time.time()
    instance = PowerOutage()
    exception = None
    try:
        __result = instance.estimateTimeOut(fromJunction, toJunction, ductLength);
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
    sys.stdout.write("PowerOutage (1100 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("PowerOutage.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            fromJunction = []
            for i in range(0, int(f.readline())):
                fromJunction.append(int(f.readline().rstrip()))
            fromJunction = tuple(fromJunction)
            toJunction = []
            for i in range(0, int(f.readline())):
                toJunction.append(int(f.readline().rstrip()))
            toJunction = tuple(toJunction)
            ductLength = []
            for i in range(0, int(f.readline())):
                ductLength.append(int(f.readline().rstrip()))
            ductLength = tuple(ductLength)
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(fromJunction, toJunction, ductLength, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1412281609
    PT, TT = (T / 60.0, 75.0)
    points = 1100 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
