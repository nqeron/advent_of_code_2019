
def pattern_list(n, target_len):
    if n <= 0:
        return None
    # four = n * 4
    mult = target_len // (n * 4) + 1
    pattern = [elem for a in [[0] * n, [1] * n, [0] * n, [-1] *n] for elem in a] * mult
    pattern.pop(0)
    return pattern


def analyze(file):
    with open(file) as f:
        fft_input = [int(i) for i in f.readline().strip()]
    total_len = len(fft_input)

    for phase in range(1, 101):
        next_pattern = []
        for row in range(1, total_len+1):
            total_value = sum([i*j for i, j in zip(fft_input, pattern_list(row, total_len))])
            next_pattern.append(int(str(total_value)[-1]))
        print("After Phase {}:".format(phase), "".join([str(p) for p in next_pattern]))
        fft_input = next_pattern


if __name__ == '__main__':
    analyze("inputs/day_16.txt")
