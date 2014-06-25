def to_morze(digit, base=4):
    pat = ':0{}b'.format(base)
    bin = '{' + pat + '}'
    return bin.format(digit).replace('0', '.').replace('1', '-')


def checkio(data):
    hh, mm, ss = map(int, data.split(':'))
    ret = [to_morze(*a) for a in ((hh//10, 2), (hh%10,),
                                (mm//10, 3), (mm%10,),
                                (ss//10, 3), (ss%10,))]
    return '{} {} : {} {} : {} {}'.format(*ret)


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio("10:37:49") == ".- .... : .-- .--- : -.. -..-", "First Test"
    assert checkio("21:34:56") == "-. ...- : .-- .-.. : -.- .--.", "Second Test"
    assert checkio("00:1:02") == ".. .... : ... ...- : ... ..-.", "Third Test"
    assert checkio("23:59:59") == "-. ..-- : -.- -..- : -.- -..-", "Fourth Test"
