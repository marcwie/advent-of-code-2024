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


def solve(input_file, find_all_paths=False):

    # Part 1
    path, start, end = load(input_file)
    (x, y), direction, cost = start, ">", 0
    seen, positions, current_path, abandoned_paths = set(), [], [], []

    while (x, y) != end:

        for next_dir, dcost in DIRECTION_CHANGE[direction]:

            next_x = x + DIRECTIONS[next_dir][0]
            next_y = y + DIRECTIONS[next_dir][1]
            next_cost = cost + dcost
            next_current_path = current_path + [(next_x, next_y, next_dir, next_cost)]

            if (next_x, next_y) in path:
                if (next_x, next_y, next_dir) not in seen:
                    seen.add((next_x, next_y, next_dir))
                    positions.append(next_current_path)
                elif current_path not in abandoned_paths:
                    abandoned_paths.append((next_current_path))

        positions = sorted(positions, key=lambda x: -x[-1][3])
        current_path = positions.pop()
        x, y, direction, cost = current_path[-1]

    if not find_all_paths:
        return current_path[-1][3]

    # Part 2 - builds on part 1
    current_path = set(current_path)
    n_steps = 0
    while n_steps != len(current_path):
        n_steps = len(current_path)
        for path_taken in abandoned_paths:
            if path_taken[-1] in current_path and not set(path_taken) <= current_path:
                current_path |= set(path_taken)

    current_path = set([(x, y) for x, y, _, _ in current_path] + [start])
    return len(current_path)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, False))
    print("Part 2 solution:", solve(args.input_file, True))


if __name__ == "__main__":
    main()
