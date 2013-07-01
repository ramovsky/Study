def main():
    with open('IntegerArray.txt', 'rt') as f:
        data = [int(r) for r in f.read().split('\r\n') if r]

    print(data[:10], data[-2:], sum(data))


if __name__ == '__main__':
    main()
