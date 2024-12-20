import argparse

DIRECTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]


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


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def ordered_path(input_file):

    path, (x, y), end = load(input_file)

    path_ordered = [(x, y)]

    while (x, y) != end:
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) in path:
                path.remove((x + dx, y + dy))
                path_ordered.append((x + dx, y + dy))

        x, y = path_ordered[-1]

    return path_ordered


def solve(input_file, cheat_length, min_savings):

    path = ordered_path(input_file)
    path = [(x, y, steps) for steps, (x, y) in enumerate(path)]

    result = 0

    for i, (x, y, steps) in enumerate(path):
        later_points = path[i:]
        later_points = [p for p in later_points if manhattan(p, (x, y)) <= cheat_length]
        time_saved = [p[2] - steps - manhattan(p, (x, y)) for p in later_points]
        result += sum([ts >= min_savings for ts in time_saved])

    return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, 2, 100))
    print("Part 2 solution:", solve(args.input_file, 20, 100))


if __name__ == "__main__":
    main()
