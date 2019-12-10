
def fuel(mass: int) -> int:
    last = int(mass/3) - 2
    total = 0
    while last > 0:
        total += last
        last = int(last/3) - 2
    return total


def analyze(file):
    with open(file) as f:
        print(sum([fuel(int(line)) for line in f]))


if __name__ == '__main__':
    analyze("../inputs/day_1.txt");