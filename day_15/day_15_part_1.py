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


class Tile(Enum):
    Empty = 0
    Wall = 1
    Oxygen = 2
    Unknown = 3


# def get_input() -> Direction:
#     while True:
#         dir = input()
#         dir = dir.lower()
#         if dir in set(["w", "i"]):
#             return Direction.NORTH
#         elif dir in set(["a", "j"]):
#             return Direction.WEST
#         elif dir in set(["s", "k"]):
#             return Direction.SOUTH
#         elif dir in set(["d", "l"]):
#             return Direction.EAST

def turn_right(running):
    if running is Direction.WEST:
        running = Direction.NORTH
    elif running is Direction.EAST:
        running = Direction.SOUTH
    elif running is Direction.NORTH:
        running = Direction.EAST
    elif running is Direction.SOUTH:
        running = Direction.WEST
    return running


def turn_left(running):
    if running is Direction.WEST:
        running = Direction.SOUTH
    elif running is Direction.EAST:
        running = Direction.NORTH
    elif running is Direction.NORTH:
        running = Direction.WEST
    elif running is Direction.SOUTH:
        running = Direction.EAST
    return running


def next_pos_is_empty(terrain, pos, direction: Direction) -> bool:
    x, y = pos
    if direction is Direction.NORTH:
        x, y = x, y - 1
    elif direction is Direction.SOUTH:
        x, y = x, y + 1
    elif direction is Direction.WEST:
        x, y = x - 1, y
    elif direction is Direction.EAST:
        x, y = x + 1, y
    return terrain[(x, y)] is Tile.Unknown


def next_on_right(terrain, pos, running: Direction) -> Tile:
    x, y = pos
    if running is Direction.NORTH:
        x, y = x + 1, y
    elif running is Direction.SOUTH:
        x, y = x - 1, y
    elif running is Direction.WEST:
        x, y = x, y - 1
    elif running is Direction.EAST:
        x, y = x, y + 1
    return terrain[(x, y)]


def next_on_left(terrain, pos, running):
    x, y = pos
    if running is Direction.NORTH:
        x, y = x - 1, y
    elif running is Direction.SOUTH:
        x, y = x + 1, y
    elif running is Direction.WEST:
        x, y = x, y + 1
    elif running is Direction.EAST:
        x, y = x, y - 1
    return terrain[(x, y)]


def get_input(terrain, pos, running: Direction, prev_status, steps) -> Direction:
    if prev_status == 0:
        if next_on_left(terrain, pos, running) is Tile.Empty:
            steps -= 1
        return turn_left(running), steps
    # steps += 1
    # if terrain[(x, y)] is Tile.Unknown:
    #     steps += 1
    #     return turn_right(running), steps
    # steps -= 1
    right_tile = next_on_right(terrain, pos, running)
    if right_tile in set([Tile.Wall, Tile.Unknown]):
        steps += 1
    elif right_tile is Tile.Empty:
        steps -= 1
    return turn_right(running), steps


def get_char(terrain, x, y, pos, direction: Direction):
    if pos[0] == x and pos[1] == y:
        if direction is Direction.NORTH:
            return '^'
        elif direction is Direction.SOUTH:
            return 'v'
        elif direction is Direction.WEST:
            return '<'
        elif direction is Direction.EAST:
            return '>'
    elif x == 0 and y == 0:
        return "S"
    code = terrain[(x, y)]
    if code is Tile.Empty:
        return ' '
    elif code is Tile.Wall:
        return '#'
    elif code is Tile.Oxygen:
        return 'O'
    elif code is Tile.Unknown:
        return '?'


def print_terrain(terrain, pos, direction):
    left = min([point[0] for point in terrain.keys() if terrain[point] is not Tile.Unknown]) - 1
    right = max([point[0] for point in terrain.keys() if terrain[point] is not Tile.Unknown]) + 1
    top = min([point[1] for point in terrain.keys() if terrain[point] is not Tile.Unknown]) - 1
    bottom = max([point[1] for point in terrain.keys() if terrain[point] is not Tile.Unknown]) + 1

    for y in range(top, bottom + 1):
        print(''.join([get_char(terrain, x, y, pos, direction) for x in range(left, right + 1)]))


def analyze(file):
    with open(file) as f:
        opcodes = [int(i) for i in f.readline().strip().split(",")]
    comp = run_int_comp(opcodes)
    next(comp)
    pos = (0, 0)
    terrain = defaultdict(lambda: Tile.Unknown)  # nothing by default
    terrain[(0, 0)] = Tile.Empty
    prev_status = 1
    running = Direction.WEST
    steps = 0
    while terrain[pos] is not Tile.Oxygen:
        direction, steps = get_input(terrain, pos, running, prev_status, steps)
        running = direction
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
            terrain[(x, y)] = Tile.Wall  # 1 is a wall
        elif status == 1:
            pos = (x, y)
            terrain[(x, y)] = Tile.Empty
        elif status == 2:
            pos = (x, y)
            terrain[(x, y)] = Tile.Oxygen  # 2 is an oxygen tank
        print_terrain(terrain, pos, running)
        print(steps)
        prev_status = status
        next(comp)
    print(steps)


if __name__ == '__main__':
    analyze("inputs/day_15.txt")
