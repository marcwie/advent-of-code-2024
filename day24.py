import argparse


def load(input_file):

    with open(input_file, "r") as infile:
        data = infile.read().splitlines()

    values = {}
    while data[0] != "":
        line = data.pop(0)
        wire, value = line.split(": ")
        values[wire] = int(value)

    data.pop(0)

    operations = {}
    for line in data:
        operation, target = line.split(" -> ")
        x0, operation, x1 = operation[:3], operation[4:-4], operation[-3:]
        operations[target] = [operation, x0, x1]
        values[target] = None

    return values, operations


def compute(operation, x0, x1):
    if operation == "XOR":
        return x0 ^ x1
    elif operation == "AND":
        return x0 & x1
    elif operation == "OR":
        return x0 | x1


def simulate(vals, operations):

    while None in vals.values():
        for target, (operation, x0, x1) in operations.items():
            if vals[x0] is not None and vals[x1] is not None and vals[target] is None:
                vals[target] = compute(operation, vals[x0], vals[x1])

    return vals


def extract_integer(vals, wires):

    results = [[key, value] for key, value in vals.items() if key[0] == wires]
    results.sort(key=lambda x: x[0], reverse=True)
    results = "".join([str(value) for _, value in results])
    return int(results, 2)


def part1(input_file):

    vals, operations = load(input_file)
    vals = simulate(vals, operations)
    return extract_integer(vals, "z")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", part1(args.input_file))


if __name__ == "__main__":
    main()
