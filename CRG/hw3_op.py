from binascii import hexlify
from Crypto.Hash import SHA256


def main():
    test = b''
    with open('prd.mp4', 'rb') as f:
        chunk = f.read(102400)
        while chunk:
            test += chunk
            chunk = f.read(102400)

    coursor = len(test)
    pad = 1024 - (coursor % 1024)
    coursor += pad
    step = 1024
    crc = b''
    while coursor >= step:
        last = test[coursor-step:coursor] + crc
        h = SHA256.new()
        h.update(last)
        crc = h.digest()
        coursor -= step

    print(coursor, hexlify(crc))


if __name__ == '__main__':
    main()
