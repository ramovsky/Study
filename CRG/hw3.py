import binascii
from Crypto.Cipher import AES


def strxor(a, b):     # xor two bytes of different lengths
    return bytes([x ^ y for (x, y) in zip(a, b)])


def test():
    x1 = b'\x00'*16
    y1 = b'\xff'*16
    y2 = b'\x00'*16

    # x2 = D(y2, E(y1, x1)+y1)
    ecb = AES.new(y1, AES.MODE_ECB)
    ex1 = ecb.encrypt(x1)
    Ey = strxor(ex1, y1)
    ecb = AES.new(y2, AES.MODE_ECB)
    x2 = ecb.decrypt(Ey)

    print()
    print('x1', binascii.hexlify(x1))
    print('y1', binascii.hexlify(y1))
    print('x2', binascii.hexlify(x2))
    print('y2', binascii.hexlify(y2))

    x1 = b'\xff'*16
    x2 = b'\xfa'*16
    y1 = b'\x00'*16

    # y2 = E(x1, x1)+y1+E(x2,x2)
    ecb = AES.new(x1, AES.MODE_ECB)
    ex1 = ecb.encrypt(x1)
    Ex1 = strxor(ex1, y1)
    ecb = AES.new(x2, AES.MODE_ECB)
    Ex2 = ecb.encrypt(x2)
    y2 = strxor(Ex1, Ex2)

    print()
    print('x1', binascii.hexlify(x1))
    print('y1', binascii.hexlify(y1))
    print('x2', binascii.hexlify(x2))
    print('y2', binascii.hexlify(y2))


if __name__ == '__main__':
    test()
