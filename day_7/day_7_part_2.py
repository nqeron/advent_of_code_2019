import itertools


def get_from_opcodes(opcodes, pos, mode) -> int:
    val = opcodes[pos]
    if mode == "0":
        if val >= len(opcodes):
            return -1
        return opcodes[val]
    elif mode == "1":
        return val
    raise Exception("Mode not recognized")


def run_int_comp(opcodes):
    pos = 0
    while opcodes[pos] != 99:
        op = str(opcodes[pos])

        if len(op) < 5:
            op = "0" * (5-len(op)) + op

        mode_1 = op[2]
        mode_2 = op[1]
        mode_3 = op[0]

        code = op[3:]

        left = get_from_opcodes(opcodes, pos+1, mode_1)
        right = get_from_opcodes(opcodes, pos+2, mode_2)
        dest = opcodes[pos+3]

        if code == "01":
            opcodes[dest] = left + right
            pos += 4
            continue
        elif code == "02":
            opcodes[dest] = left * right
            pos += 4
            continue
        elif code == "03":
            left = opcodes[pos+1]
            opcodes[left] = yield
            pos += 2
        elif code == "04":
            pos += 2
            # print(left)
            yield left
            continue
        elif code == "05":
            if left != 0:
                pos = right
            else:
                pos += 3
            continue
        elif code == "06":
            if left == 0:
                pos = right
            else:
                pos += 3
            continue
        elif code == "07":  # less than
            if left < right:
                opcodes[dest] = 1
            else:
                opcodes[dest] = 0
            pos += 4
            continue
        elif code == "08":  # equals
            if left == right:
                opcodes[dest] = 1
            else:
                opcodes[dest] = 0
            pos += 4
            continue
        elif op == "99":
            break
        else:
            raise Exception("Unrecognized opcode")


def analyze(file):
    with open(file) as f:
        opcodes = [int(i) for i in f.readline().split(",")]

    maximum = 0
    for perm in itertools.permutations(range(5, 10)):
        amp_a = run_int_comp(opcodes.copy())
        amp_b = run_int_comp(opcodes.copy())
        amp_c = run_int_comp(opcodes.copy())
        amp_d = run_int_comp(opcodes.copy())
        amp_e = run_int_comp(opcodes.copy())

        next(amp_a)
        next(amp_b)
        next(amp_c)
        next(amp_d)
        next(amp_e)
        r = amp_a.send(perm[0])
        amp_b.send(perm[1])
        amp_c.send(perm[2])
        amp_d.send(perm[3])
        amp_e.send(perm[4])

        next_a = amp_a.send(0)
        out = 0
        while True:
            next_b = amp_b.send(next_a)
            next_c = amp_c.send(next_b)
            next_d = amp_d.send(next_c)
            out = amp_e.send(next_d)

            if out >= maximum:
                maximum = out
            next_a = amp_a.send(out)
            if next_a is None:
                break

    print(maximum)


if __name__ == '__main__':
    analyze("../inputs/day_7_test.txt")