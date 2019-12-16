from tkinter import *


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


class IntComp:

    def __init__(self, opcodes):
        self.int_comp = run_int_comp(opcodes)


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
                screen[y][x] = tile
        if sum([1 for k in screen for j in screen[k] if screen[k][j] == 2]) <= 0:
            break
        try:
            x = comp.send(0)
        except StopIteration:
            break
        else:
            new_screen = True


def run_comp(comp, screen, joy_pos):
    new_screen = True
    while True:
        try:
            if not new_screen:
                x = next(comp)
                if x is None:
                    break
            else:
                x = comp.send(joy_pos)
                new_screen = False
            y = next(comp)
            if new_screen and y is None:
                break
            tile = next(comp)
        except StopIteration:
            break
        else:
            screen[y][x] = tile


def draw_screen(canv, screen):
    canv.delete("all")
    for y in screen:
        for x in screen[y]:
            if x == -1 and y == 0:
                canv.create_text(30, 10, text="Score: {}".format(screen[y][x]))
            else:
                code = screen[y][x]
                if code == 0:
                    pass  # draw nothing?
                elif code == 1:
                    canv.create_rectangle(x*10+5, y*10+20, x*10+15, y*10+30, fill=["black"])
                elif code == 2:
                    canv.create_rectangle(x*10+5, y*10+20, x*10+15, y*10+30, fill=["green"])
                elif code == 3:
                    canv.create_rectangle(x*10+5, y*10+20, x*10+15, y*10+30, fill=["gray"])
                elif code == 4:
                    canv.create_oval(x*10+5, y*10+20, x*10+15, y*10+30, fill=["blue"])
    return True


def do_for_key(event: Event, canv, comp: IntComp, screen, initial_ops):
    keysym = str(event.keysym).lower()

    if keysym == "w" or keysym == "i" or keysym == "up" or keysym == "space":
        joy_pos = 0  # neutral
    elif keysym == "a" or keysym == "j" or keysym == "left":
        joy_pos = -1
    elif keysym == "d" or keysym == "l" or keysym == "right":
        joy_pos = 1
    elif keysym == "r":
        comp.int_comp = run_int_comp(initial_ops.copy())
        screen = defaultdict(lambda: defaultdict(lambda: 0))
        run_comp(comp.int_comp, screen, None)
        draw_screen(canv, screen)
        return
    else:
        return

    run_comp(comp.int_comp, screen, joy_pos)

    draw_screen(canv, screen)


def run_app(file):
    with open(file) as f:
        opcodes = [int(i) for i in f.readline().strip().split(",")]
    opcodes[0] = 2
    initial_ops = opcodes.copy()

    comp = IntComp(opcodes)
    screen = defaultdict(lambda: defaultdict(lambda: 0))

    master = Tk()

    canv = Canvas(master, width=500, height=500)
    canv.pack()

    run_comp(comp.int_comp, screen, None)
    draw_screen(canv, screen)

    canv.bind("<1>", lambda event: canv.focus_set())
    canv.bind("<Key>", lambda event: do_for_key(event, canv, comp, screen, initial_ops.copy()))

    master.mainloop()


if __name__ == '__main__':
    run_app("inputs/day_13.txt")
