import re
import time
from functools import reduce


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def lcmm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)


def new_vel(coord_cur, coord_target):
    if coord_cur < coord_target:
        return 1
    elif coord_cur > coord_target:
        return -1
    else:
        return 0


def simulate(moons, velocities):
    num_moons = len(moons)
    # num_coords = len(moons[0])
    while True:
        velocities = [sum([new_vel(moons[m], moons[i]) for i in range(num_moons) if i != m],
                          velocities[m]) for m in range(num_moons)]
        moons = [moons[m] + velocities[m] for m in range(num_moons)]
        yield tuple([elem for x in zip(moons, velocities) for elem in x])


def analyze(file):
    point_matcher = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    moons = []
    with open(file) as f:
        for line in f:
            moons.append([int(i) for i in point_matcher.match(line).groups()])
    velocities = [[0] * len(moons[i]) for i in range(len(moons))]

    simulate_x = simulate([moons[i][0] for i in range(len(moons))], [velocities[i][0] for i in range(len(velocities))])
    simulate_y = simulate([moons[i][1] for i in range(len(moons))], [velocities[i][1] for i in range(len(velocities))])
    simulate_z = simulate([moons[i][2] for i in range(len(moons))], [velocities[i][2] for i in range(len(velocities))])
    x_ident, y_ident, z_ident = next(simulate_x), next(simulate_y), next(simulate_z)
    x_steps = 0
    y_steps = 0
    z_steps = 0
    now = time.time()
    seen = set()
    while x_ident not in seen:
        seen.add(x_ident)
        x_ident = next(simulate_x)
        x_steps += 1
    seen = set()
    while y_ident not in seen:
        seen.add(y_ident)
        y_ident = next(simulate_y)
        y_steps += 1
    seen = set()
    while z_ident not in seen:
        seen.add(z_ident)
        z_ident = next(simulate_z)
        z_steps += 1
    then = time.time()
    # print(then-now)
    print(lcmm(x_steps, y_steps, z_steps))


if __name__ == '__main__':
    analyze("inputs/day_12.txt")
