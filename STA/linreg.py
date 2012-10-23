def avg(lst):
    return float(sum(lst))/len(lst)

def lin_reg(xs, ys, x):
    assert len(xs) == len(ys), 'unsimilar length'
    axs = [avg(xs)] * len(xs)
    ays = [avg(ys)] * len(ys)
    dxs = [xi - ax for xi, ax in zip(xs, axs)]
    dys = [yi - ay for yi, ay in zip(ys, ays)]
    b1 = sum([dx*dy for dx, dy in zip(dxs, dys)])/sum([dx*dx for dx in dxs])
    b0 = avg(ys) - b1*avg(xs)
    print(axs)
    print(ays)
    print(dxs)
    print(dys)
    print(b0, b1)
    return b0 + b1*x
