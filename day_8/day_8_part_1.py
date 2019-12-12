def analyze(file, width, height):
    with open(file) as f:
        pixels = [int(i) for i in f.readline().strip()]
    sep = width * height
    layers = [pixels[i:i+sep] for i in range(0, len(pixels), sep)]
    min_layer = min(layers, key=lambda x: sum([1 for i in x if i == 0]))
    print(sum([1 for i in min_layer if i == 1]) * sum([1 for i in min_layer if i == 2]))


if __name__ == '__main__':
    analyze("../inputs/day_8.txt", 25, 6)