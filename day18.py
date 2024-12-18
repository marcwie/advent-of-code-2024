import argparse

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def load(input_file):

    with open(input_file, "r") as infile:
        data = infile.read().splitlines()

    data = [tuple(map(int, entry.split(","))) for entry in data]

    return data


def part1(input_file, size, n_bytes):

    obstacles = load(input_file)
    return run(obstacles, size, n_bytes)


def part2(input_file, size):

    obstacles = load(input_file)
    for i in range(len(obstacles) - 1, -1, -1):
        if run(obstacles, size, i):
            return str(obstacles[i][0]) + "," + str(obstacles[i][1])


def run(obstacles, size, n_bytes):

    obstacles = set(obstacles[:n_bytes])

    path = [(x, y) for x in range(size + 1) for y in range(size + 1)]
    path = set(path)
    path -= obstacles

    seen = set()
    x, y, steps = 0, 0, 0
    stack = []

    while (x, y) != (size, size):

        for dx, dy in DIRECTIONS:
            if (x + dx, y + dy) not in seen and (x + dx, y + dy) in path:
                seen.add((x + dx, y + dy))
                stack.append((x + dx, y + dy, steps + 1))

        if not stack:
            return None

        stack = sorted(stack, key=lambda x: -x[2])
        x, y, steps = stack.pop()

    return steps


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--size", type=int, default=70)
    parser.add_argument("--n_bytes", type=int, default=1024)
    args = parser.parse_args()

    print("Part 1 solution:", part1(args.input_file, args.size, args.n_bytes))
    print("Part 2 solution:", part2(args.input_file, args.size))


if __name__ == "__main__":
    main()
