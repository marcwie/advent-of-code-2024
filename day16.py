import argparse

DIRECTION_CHANGE = {
    "^": (("^", 1), ("<", 1001), (">", 1001)),
    ">": ((">", 1), ("^", 1001), ("v", 1001)),
    "v": (("v", 1), ("<", 1001), (">", 1001)),
    "<": (("<", 1), ("^", 1001), ("v", 1001)),
}

DIRECTIONS = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}


def load(input_file):

    path = set()
    with open(input_file, "r") as infile:
        for i, line in enumerate(infile.read().splitlines()):
            for j, char in enumerate(line):
                if char == ".":
                    path.add((i, j))
                elif char == "S":
                    start = (i, j)
                elif char == "E":
                    path.add((i, j))
                    end = (i, j)

    return path, start, end


def solve(input_file):

    path, (x, y), end = load(input_file)
    direction, cost = ">", 0
    seen, positions = set(), []

    while (x, y) != end:

        for next_dir, dcost in DIRECTION_CHANGE[direction]:

            next_x = x + DIRECTIONS[next_dir][0]
            next_y = y + DIRECTIONS[next_dir][1]
            if (next_x, next_y, next_dir) not in seen and (next_x, next_y) in path:
                seen.add((next_x, next_y, next_dir))
                positions.append((next_x, next_y, next_dir, cost + dcost))

        positions = sorted(positions, key=lambda x: -x[3])
        x, y, direction, cost = positions.pop()

    return cost


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file))
    # print("Part 2 solution:", solve(args.input_file, True))


if __name__ == "__main__":
    main()
