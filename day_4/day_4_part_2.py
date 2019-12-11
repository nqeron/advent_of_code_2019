

def check_for_descending(stringed) -> bool:
    for s in range(1, len(stringed)):
        if int(stringed[s]) < int(stringed[s - 1]):
            return False
    return True


def check_for_double(stringed) -> bool:
    s = 0
    while s < len(stringed) - 1:
        if stringed[s] == stringed[s+1]:
            if len(stringed) > s+2 and stringed[s+2] == stringed[s]:
                s += 2
                continue
            else:
                return True
        s += 1
    return False


def analyze():
    print(check_for_double(str(333222)))
    print(sum([1 for i in range(197487, 673252) if check_for_double(str(i)) and check_for_descending(str(i))]))


if __name__ == '__main__':
    analyze()