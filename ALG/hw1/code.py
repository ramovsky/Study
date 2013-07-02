def inv_count(arr, count=0):
    if len(arr) < 2:
        return arr, 0

    m = len(arr) // 2
    left, c = inv_count(arr[:m])
    count += c
    right, c = inv_count(arr[m:])
    count += c

    i = j = 0
    sarr = []
    c = len(arr)
    while c > 0:
        c -= 1
        if left[i] <= right[j]:
            sarr.append(left[i])
            i += 1
        else:
            sarr.append(right[j])
            count += len(left) - i
            j += 1
        if i == len(left):
            sarr += right[j:]
            break
        if j == len(right):
            sarr += left[i:]
#            count += len(left) - 1 - i
            break

    return sarr, count


def main():
    with open('IntegerArray.txt', 'rt') as f:
        data = [int(r) for r in f.read().split('\n') if r]

    print(inv_count([8,1,2,3,4,5,6,7]))
    print(inv_count(data)[1])


if __name__ == '__main__':
    main()
