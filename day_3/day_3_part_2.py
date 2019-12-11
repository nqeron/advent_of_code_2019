def gen_points(directions):
    pos = (0, 0)
    for d in directions:
        bearing = d[0]
        dist = int(d[1:])
        x_bear = ()
        y_bear = ()
        if bearing == "L":
            x_bear = range(pos[0], pos[0] - dist - 1, -1)
            y_bear = (pos[1] for _ in range(dist))
            pos = (pos[0] - dist, pos[1])
        elif bearing == "R":
            x_bear = range(pos[0], pos[0] + dist + 1)
            y_bear = (pos[1] for _ in range(dist))
            pos = (pos[0] + dist, pos[1])
        elif bearing == "U":
            y_bear = range(pos[1], pos[1] + dist + 1)
            x_bear = (pos[0] for _ in range(dist))
            pos = (pos[0], pos[1] + dist)
        elif bearing == "D":
            y_bear = range( pos[1], pos[1] - dist - 1, -1)
            x_bear = (pos[0] for _ in range(dist))
            pos = (pos[0], pos[1] - dist)
        for x, y in zip(x_bear, y_bear):
            yield (x, y)
    yield pos


def m_dist(point_1: tuple, point_2: tuple) -> int:
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


def analyze(file):
    with open(file) as f:
        directions_1 = f.readline().split(",")
        directions_2 = f.readline().split(",")

    points_1 = gen_points(directions_1)
    points_2 = gen_points(directions_2)
    final_1 = list(gen_points(directions_1))
    final_2 = list(gen_points(directions_2))
    next(points_1)
    next(points_2)

    print(min((final_1.index(i) + final_2.index(i) for i in set(points_1).intersection(set(points_2)))))


if __name__ == '__main__':
    analyze("../inputs/day_3.txt")