from Crypto.Cipher import AES


def strxor(a, b):     # xor two bytes of different lengths
    if len(a) > len(b):
        return bytes([x ^ y for (x, y) in zip(a[:len(b)], b)])
    else:
        return bytes([x ^ y for (x, y) in zip(a, b[:len(a)])])


def test():
    key1 = bytes.fromhex('140b41b22a29beb4061bda66b6747e14')
    text1 = bytes.fromhex('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81')
    key3 = bytes.fromhex('36f18357be4dbd77f050515c73fcf9f2')
    text3 = bytes.fromhex('69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329')

    key4 = bytes.fromhex('36f18357be4dbd77f050515c73fcf9f2')
    text4 = bytes.fromhex('770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451')


    text = text1[16:]

    ecb = AES.new(key1, AES.MODE_ECB)
    out = b''
    for i in range(4):
        f = ecb.decrypt(text[i*16:(i+1)*16])
        a = text1[i*16:(i+1)*16]
        out += strxor(a, f)
    print(out)

    iv = bytearray(text4[:16])
    text = text4[16:]

    ecb = AES.new(key4, AES.MODE_ECB)
    fkiv = b''
    for i in range(10):
        fkiv += ecb.encrypt(bytes(iv))
        iv[-1] += 1
    print(strxor(fkiv, text))


if __name__ == '__main__':
    test()
