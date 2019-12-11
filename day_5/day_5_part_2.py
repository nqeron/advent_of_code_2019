def get_from_opcodes(opcodes, pos, mode) -> int:
    val = opcodes[pos]
    if mode == "0":
        if val >= len(opcodes):
            return -1
        return opcodes[val]
    elif mode == "1":
        return val
    raise Exception("Mode not recognized")


def analyze(file):
    with open(file) as f:
        opcodes = [int(i) for i in f.readline().split(",")]
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
            opcodes[left] = int(input("Enter the next value"))
            pos += 2
        elif code == "04":
            pos += 2
            print(left)
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


if __name__ == '__main__':
    analyze("../inputs/day_5.txt")