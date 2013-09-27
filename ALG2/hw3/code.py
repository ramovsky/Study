import sys
from collections import defaultdict


from queue import Queue


class Node:
    def __init__(self, level, profit, weight):
        self.level = level # The level within the tree (depth)
        self.profit = profit # The total profit
        self.weight = weight # The total weight

def solveKnapsack(weights, profits, knapsackSize):
    numItems = len(weights)
    queue = Queue()
    root = Node(-1, 0, 0)
    queue.put(root)

    maxProfit = 0
    bound = 0
    while not queue.empty():
        v = queue.get() # Get the next item on the queue

        uLevel = v.level + 1
        u = Node(uLevel, v.profit + profits[uLevel], v.weight + weights[uLevel])

        bound = getBound(u, numItems, knapsackSize, weights, profits)

        if u.weight <= knapsackSize and u.profit > maxProfit:
            maxProfit = u.profit

        if bound > maxProfit:
            queue.put(u)

        u = Node(uLevel, v.profit, v.weight)
        bound = getBound(u, numItems, knapsackSize, weights, profits)

        if (bound > maxProfit):
            queue.put(u)
    return maxProfit


# This is essentially the brute force solution to the fractional knapsack
def getBound(u, numItems, knapsackSize, weights, profits):
    if u.weight >= knapsackSize: return 0
    else:
        upperBound = u.profit
        totalWeight = u.weight
        j = u.level + 1
        while j < numItems and totalWeight + weights[j] <= knapsackSize:
            upperBound += profits[j]
            totalWeight += weights[j]
            j += 1
        if j < numItems:
            upperBound += (knapsackSize - totalWeight) * profits[j]/weights[j]
        return upperBound


def main():

    if sys.argv[-1] == '2':
        with open('knapsack_big.txt', 'rt') as f:
            size = None
            values = []
            weights = []
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                v, w = map(int, r.split(' '))
                if size is None:
                    size = v+1
                    items = w
                else:
                    values.append(v)
                    weights.append(w)

        print(solveKnapsack(weights, values, size))

    else:
        with open('knapsack1.txt', 'rt') as f:
            size = None
            values = []
            weights = []
            for r in f.read().split('\n'):
                if not r:
                    continue
                elif r == 'stop':
                    break
                v, w = map(int, r.split(' '))
                if size is None:
                    size = v+1
                    items = w
                else:
                    values.append(v)
                    weights.append(w)

        cache = defaultdict(int)
        print(len(values), len(weights))
        for i in range(1, items):
            for j in range(size):
                if j >= weights[i]:
                    cache[(i, j)] = max(
                        cache[(i-1, j)],
                        cache[(i-1, j-weights[i])] + values[i])
                else:
                    cache[(i, j)] = cache[(i-1, j)]

        ks, m = 0, 0
        for k, v in cache.items():
            if v > m:
                m = v
                ks = k
        print(ks, cache[ks])


if __name__ == '__main__':
    main()
