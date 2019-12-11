def produce_points(directions) -> set:
    points = set()
    pos = (0, 0)
    for d in directions:
        bearing = d[0]
        dist = int(d[1:])
        x_bear = ()
        y_bear = ()
        if bearing == "L":
            x_bear = range(pos[0]-dist, pos[0]+1)
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
            y_bear = range(pos[1] - dist, pos[1] + 1)
            x_bear = (pos[0] for _ in range(dist))
            pos = (pos[0], pos[1] - dist)
        for x, y in zip(x_bear, y_bear):
            points.add((x, y))

    return points


def m_dist(point_1: tuple, point_2: tuple) -> int:
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


def analyze(file):
    with open(file) as f:
        directions_1 = f.readline().split(",")
        directions_2 = f.readline().split(",")
    points_1 = produce_points(directions_1)
    points_2 = produce_points(directions_2)

    intersections = points_1.intersection(points_2)

    print(min( (m_dist(intersection, (0, 0)) for intersection in intersections)))


if __name__ == '__main__':
    analyze("../inputs/day_3.txt")