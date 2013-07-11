from random import shuffle
PIVOT = -1
SWAPS = 0


def find_pivot(arr):
    l = (len(arr)-1)//2
    a = sorted([(arr[0], 0), (arr[l], l), (arr[-1], -1)])
#    print(a)
    return a[1][1]


def quick_sort(arr):
    global SWAPS
    l = len(arr)
    SWAPS += l - 1
    if l == 1:
        return arr

    PIVOT = find_pivot(arr)
    arr[PIVOT], arr[0] = arr[0], arr[PIVOT]
    pivot = arr[0]
    j = 0
    for i in range(1, l):
        if arr[i] < pivot:
            arr[j+1], arr[i] = arr[i], arr[j+1]
            j += 1

    arr[0], arr[j] = arr[j], arr[0]
    if j > 0:
        arr[:j] = quick_sort(arr[:j])
    if j < l-1:
        arr[j+1:] = quick_sort(arr[j+1:])
    return arr


def main():
    with open('QuickSort.txt', 'rt') as f:
        data = [int(r) for r in f.read().split('\n') if r]


    print(find_pivot([2,4,3]))

    quick_sort(data)
    print(SWAPS)


if __name__ == '__main__':
    main()
