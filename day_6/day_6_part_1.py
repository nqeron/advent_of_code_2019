def analyze(file):
    orbits = {}
    with open(file) as f:
        for line in f:
            planet, orbiter = line.strip().split(")")
            orbits[orbiter] = planet

    total_branches = 0
    for planet in orbits:
        total_branches += 1
        start = orbits[planet]
        while start != "COM":
            start = orbits[start]
            total_branches += 1
    print(total_branches)


if __name__ == '__main__':
    analyze("../inputs/day_6.txt")