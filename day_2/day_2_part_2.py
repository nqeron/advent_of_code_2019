
def analyze(file):
    with open(file) as f:
        original_codes = [int(i) for i in f.readline().split(",")]

    noun = 0
    verb = 0
    found = False
    for noun_iter in range(100):
        for verb_iter in range(100):
            opcodes = original_codes.copy()
            opcodes[1] = noun_iter
            opcodes[2] = verb_iter
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
                    break
                pos += 4
            if opcodes[0] == 19690720:
                found = True
                noun = noun_iter
                verb = verb_iter
                break
        if found:
            break
    print(noun*100+verb)


if __name__ == '__main__':
    analyze("../inputs/day_2.txt")