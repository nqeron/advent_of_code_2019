from collections import defaultdict


def get_val_from_opcodes(opcodes, pos, mode, rel_base) -> int:
    val = opcodes[pos]
    if mode == "0":
        if val >= len(opcodes):
            return -1
        return opcodes[val]
    elif mode == "1":
        return val
    elif mode == "2":
        new_pos = rel_base + val
        if new_pos < 0 or new_pos >= len(opcodes):
            return -1
        return opcodes[new_pos]
    raise Exception("Mode not recognized")


def get_dest_from_opcodes(opcodes, pos, mode, rel_base) -> int:
    val = opcodes[pos]
    if mode == "0":
        return  val
    elif mode == "1":
        raise Exception("Cannot save in immediate mode")
    elif mode == "2":
        return rel_base + val


def run_int_comp(opcodes):
    opcodes += [0] * 10000
    pos = 0
    rel_base = 0
    while opcodes[pos] != 99:
        op = str(opcodes[pos])

        if len(op) < 5:
            op = "0" * (5-len(op)) + op

        mode_1 = op[2]
        mode_2 = op[1]
        mode_3 = op[0]

        code = op[3:]

        left = get_val_from_opcodes(opcodes, pos + 1, mode_1, rel_base)
        right = get_val_from_opcodes(opcodes, pos + 2, mode_2, rel_base)
        if len(opcodes) > pos+3:
            dest = get_dest_from_opcodes(opcodes, pos+3, mode_3, rel_base)

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
            if mode_1 == "2":
                left = rel_base + opcodes[pos+1]
            opcodes[left] = yield
            pos += 2
        elif code == "04":
            pos += 2
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
        elif code == "09": # update relative base
            rel_base += left
            pos += 2
            continue
        elif op == "99":
            break
        else:
            raise Exception("Unrecognized opcode")


def analyze(file):
    with open(file) as f:
        opcodes = [int(i) for i in f.readline().strip().split(",")]
    opcodes[0] = 2
    comp = run_int_comp(opcodes)
    next(comp)

    main_movement = "A,B,A,C,B,A,C,A,C,B"
    routine_a = "L,12,L,8,L,8"
    routine_b = "L,12,R,4,L,12,R,6"
    routine_c = "R,4,L,12,L,12,R,6"
    continuous_feed = "n"

    line = ""
    while True:
        try:
            # latest = result
            result = next(comp)
            if result is None:
                break
            if result == 10:
                print(line)
                line = ""
            else:
                line += chr(result)
        except StopIteration:
            break

    for elem in [ord(c) for c in main_movement] + [10]:
        x = comp.send(elem)
        # print(x)
    print_input(comp, x)
    for elem in [ord(c) for c in routine_a] + [10]:
        x = comp.send(elem)
    print_input(comp, x)
    for elem in [ord(c) for c in routine_b] + [10]:
        x = comp.send(elem)
    print_input(comp, x)
    for elem in [ord(c) for c in routine_c] + [10]:
        x = comp.send(elem)
    print_input(comp, x)
    for elem in [ord(c) for c in continuous_feed] + [10]:
        latest = comp.send(elem)
    print_input(comp, latest)
    # latest, result = None, None
    print(latest)


def print_input(comp, x):
    line = chr(x)
    while True:
        try:
            out = next(comp)
        except StopIteration:
            break
        else:
            if out is None:
                break
            if out == 10:
                print(line)
                line = ""
            else:
                try:
                    line += chr(out)
                except ValueError:
                    print(out)


def print_camera(camera, height, width):
    for y in range(height):
        print("".join([camera[(x, y)] for x in range(width)]))


if __name__ == '__main__':
    analyze("inputs/day_17.txt")
