

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


def analyze(file):
    stars = []
    with open(file) as f:
        for line in f:
            stars.append([i for i in line.strip()])

    maximum = 0
    for y, row in enumerate(stars):
        for x, elem in enumerate(row):
            if is_asteroid(x, y, stars):
                seen = calculate_seen(x, y, stars.copy())
                if seen >= maximum:
                    maximum = seen
    print(maximum)


if __name__ == '__main__':
    analyze("../inputs/day_10_t.txt")