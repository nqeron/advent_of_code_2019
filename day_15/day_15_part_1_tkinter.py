from enum import Enum
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


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


def get_input() -> Direction:
    dir = input()
    dir = dir.lower()
    if dir in set(["w", "i"]):
        return Direction.NORTH
    elif dir in set(["a", "j"]):
        return Direction.WEST
    elif dir in set(["s", "k"]):
        return Direction.SOUTH
    elif dir in set(["d", "l"]):
        return Direction.EAST


def print_terrain(terrain):
    for row in terrain:
        print([terrain[row][col] for col in terrain[row]])


def analyze(file):
    with open(file) as f:
        opcodes = [int(i) for i in f.readline().strip().split(",")]
    comp = run_int_comp(opcodes)
    next(comp)
    pos = (0, 0)
    terrain = defaultdict(lambda: defaultdict(lambda: 3))  # nothing by default
    while True:
        direction = get_input()
        status = comp.send(direction.value)
        print(status)
        if direction is Direction.NORTH:
            x, y = pos[0], pos[1] - 1
        elif direction is Direction.SOUTH:
            x, y = pos[0], pos[1] + 1
        elif direction is Direction.WEST:
            x, y = pos[0] - 1, pos[1]
        elif direction is Direction.EAST:
            x, y = pos[0] + 1, pos[1]

        if status == 0:
            terrain[y][x] = 1  # 1 is a wall
        elif status == 1:
            pos = (x, y)
            terrain[y][x] = 0
        elif status == 2:
            pos = (x, y)
            terrain[y][x] = 2  # 2 is an oxygen tank
        print_terrain(terrain, pos)
        next(comp)


if __name__ == '__main__':
    analyze("inputs/day_15.txt")
