import argparse
from itertools import product


def load(input_file):

    with open(input_file, "r") as infile:
        data = infile.read()

    schematics = [schematic.splitlines() for schematic in data.split("\n\n")]
    keys, locks = [], []
    max_height = len(schematics[0]) - 2
    n_columns = len(schematics[0][0])

    for schematic in schematics:

        height = []
        for column in range(n_columns):
            height.append(sum([entry[column] == "#" for entry in schematic]) - 1)

        if schematic[0][0] == "#":
            locks.append(height)
        else:
            keys.append(height)

    return locks, keys, max_height


def solve(input_file):

    locks, keys, max_height = load(input_file)
    fits = 0

    for lock, key in product(locks, keys):
        fits += all([l + k <= max_height for l, k in zip(lock, key)])

    return fits


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file))


if __name__ == "__main__":
    main()
