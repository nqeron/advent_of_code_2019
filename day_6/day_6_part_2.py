from collections import defaultdict
import math


def analyze(file):
    orbits = defaultdict(list)
    with open(file) as f:
        for line in f:
            planet, orbiter = line.strip().split(")")
            orbits[orbiter].append(planet)
            orbits[planet].append(orbiter)

    distance = 0
    next_planets = [i for i in orbits["YOU"]]
    distances = {x: math.inf for x in orbits}
    distances["YOU"] = 0
    while len(next_planets) > 0:
        next_planet = next_planets.pop(0)
        if distances[next_planet] == math.inf:
            distances[next_planet] = 0
        distance = distances[next_planet] + 1
        if next_planet == "SAN":
            break
        else:
            for i in orbits[next_planet]:
                if distances[i] == math.inf:
                    next_planets.append(i)
                    distances[i] = distance

    print(distances["SAN"] - 1)


if __name__ == '__main__':
    analyze("../inputs/day_6.txt")