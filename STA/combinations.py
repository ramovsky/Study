from __future__ import division


def combinations(n, k):
    assert n >= k, 'Wrong parameters'
    ret = 1
    for i in range(n, n-k, -1):
        ret *= i
    for i in range(1, k+1):
        ret /= i
    return ret


def probabiliti(n, k, p):
    return combinations(n, k) * p**k * (1-p)**(n-k)


def mean(a):
    return sum(a)/len(a)


def variance(a):
    m = mean(a)
    return sum((m - x)**2 for x in a)/len(a)


def std(a):
    return variance(a)**0.5


def confidence(a, k=1.96):
    return k * (variance(a)/len(a))**0.5

