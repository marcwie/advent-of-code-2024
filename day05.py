def load(input_file):

    rules = []
    instructions = []

    with open(input_file, "r") as infile:

        for line in infile.read().splitlines():

            if "|" in line:
                rules.append(list(map(int, line.split("|"))))
            elif "," in line:
                instructions.append(list(map(int, line.split(","))))

    return rules, instructions


def rules_dictionary(rules):

    rules_dic = {}

    for page, allowed_follows in rules:

        if page not in rules_dic.keys():
            rules_dic[page] = set()
        if allowed_follows not in rules_dic.keys():
            rules_dic[allowed_follows] = set()

        rules_dic[page].add(allowed_follows)

    return rules_dic


def middle_page_if_valid(rules, instruction):

    allowed_pages = rules[instruction[0]]

    for page in instruction[1:]:

        if page not in allowed_pages:
            return 0

        allowed_pages = allowed_pages & rules[page]

    middle = len(instruction) // 2

    return instruction[middle]


def middle_page_if_invalid(rules, instruction):

    if middle_page_if_valid(rules, instruction):
        return 0

    instruction = set(instruction)
    rules = {
        page: rule & instruction for page, rule in rules.items() if page in instruction
    }

    new_ordering = []

    for i in range(len(instruction) - 1, -1, -1):
        for page, rule in rules.items():
            if len(rule) == i:
                new_ordering.append(page)
                continue

    middle = len(new_ordering) // 2

    return new_ordering[middle]


def solve(input_file, solve_func):

    rules, instructions = load(input_file)
    rules = rules_dictionary(rules)

    result = 0
    for instruction in instructions:
        result += solve_func(rules, instruction)

    return result


def main():

    assert solve("inputs/day05/test.txt", middle_page_if_valid) == 143
    solution = solve("inputs/day05/input.txt", middle_page_if_valid)
    print("Part 1 solution:", solution)
    assert solution == 4135

    assert solve("inputs/day05/test.txt", middle_page_if_invalid) == 123
    solution = solve("inputs/day05/input.txt", middle_page_if_invalid)
    print("Part 2 solution:", solution)
    assert solution == 5285


if __name__ == "__main__":
    main()
