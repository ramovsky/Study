

def main():
    with open('kargerMinCut.txt', 'rt') as f:
        data = {}
        for r in f.read().split('\n'):
            if r:
                r = [int(i) for i in r.split('\t') if i]
                data[r[0]] = r[1:]
    print(data[1])
    print(data[2])



if __name__ == '__main__':
    main()
