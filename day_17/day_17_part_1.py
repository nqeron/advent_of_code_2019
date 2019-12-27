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
    comp = run_int_comp(opcodes)

    line = ""
    x, y = 0, 0
    camera = defaultdict(lambda: '.')
    while True:
        try:
            tile = next(comp)
        except StopIteration:
            break
        else:
            if tile == 10:
                # print(line)
                line = ""
                y += 1
                x = 0
            else:
                camera[(x, y)] = chr(tile)
                line += chr(tile)
                x += 1
                width = x
    height = y
    print_camera(camera, height, width)

    intersections = 0
    for pos in camera:
        if camera[pos] != "#":
            continue
        x, y = pos
        if x - 1 < 0 or x + 1 > width or y - 1 < 0 or y + 1 > height:
            continue
        left = (x - 1, y)
        right = (x + 1, y)
        up = (x, y - 1)
        down = (x, y + 1)
        if camera[up] == "#" and camera[down] == "#" and camera[left] == "#" and camera[right] == "#":
            intersections += x * y
    print(intersections)


def print_camera(camera, height, width):
    for y in range(height):
        print("".join([camera[(x, y)] for x in range(width)]))


if __name__ == '__main__':
    analyze("inputs/day_17.txt")
