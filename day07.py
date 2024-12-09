import argparse


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

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, [add, multiply]))
    print("Part 2 solution:", solve(args.input_file, [add, multiply, concatenate]))


if __name__ == "__main__":
    main()
