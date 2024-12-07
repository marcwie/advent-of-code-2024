def load(input_file):
    with open(input_file, "r") as infile:
        data = infile.read().splitlines()

    data = [line.split(": ") for line in data]
    return {int(target): list(map(int, values.split(" "))) for target, values in data}


def add(x, y):
    return x + y


def multiply(x, y):
    return x * y


def concatenate(x, y):
    return int(str(x) + str(y))


def evaluate(target, values, operators):

    results = [values[0]]
    for val in values[1:]:
        results = [operator(res, val) for res in results for operator in operators]
        results = [res for res in results if res <= target]

    return (target in results) * target


def solve(input_file, operators):

    data = load(input_file)
    result = [evaluate(target, values, operators) for target, values in data.items()]
    return sum(result)


def main():

    assert solve("inputs/day07/test.txt", [add, multiply]) == 3749
    solution = solve("inputs/day07/input.txt", [add, multiply])
    print("Part 1 solution:", solution)
    assert solution == 932137732557

    assert solve("inputs/day07/test.txt", [add, multiply, concatenate]) == 11387
    solution = solve("inputs/day07/input.txt", [add, multiply, concatenate])
    print("Part 2 solution:", solution)
    assert solution == 661823605105500


if __name__ == "__main__":
    main()
