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
    points_1 = produce_points("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(","))
    points_temp = gen_points("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(","))
    #print(set(points_temp))
    #print(points_1)
    #print(set(points_temp) - points_1)
    points_temp = gen_points("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(","))
    #print([i for i in points_temp])
    points_2 = produce_points("U62,R66,U55,R34,D71,R55,D58,R83".split(","))
    points_2_temp = gen_points("U62,R66,U55,R34,D71,R55,D58,R83".split(","))
    #print(points_2 - set(points_2_temp))


    intersections = points_1.intersection(points_2)
    int_temp = set(points_temp).intersection(set(points_2_temp))

    print(intersections)
    print(int_temp)
    #print(min( (m_dist(intersection, (0, 0)) for intersection in intersections)))


if __name__ == '__main__':
    analyze("../inputs/day_3.txt")