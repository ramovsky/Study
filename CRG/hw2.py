import string
import binascii

def strxor(a, b):     # xor two bytes of different lengths
    if len(a) > len(b):
        return bytes([x ^ y for (x, y) in zip(a[:len(b)], b)])
    else:
        return bytes([x ^ y for (x, y) in zip(a, b[:len(a)])])


def random(size=16):
    with open("/dev/urandom") as f:
        return f.buffer.read(size)


def encrypt(key, msg):
    c = strxor(key, msg)
    return c


def create(msgs):
    key = random(256)
    return [encrypt(key, m) for m in msgs]

a = [
["5f67abaf5210722b","bbe033c00bc9330e"],
["2d1cfa42c0b1d266","eea6e3ddb2146dd0"],
["e86d2de2e1387ae9","1792d21db645c008"],
["9d1a4f78cb28d863","75e5e3ea773ec3e6"],
]

for p in a:
    l = list(map(bytes.fromhex, p))
    print(binascii.hexlify(strxor(*l)))
