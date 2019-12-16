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


def get_input_from_joy() -> int:
    move = input().lower()
    if move == "w" or move == "i":
        return 0
    elif move == "a" or move == "j":
        return -1
    elif move == "d" or move == "l":
        return 1
    else:
        raise Exception("Unknown Command")


def get_char(col):
    if col == 0:
        return ' '
    elif col == 1:
        return '|'
    elif col == 2:
        return '#'
    elif col == 3:
        return '-'
    elif col == 4:
        return '0'


def print_screen(screen):
    for row in screen:
        print([get_char(col) for col in screen])


def analyze(file):
    with open(file) as f:
        opcodes = [int(i) for i in f.readline().strip().split(",")]
    opcodes[0] = 2
    comp = run_int_comp(opcodes)
    screen = defaultdict(lambda: defaultdict(lambda: 0))
    new_screen = False
    while True:
        while True:
            try:
                if not new_screen:
                    x = next(comp)
                    if x is None:
                        break
                else:
                    new_screen = False
                y = next(comp)
                if new_screen and y is None:
                    break
                tile = next(comp)
            except StopIteration:
                break
            else:
                screen[x][y] = tile
        if sum([1 for k in screen for j in screen[k] if screen[k][j] == 2]) <= 0:
            break
        print_screen(screen)
        try:
            x = comp.send(get_input_from_joy())
        except StopIteration:
            break
        else:
            new_screen = True


if __name__ == '__main__':
    # print(get_input_from_joy())
    analyze("inputs/day_13.txt")
