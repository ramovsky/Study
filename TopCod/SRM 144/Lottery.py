# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect


_factorial_cache = {}

def factorial(n):
    if n in _factorial_cache:
        return _factorial_cache[n]

    if n == 0:
        return 1

    else:
        res = n * factorial(n-1)
        _factorial_cache[n] = res
        return res

factorial = math.factorial


def combinations(p, r):
    assert p > r
    return factorial(p)/factorial(r)/factorial(p-r)


class Lottery:

    def sortByOdds(self, rules):
        lst = []
        for r in rules:
            name, rule = r.split(':')
            lst.append((self._get_rule_score(rule), name))
        return tuple(n for s, n in sorted(lst))

    def _get_rule_score(self, rule):
        choices, blanks, sorte, unique = rule.strip().split()
        choices, blanks = map(int, (choices, blanks))
        base = combinations(choices, blanks)
        p, r = choices, blanks

        if sorte == 'T' and unique == 'T':
            return base

        if sorte == 'T'and unique == 'F':
            return factorial(p+r-1)/factorial(p-1)/factorial(r)

        if sorte == 'F' and unique == 'T':
            return factorial(p)/factorial(p-r)

        if sorte == 'F'  and unique == 'F':
            return choices ** blanks

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

def do_test(rules, __expected):
    startTime = time.time()
    instance = Lottery()
    exception = None
    try:
        __result = instance.sortByOdds(rules);
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
    sys.stdout.write("Lottery (550 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("Lottery.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            rules = []
            for i in range(0, int(f.readline())):
                rules.append(f.readline().rstrip())
            rules = tuple(rules)
            f.readline()
            __answer = []
            for i in range(0, int(f.readline())):
                __answer.append(f.readline().rstrip())
            __answer = tuple(__answer)

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(rules, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1411590177
    PT, TT = (T / 60.0, 75.0)
    points = 550 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)


if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
