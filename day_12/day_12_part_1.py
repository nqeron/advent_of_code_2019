import re


def new_vel(coord_cur, coord_target):
    if coord_cur < coord_target:
        return 1
    elif coord_cur > coord_target:
        return -1
    else:
        return 0


def simulate(moons, velocities):
    num_moons = len(moons)
    num_coords = len(moons[0])
    while True:
        velocities = [[sum([new_vel(moons[m][coord], moons[i][coord]) for i in range(num_moons) if i != m],
                           velocities[m][coord]) for coord in range(num_coords)] for m in range(num_moons)]
        moons = [[moons[m][coord] + velocities[m][coord] for coord in range(num_coords)] for m in range(num_moons)]
        kinetic = sum([sum([abs(moons[m][coord]) for coord in range(num_coords)]) *
                       sum([abs(velocities[m][coord]) for coord in range(num_coords)]) for m in range(num_moons)])
        yield moons, velocities, kinetic


def analyze(file):
    point_matcher = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    moons = []
    with open(file) as f:
        for line in f:
            moons.append([int(i) for i in point_matcher.match(line).groups()])
    velocities = [[0] * len(moons[i]) for i in range(len(moons))]

    simulator = simulate(moons, velocities)
    for i in range(1000):
        print("After ", i, "steps")
        for m, v in zip(moons, velocities):
            print("pos=<x={},y={},z={}>".format(*m), "vel=<x={},y={},z={}>".format(*v))
        moons, velocities, kinetic = next(simulator)
        print("Kinetic={}".format(kinetic))


if __name__ == '__main__':
    analyze("inputs/day_12.txt")
