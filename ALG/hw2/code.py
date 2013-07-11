PIVOT = 0
SWAPS = 0

def quick_sort(arr):
    print('inp', arr)
    l = len(arr)

    if l == 1:
        return arr

    arr[PIVOT], arr[0] = arr[0], arr[PIVOT]
    pivot = arr[0]
    j = 1
    for i in range(2, l):
        if arr[i] < pivot:
            arr[j], arr[i] = arr[i], arr[j]
            j += 1

    j -= 1
    arr[0], arr[j] = arr[j], arr[0]
    if j > 1:
        arr[:j] = quick_sort(arr[:j])
    if j < l-2:
        arr[j+1:] = quick_sort(arr[j+1:])
    print('out', arr)
    return arr


def main():
    with open('QuickSort.txt', 'rt') as f:
        data = [int(r) for r in f.read().split('\n') if r]

    arr = [5,2,3,2,6,7,8,32,32,3,2,1,3,4]
    arr = [5,4,3,2]
    print(arr)
    print(quick_sort(arr))


if __name__ == '__main__':
    main()
