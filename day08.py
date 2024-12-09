import argparse


def load(input_file):
    with open(input_file, "r") as infile:
        data = infile.read().splitlines()

    positions = {}
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == ".":
                continue

            if char in positions.keys():
                positions[char].append((i, j))
            else:
                positions[char] = [(i, j)]

    n_rows, n_cols = len(data), len(data[0])

    return positions, n_rows, n_cols


def find_antinodes(positions, n_rows, n_cols):

    antinodes = set()

    for i, (xi, yi) in enumerate(positions):
        for xj, yj in positions[i + 1 :]:
            dx, dy = xj - xi, yj - yi

            if 0 <= xj + dx < n_rows and 0 <= yj + dy < n_cols:
                antinodes.add((xj + dx, yj + dy))
            if 0 <= xi - dx < n_rows and 0 <= yi - dy < n_cols:
                antinodes.add((xi - dx, yi - dy))

    return antinodes


def find_diagonal(positions, n_rows, n_cols):

    antinodes = set()

    for i, (xi, yi) in enumerate(positions):
        for xj, yj in positions[i + 1 :]:
            dx, dy = xj - xi, yj - yi

            x, y = xj, yj
            while 0 <= x < n_rows and 0 <= y < n_cols:
                antinodes.add((x, y))
                x, y = x + dx, y + dy

            x, y = xj, yj
            while 0 <= x < n_rows and 0 <= y < n_cols:
                antinodes.add((x, y))
                x, y = x - dx, y - dy

    return antinodes


def solve(input_file, solve_func):

    positions, n_rows, n_cols = load(input_file)
    antinodes = set()

    for pos in positions.values():
        antinodes |= solve_func(pos, n_rows, n_cols)

    return len(antinodes)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, find_antinodes))
    print("Part 2 solution:", solve(args.input_file, find_diagonal))


if __name__ == "__main__":
    main()
