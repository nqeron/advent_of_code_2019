import math
from collections import defaultdict


def is_asteroid(x, y, stars):
    if y > len(stars) or x > len(stars[0]):
        return False
    else:
        return stars[y][x] == "#"


def calculate_seen(x, y, star_map: list) -> int:
    height = len(star_map)
    width = len(star_map[0])
    out = sum(1 for i in range(len(star_map)) for x_delta in range(-width, width)
              for y_delta in range(-height, height) if is_asteroid(x, y, star_map))
    return out


def distance(x_1, y_1, x, y):
    return math.sqrt((y-y_1)**2 + (x-x_1)**2)


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
                    positive = 0
                if x_1 == x:
                    slope = math.inf
                else:
                    slope = (y_1 - y) / (x_1 - x)
                slopes[(x_1, y_1)][positive][slope].append((x, y))
        seen[(x_1, y_1)] = len(slopes[(x_1, y_1)][-1]) + len(slopes[(x_1, y_1)][1]) + len(slopes[(x_1, y_1)][0])

    print(max([seen[(x, y)] for x, y in asteroids]))


if __name__ == '__main__':
    analyze("../inputs/day_10.txt")