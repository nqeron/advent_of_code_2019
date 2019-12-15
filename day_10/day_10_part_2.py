import math
from collections import defaultdict


def distance(x_1, y_1, x, y):
    return math.sqrt((y - y_1) ** 2 + (x - x_1) ** 2)


def analyze(file):
    stars = []
    with open(file) as f:
        for line in f:
            stars.append([i for i in line.strip()])

    height = len(stars)
    width = len(stars[0])
    asteroids = [(x, y) for x in range(width) for y in range(height) if stars[y][x] == "#"]

    slopes = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    seen = {}
    for x_1, y_1 in asteroids:
        for x, y in asteroids:
            if not (x_1 == x and y_1 == y):
                if y_1 > y:
                    positive = 1
                elif y_1 < y:
                    positive = -1
                elif x_1 > x:
                    positive = 2
                elif x_1 < x:
                    positive = -2
                if x_1 == x:
                    slope = -math.inf
                else:
                    slope = (y_1 - y) / (x_1 - x)
                slopes[(x_1, y_1)][positive][slope].append((x, y))
        seen[(x_1, y_1)] = len(slopes[(x_1, y_1)][-1]) + len(slopes[(x_1, y_1)][1]) \
                            + len(slopes[(x_1, y_1)][2]) + len(slopes[(x_1, y_1)][-2])

    laser_x, laser_y = max([(x, y) for x, y in asteroids], key=lambda ast: seen[(ast[0], ast[1])])
    to_destroy = slopes[(laser_x, laser_y)]
    # num_asteroids_to_destroy = seen[(laser_x, laser_y)]
    slopes_iter = [(1, s) for s in sorted(to_destroy[1].keys()) if s <= 0]
    slopes_iter.extend([(-2, s) for s in sorted(to_destroy[-2].keys())])
    slopes_iter.extend([(-1, s) for s in sorted(to_destroy[-1].keys()) if s >= 0])
    slopes_iter.extend([(-1, s) for s in sorted(to_destroy[-1].keys(), key=lambda x: -x) if s <= 0])
    slopes_iter.extend([(2, s) for s in sorted(to_destroy[2].keys(), key=lambda x: -x)])
    slopes_iter.extend([(1, s) for s in sorted(to_destroy[1].keys()) if s >= 0])
    slopes_iter = slopes_iter * 10000

    count = 0
    # destroyed_x, destroyed_y = 0, 0
    for s in slopes_iter:
        positive = s[0]
        slope = s[1]
        if len(to_destroy[positive][slope]) <= 0:
            continue
        destroyed_x, destroyed_y = min(to_destroy[positive][slope],
                                       key=lambda ast: distance(laser_x, laser_y, ast[0], ast[1]))
        to_destroy[positive][slope].remove((destroyed_x, destroyed_y))
        print(count + 1, destroyed_x, destroyed_y, "slope="+str(slope), "positive="+str(positive))
        if count == 199:
            break
        count += 1
    print(destroyed_x, destroyed_y)


if __name__ == '__main__':
    analyze("../inputs/day_10.txt")
