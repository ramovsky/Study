from datetime import date, timedelta


def checkio(from_date, to_date):
    diff = (to_date - from_date).days
    start = from_date.isoweekday()
    next_monday = from_date + timedelta(days=8-start)
    if next_monday > to_date:
        one_week = start + diff - 5
        return one_week if one_week > 0 else 0

    weekends = 2 if start < 7 else 1
    left = (to_date - next_monday).days
    print(next_monday, left, left // 7, left % 7 )
    weekends += (left // 7) * 2
    tail = left % 7 - 4
    if tail > 0:
        weekends += tail

    return weekends


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(date(2013, 9, 18), date(2013, 9, 23)) == 2, "1st example"
    assert checkio(date(2013, 1, 1), date(2013, 2, 1)) == 8, "2nd example"
    assert checkio(date(2013, 2, 2), date(2013, 2, 3)) == 2, "3rd example"
    assert checkio(date(2013, 11, 9), date(2013, 11, 23)) == 5, "4rd example"
    assert checkio(date(2002, 9, 9), date(2002, 9, 10)) == 0, "5rd example"
