from collections import defaultdict
from enum import Enum


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
    opcodes += [0] * 1000
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
    UP = 1,
    RIGHT = 2,
    DOWN = 3,
    LEFT = 4

    def rotate_left(self):
        if self is Direction.UP:
            return Direction.LEFT
        elif self is Direction.LEFT:
            return Direction.DOWN
        elif self is Direction.DOWN:
            return Direction.RIGHT
        elif self is Direction.RIGHT:
            return Direction.UP

    def rotate_right(self):
        if self is Direction.UP:
            return Direction.RIGHT
        elif self is Direction.LEFT:
            return Direction.UP
        elif self is Direction.DOWN:
            return Direction.LEFT
        elif self is Direction.RIGHT:
            return Direction.DOWN


def analyze(file):
    with open(file) as f:
        opcodes = [int(c) for c in f.readline().strip().split(",")]

    op_runner = run_int_comp(opcodes)
    next(op_runner)
    hull = defaultdict(lambda: 0)
    painted = set()
    pos_x, pos_y = 0, 0
    direction = Direction.UP
    hull[(0, 0)] = 1
    while True:
        cur_paint = hull[(pos_x, pos_y)]
        try:
            to_paint = op_runner.send(cur_paint)
            to_dir = next(op_runner)
            c = next(op_runner)
            painted.add((pos_x, pos_y))
        except StopIteration:
            break
        hull[(pos_x, pos_y)] = to_paint
        if to_dir == 0:
            direction = Direction.rotate_left(direction)
        else:
            direction = Direction.rotate_right(direction)
        if direction is Direction.UP:
            pos_x, pos_y = pos_x, pos_y + 1
        elif direction is Direction.DOWN:
            pos_x, pos_y = pos_x, pos_y - 1
        elif direction is Direction.RIGHT:
            pos_x, pos_y = pos_x + 1, pos_y
        elif direction is Direction.LEFT:
            pos_x, pos_y = pos_x - 1, pos_y

    for i in [[' ' if hull[(x, y)] == 0 else '#' for x in range(-50,50)] for y in range(50, -50, -1)]:
        print(i)


if __name__ == '__main__':
    analyze("../inputs/day_11.txt")
