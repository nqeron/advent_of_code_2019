
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
    fft_input *= 10000
    offset = int("".join([str(k) for k in fft_input[:7]]))
    # print(offset)
    # print(offset > total_len // 2)
    fft_input = fft_input[offset:]
    total_len = len(fft_input)

    for _ in range(100):
        total = 0
        next_input = []
        fft_input.reverse()
        for elem in fft_input:
            total += elem
            next_input.append(abs(total)%10)
        next_input.reverse()
        fft_input = next_input
    print("".join([str(k) for k in fft_input[:8]]))
    # first_digit = int(str(sum(fft_input[100:]))[-1])


if __name__ == '__main__':
    analyze("inputs/day_16.txt")
