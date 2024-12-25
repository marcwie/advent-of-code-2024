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

    values = operations.values()
    or_operands = [x for op, *inp in values for x in inp if op == "OR"]
    and_xor_operands = [x for op, *inp in values for x in inp if op != "OR"]

    swap_candidates = set()
    for wire, (op, x0, x1) in operations.items():

        is_output = wire[0] == "z"
        is_input = x0[0] in ["x", "y"] or x1[0] in ["x", "y"]

        if is_output and op != "XOR" and wire != largest_z:
            swap_candidates.add(wire)

        if op == "XOR" and not is_input and not is_output:
            swap_candidates.add(wire)

        if op == "AND" and "x00" not in [x0, x1] and wire in and_xor_operands:
            swap_candidates.add(wire)

        if op == "XOR" and wire in or_operands:
            swap_candidates.add(wire)

    return ",".join(sorted(swap_candidates))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", part1(args.input_file))
    print("Part 2 solution:", part2(args.input_file))


if __name__ == "__main__":
    main()
