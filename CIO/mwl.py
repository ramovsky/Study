import string
from collections import Counter


def checkio(text):
    c = Counter()
    ret = 0, 'a'
    for l in text:
        if l in string.whitespace:
            continue
        l = l.lower()
        c += Counter(l)
        if c[l] >= ret[0]:
            ret = c[l], l
    return ret[1]


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio("Hello World!") == "l", "Hello test"
    assert checkio("How do you do?") == "o", "O is most wanted"
    assert checkio("One") == "e", "All letter only once."
