from decimal import Decimal


def checkio(data):
    balance, withdrawal = data
    for w in withdrawal:
        sub = w * Decimal('1.01') + Decimal('0.5')
        if w % Decimal(5) != 0 or sub > balance:
            continue
        balance -= sub
    return balance


if __name__ == '__main__':
    assert Decimal(checkio([
        Decimal('120'),
        [Decimal('10') , Decimal('20'), Decimal('30')]
        ])) ==  Decimal('57.9') ,'First'

    # With one Insufficient Funds, and then withdraw 10 $
    assert Decimal(checkio([
        Decimal('120'),
        [Decimal('200') , Decimal('10')] ])) == Decimal('109.4'), 'Second'


    #with one incorrect amount
    assert Decimal(checkio([
        Decimal('120'),
        [Decimal('3'), Decimal('10')]
        ])) == Decimal('109.4'), 'Third'

    #with one incorrect amount
    assert Decimal(checkio([
        Decimal('120'),
        [Decimal('3'), Decimal('10'), Decimal('100'), Decimal('10')]
        ])) == Decimal('7.9'), 'Fourth'

    print('All Ok')
