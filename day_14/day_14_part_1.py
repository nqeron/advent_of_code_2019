import re
from collections import defaultdict, namedtuple

Reaction = namedtuple("Reaction", "quantity name")


def analyze(file):
    line_matcher = re.compile(r"(\d+) (\w+)")
    chemistry = {}
    with open(file) as f:
        for line in f:
            equation = line_matcher.findall(line)
            product = equation[-1][1]
            chemistry[product] = [Reaction(int(e[0]), e[1]) for e in equation[:-1]] + [equation[-1][0]]

    to_produce = chemistry["FUEL"][:-1]
    amount_stack = [i.quantity * 1 for i in chemistry["FUEL"][:-1]]
    total_ore = 0
    current_amount = defaultdict(lambda: 0)
    prev_item = Reaction(1, "FUEL")
    while len(to_produce) > 0:
        next_production = to_produce.pop()
        next_amount = amount_stack.pop()
        if next_production.name == "ORE":
            total_ore += next_amount // next_production.quantity
            current_amount[next_production.name] += next_production.quantity
            continue
        else:
            produced = int(chemistry[next_production.name][-1])
            crafted = next_amount // produced + (1 * (0 if next_amount % produced == 0 else 1))

            add_to_produce = chemistry[next_production.name][:-1]
            to_produce.extend(add_to_produce)

            for i in add_to_produce:
                to_craft_i = i.quantity * crafted - current_amount[i.name]
                current_amount[i.name] += to_craft_i
                amount_stack.append(to_craft_i)

            current_amount[next_production.name] += crafted
            prev_item = next_production
    print(current_amount)


if __name__ == '__main__':
    analyze("inputs/day_14_test.txt")
