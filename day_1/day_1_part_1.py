
def analyze(file):
    with open(file) as f:
        print(sum([int(int(line)/3) - 2 for line in f]))


if __name__ == '__main__':
    analyze("../inputs/day_1.txt");