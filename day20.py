import argparse
from collections import Counter

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
                    path.add((i, j))
                elif char == "E":
                    path.add((i, j))
                    end = (i, j)

    return path, start, end


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def order_path(path, start, end):

    steps = 0
    x, y = start
    ordered_path = [(x, y, steps)]
    seen = set()
    seen.add(start)

    while (x, y) != end:
        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) not in seen and (x + dx, y + dy) in path:
                seen.add((x + dx, y + dy))
                ordered_path.append((x + dx, y + dy, steps + 1))

        x, y, steps = ordered_path[-1]

    return ordered_path


def solve(input_file, cheat_len, min_savings):

    path, start, end = load(input_file)

    ordered_path = order_path(path, start, end)
    time = {(x, y): steps for x, y, steps in ordered_path}

    results = []

    for point in path:
        later_points = [p for p in path if time[p] > time[point]]
        later_points = [p for p in later_points if manhattan(p, point) <= cheat_len]
        time_saved = [time[p] - time[point] - manhattan(p, point) for p in later_points]
        time_saved = [ts for ts in time_saved if ts > 0]
        results.extend(time_saved)

    return sum([result >= min_savings for result in results])


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, 2, 100))
    print("Part 2 solution:", solve(args.input_file, 20, 100))


if __name__ == "__main__":
    main()
