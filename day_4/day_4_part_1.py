def check_for_descending(stringed) -> bool:
    for s in range(1, len(stringed)):
        if int(stringed[s]) < int(stringed[s - 1]):
            return False
    return True


def check_for_double(stringed) -> bool:
    for s in range(len(stringed) - 1):
        if stringed[s] == stringed[s+1]:
            return True


def analyze():
    print(sum([1 for i in range(197487, 673252) if check_for_double(str(i)) and check_for_descending(str(i))]))


if __name__ == '__main__':
    analyze()