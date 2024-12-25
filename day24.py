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


def part2(input_file):

    vals, operations = load(input_file)
    largest_z = max([key for key in vals if key[0] == "z"])

    swap_candidates = set()
    for key, (op, x0, x1) in operations.items():

        if key[0] == "z" and op != "XOR" and key != largest_z:
            swap_candidates.add(key)

        if (
            op == "XOR"
            and x0[0] not in ["x", "y"]
            and x1[0] not in ["x", "y"]
            and key[0] != "z"
        ):
            swap_candidates.add(key)

        for _op, _x0, _x1 in operations.values():
            if (
                op == "AND"
                and "x00" not in [x0, x1]
                and key in [_x0, _x1]
                and _op != "OR"
            ):
                swap_candidates.add(key)
            elif op == "XOR" and key in [_x0, _x1] and _op == "OR":
                swap_candidates.add(key)

    return ",".join(sorted(swap_candidates))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", part1(args.input_file))
    print("Part 2 solution:", part2(args.input_file))


if __name__ == "__main__":
    main()
