
def rotate(t, n):
    return t[n:] + t[:n]
def flip_all(t):
    return tuple(map(lambda ds: (0, ds[1]) if ds[0] == 1 else (1, ds[1]), t))

def get_canonical(t):
    if t[0][0] == 0:
        print "flip"
        t = flip_all(t)

    if (sum(map(lambda ds: ds[0], t)) == 2):
        print t[1]
        if t[1][0] == 0:
            print "yes"
            t = rotate(t, -1)
    return t

print get_canonical(((0, -1), (1, 1), (0, 1)))
