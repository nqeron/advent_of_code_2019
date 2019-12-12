def analyze(file, width, height):
    with open(file) as f:
        inputs = [int(i) for i in f.readline().strip()]
    sep = width * height
    layers = [inputs[i:i+sep] for i in range(0, len(inputs), sep)]

    pixels = [[layer[i:i+width] for i in range(0, len(layer), width)] for layer in layers]

    final_pixel = [[2] * width for _ in range(height)]

    for x in range(width):
        for y in range(height):
            for layer in pixels:
                if layer[y][x] != 2:
                    final_pixel[y][x] = layer[y][x]
                    break
    for line in final_pixel:
        print(line)


if __name__ == '__main__':
    analyze("../inputs/day_8.txt", 25, 6)
