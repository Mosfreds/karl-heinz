

directions = [(1,0), (0,1), (-1,0), (0,-1)]

def add(a, b):
    return tuple(map(lambda a, b: a + b, a, b))


def manhattan_dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


