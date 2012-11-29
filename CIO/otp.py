import string
import binascii
from random import choice
from collections import defaultdict


MSGS1 = (
b'Lorem ipsum dolor sit amet, consectetur adipiscing',
b' elit. Nulla purus est, pellentesque sit amet suscipi',
b't eget, placerat et lorem Morbi augue magna, bibendum po',
b'rta commodo interdum pellentesque nec nulla Nulla ',
b'eu dapibus leo. Quisque consequat commodo velit id ultrices. Maecenas ',
b'enim maurise, vestibulum eu  volutpat non, porta eu metus. ',
b'Cras eget orci arcu, a volutpat  enim. Praesent mauris est,',
b' tincidunt et i nterdum ut semper vitae dolor. Nullam ultrices, ',
b'purus et ullamcorper bibendum, risus diam volutpat augue, eu ',
b'lobortis augue nisl quis dolor. Cum sociis natoque penatibus et ',
b'magnis dis parturient montes, nascetur ridiculus mus. ',
b'Vestibulum cursus dapibus erat'
)

MSGS2 = (
b'In cryptography the one-time pad (OTP) is ',
b'a type of encryption which has been proven to be',
b' impossible to crack if used correctly. Each ',
b'bit or  character from the plaintext is encrypted ',
b'by a modular addition with a bit or character',
b' from a  secret random  key (or pad) ',
b'of the same length as the plaintext,  ',
b'resulting  in a ciphertext. If the key is ',
b' truly random, as large  as or greater than the',
b'plaintext, never reused in whole o part, and kept secret',
b'with quantum key distribution'
)


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


def test():
    hexmsgs = [binascii.hexlify(m).decode('ascii') for m in create(MSGS1)]
    print('\nInput1:', hexmsgs)
    rep = checkio(hexmsgs)
    print('\nOutput1:\n' + repr(rep))
    assert rep == 'Vestibulum cursus dapibus erat'
    hexmsgs = [binascii.hexlify(m).decode('ascii') for m in create(MSGS2)]
    print('\nInput2:', hexmsgs)
    rep = checkio(hexmsgs)
    print('\nOutput2:\n' + repr(rep))
    assert rep == 'with quantum key distribution'


def checkio(data):
    bytemsgs = list(map(bytes.fromhex, data))

    all_letters = (string.ascii_letters + string.digits + ' ').encode('ascii')
    xored_space = strxor(b' '*len(all_letters), all_letters)

    spaces = [[0]*100 for i in range(len(bytemsgs))]
    for i, m in enumerate(bytemsgs):
        for n, t in enumerate(bytemsgs):
            if i == n:
                continue
            for j, char in enumerate(strxor(t, m)):
                spaces[i][j] += 1 if char in xored_space else 0

    key = bytearray(b' '*100)
    weights = defaultdict(int)
    for i, m in enumerate(spaces):
        for j, w in enumerate(m):
            if w > weights[j]:
                key[j] = 32 ^ bytemsgs[i][j]
                weights[j] = w

    ret = strxor(key, bytemsgs[-1]).decode('ascii')
    return ret


test()

assert checkio(['49009e15436343564303d0d33311b207c02d79c95b2d2289765535aa29a570270b4cb2fdc8701952afa0d9e95fe49292919a', '250a80195a6d0a68451ad192770eab1ac77e2ac55c796fc4634475e62fa46a311d5eb3fd9c760206eea5ddfc42b7828e8c9e7c5ce3', '714f89174b370606401adc90320cbf1c92687e80436231817e0154e538a877740f5aa1edd9250613a9aad1b516f598999a937159e79a4281', '771b8d504d2c474b5f12d2d33e10aa0dc0697fcd0f7d26887f4477fe2fb96f210b0fa8fddf250507a2a8d1b978e29d979edd', '601acc144f33434445059d9f3211f048e37863d35e7826c4704e77f92fbb6b351a0fa5f7d1680416a1e4c6fc5afe85db96993559e6ce4087c594635101d41bc2183db5a9b688', '6001851d0e2e4b53421fce967b5ea80dc17963c25a61368933446caa6abc71381b5bb6f9c825051da0e890e959e5859adf98600ce7df469bd5df30', '461d8d030e264d434456d2813417fe09c06e7f8c0f6c63927c4d6cfe3aab6a744e4aa8f1d12b4b22bca5d5ea53f985db929c605ee3c9128bd5853c', '251b851e4d2a4e535e029d96235eb748dc796fd24b782ec4665539f92fa76e311c0fb0f1c8640e52aaabdcf644b9d1b58a91794de79a4782d283791c44ea5687', '751a9e055d634f521003d19f3613bd07c07d6fd20f6f2a86764f7dff27e63e26075cb3eb9c610213a3e4c6f65ae2858b9e89354dffdd478b8ad1750a01', '69008e1f5c3743551017c894221bfe06db7e66805e782a97334576e625b830742d5aabb8cf6a081ba7b790f757e39e8a8a98355cefd4539acf93650c01fc0e87', '680e8b1e47300a4259059d83360caa1dc0646fce5b2d2e8b7d557cf966ea70351d4ca3ecc9774b00a7a0d9fa43fb8488df90605fa49a', '530a9f0447215f4a451b9d90220cad1dc12d6ec15f64219160017cf82bbe']) == 'Vestibulum cursus dapibus erat', 'First'

assert checkio(['97be8c7f30712f760109fea253d1e4fdb9c876538cb0e61c847d9fb8fb2f9886ccede8a6a5abe075d017', 'bff0d865326d7f6d084ee9ad40cbe4adb9c97c1dc3a9eb58937cd2b5ba2cd98089a0c9d285f0af6ac659d76ec63db42c', 'feb9c16c2d7b2c6b0c02e9e357d6bdbebfc17018c3b7e511856797b9fb3c96909ea0c48699fbee3ce656947289', 'bcb9d83c2d7a7f220d06edb142dae9b8bf8075018cb3a3459871d2adb73e908c98a0df86d5ebb33cc6599468d06da22c442c', 'bca98c7d626530661b02edb103d8f9b9a4d47a1c8dfef458847cd2bcfb3d9096ccaad5d296eaa16ec254837fdb', 'feb6de732f283e224e1de9a051dce9fdbfc17d178cb3a3119b718bfdf3308bc29ca4c3dbd5', 'b1b68c682a6d7f710f03e9e34fdcf3bab9c8331290fef759953482b1ba36979689bdd3ded5a2', 'acb5df692e7c366c094eacaa4d99fcfdaec9631b86acf7548860dcfd9239d99684a0879990fbe075d017', 'fea4de692e717f700f00e8ac4e95bdbcbe807f1291b9e611d07581fdb42dd9859ea0c68690f0e068cb56993add75b3', 'aebccd752c7c3a7a1a42acad46cff8afedd2760690bbe711997ad2aab3309587ccaa878294f0b4308356997e8976b339542cc6244f733a3d', 'a9b9d87462792a63001af9ae03d2f8a4edc47a0097acea5385609bb2b5']) == 'with quantum key distribution', 'Second'
