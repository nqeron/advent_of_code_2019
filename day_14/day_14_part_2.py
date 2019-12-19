import re
from collections import defaultdict, namedtuple
import typing
import math

Reaction = namedtuple("Reaction", "quantity name")


def can_be_made(reactions: typing.List[Reaction], current_amount) -> int:
    react_dict = defaultdict(lambda: 0)
    react_dict.update({r.name: r.quantity for r in reactions})
    # print([current_amount[elem] // react_dict[elem] for elem in current_amount if react_dict[elem] > 0])
    return min([current_amount[elem] // react_dict[elem] if react_dict[elem] > 0 else 0 for elem in current_amount
                if react_dict[elem] > 0])


def needed_to_make(product, to_make_product, chemistry) -> int:
    react_dict = defaultdict(lambda: 0)
    react_dict.update({i.name: i.quantity for i in chemistry[to_make_product][:-1]})
    return react_dict[product]


def analyze(file, given_ore):
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
    distance_to_fuel = defaultdict(lambda: 0)
    # calc_distance = True
    while len(to_produce) > 0:
        next_production = to_produce.pop()
        next_amount = amount_stack.pop()
        if next_production.name == "ORE":
            total_ore += next_amount // next_production.quantity
            current_amount[next_production.name] += next_amount
            continue
        else:
            produced = int(chemistry[next_production.name][-1])
            needed = next_amount - current_amount[next_production.name]
            crafted = needed // produced + (1 * (0 if needed % produced == 0 else 1))

            add_to_produce = chemistry[next_production.name][:-1]
            to_produce.extend(add_to_produce)

            for i in add_to_produce:
                to_craft_i = i.quantity * crafted  # - current_amount[i.name]
                # current_amount[i.name] += to_craft_i
                # if calc_distance:
                distance_to_fuel[i.name] = distance_to_fuel[next_production.name] + 1
                amount_stack.append(to_craft_i)

            current_amount[next_production.name] += crafted * produced - needed - current_amount[next_production.name]

    print(current_amount)
    first_crafts = given_ore // current_amount["ORE"]
    current_amount.update({i: current_amount[i] * first_crafts for i in current_amount})
    current_amount["FUEL"] += first_crafts
    current_amount["ORE"] = given_ore - current_amount["ORE"]
    print(current_amount)

    # to_make_product = "FUEL"
    while True:
        print(current_amount)
        print([(product, can_be_made(chemistry[product][:-1], current_amount),
                needed_to_make(product, to_make_product, chemistry))
               for product in chemistry for to_make_product in chemistry
               if product in set(i.name for i in chemistry[to_make_product][:-1])])
        next_product = min([(product, can_be_made(chemistry[product][:-1], current_amount),
                             needed_to_make(product, to_make_product, chemistry), to_make_product)
                            for product in chemistry for to_make_product in chemistry
                            if product == "FUEL" or product in set(i.name for i in chemistry[to_make_product][:-1])],
                           key=lambda x: distance_to_fuel[x[0]] * current_amount[x[0]] if x[1] > x[2] > 0 else math.inf)
        print(next_product)
        if next_product[1] <= 0:
            break
        reagent = next_product[0]
        have = current_amount[reagent]
        needed_for_reaction = next_product[2]
        production_amount = int(chemistry[reagent][-1])
        can_make = next_product[1]
        # crafts = needed_for_reaction // production_amount +\
        #          (1 * (0 if needed_for_reaction % production_amount == 0 else 1))   # - have
        crafts = can_make // production_amount + (1 * (0 if can_make % production_amount == 0 else 1))
        current_amount[reagent] += can_make
        for r in chemistry[reagent][:-1]:
            current_amount[r.name] -= crafts * r.quantity
        to_make_product = reagent
    print(current_amount["FUEL"])


if __name__ == '__main__':
    analyze("inputs/day_14_test3.txt", 1_000_000_000_000)
