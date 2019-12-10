
def analyze(file):
    opcodes = []
    with open(file) as f:
        opcodes = [int(i) for i in f.readline().split(",")]
    print(opcodes)

    opcodes[1] = 12
    opcodes[2] = 2
    pos = 0
    while opcodes[pos] != 99:
        op = opcodes[pos]
        left = opcodes[pos+1]
        right = opcodes[pos+2]
        dest = opcodes[pos+3]

        if op == 1:
            opcodes[dest] = opcodes[left] + opcodes[right]
        elif op == 2:
            opcodes[dest] = opcodes[left] * opcodes[right]
        elif op == 99:
            break
        else:
            raise Exception("Unrecognized opcode")
        pos += 4
    print(opcodes[0])


if __name__ == '__main__':
    analyze("../inputs/day_2.txt")