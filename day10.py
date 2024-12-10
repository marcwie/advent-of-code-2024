import argparse

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def load(input_file):
    with open(input_file, "r") as infile:
        return [list(map(int, line)) for line in infile.read().splitlines()]


def find_paths(initial_position, topo, count_distinct):

    height = 0
    queue = [initial_position]
    n_rows, n_cols = len(topo), len(topo[0])

    while queue and height < 9:
        height += 1
        next_queue = []

        for x, y in queue:
            for dx, dy in DIRECTIONS:
                if (
                    0 <= x + dx < n_rows
                    and 0 <= y + dy < n_cols
                    and topo[x + dx][y + dy] == height
                ):
                    if count_distinct or (x + dx, y + dy) not in next_queue:
                        next_queue.append((x + dx, y + dy))

        queue = next_queue

    return len(queue)


def solve(input_file, count_distinct):

    topo = load(input_file)

    result = 0
    for i, line in enumerate(topo):
        for j, height in enumerate(line):
            if not height:
                result += find_paths((i, j), topo, count_distinct)

    return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, False))
    print("Part 2 solution:", solve(args.input_file, True))


if __name__ == "__main__":
    main()
