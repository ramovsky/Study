import string
from random import choice

MSGS = (
    b'I love lol troll face',
    b'insollo kwasollo pasollo'
    )


def strxor(a, b):     # xor two bytes of different lengths
    if len(a) > len(b):
        return bytearray([x ^ y for (x, y) in zip(a[:len(b)], b)])
    else:
        return bytearray([x ^ y for (x, y) in zip(a, b[:len(a)])])


def random(size=16):
    with open("/dev/urandom") as f:
        return f.buffer.read(size)


def encrypt(key, msg):
    c = strxor(key, msg)
    return c


def main():
    key = random(1024)
    ciphertexts = [encrypt(key, msg) for msg in MSGS]
    for c in ciphertexts:
        print(encrypt(key, c))

main()
