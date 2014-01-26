import sys
from collections import Counter, defaultdict


WEIGHTS = {l: 1 for l in 'eaionrtlsu'}
WEIGHTS.update({l: 2 for l in 'dg'})
WEIGHTS.update({l: 3 for l in 'bcmp'})
WEIGHTS.update({l: 4 for l in 'fhvwy'})
WEIGHTS.update({l: 5 for l in 'k'})
WEIGHTS.update({l: 8 for l in 'jx'})
WEIGHTS.update({l: 10 for l in 'qz'})


def extract_letters(word):
    c = Counter()
    for l in word:
        c += Counter(l)
    return c

def score(word):
    return sum(WEIGHTS[l] for l in word)


def process(dictionary, letters):
    mask = set()
    best = None, 0
    for l, c in extract_letters(letters).items():
        for i in range(c):
            mask.add(l*(i+1))

    for word in dictionary:
        need = set(letter*count for letter, count in extract_letters(word).items())
        if need <= mask:
            s = score(word)
            if s  > best[1]:
                best = word, s
    print(best[0])
    return best



def main():
    n = int(raw_input())
    dictionary = []
    for i in xrange(n):
        dictionary.append(raw_input())
    letters = raw_input()
    process(dictionary, letters)



if __name__ == '__main__':
    main()
