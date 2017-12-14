

directions = [(-1,0), (0,1), (1,0), (0,-1), (0,0)]
dirs = ["North", "East", "South", "West", "Stay"]


def add(a, b):
    return tuple(map(lambda a, b: a + b, a, b))

def sub(a,b):
    return tuple(map(lambda a, b: a - b, a, b))


def manhattan_dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])



def direction_to_cmd(p):
    return dirs[directions.index((p[0],p[1]))]

def cmd_to_direction(c):
    return directions[dirs.index(c)]
