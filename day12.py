import argparse

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
CORNER_DIRECTIONS = ((1, 1), (1, -1), (-1, 1), (-1, -1))


def load(input_file):
    with open(input_file, "r") as infile:
        return [list(line) for line in infile.read().splitlines()]


def find_corners(area):

    corners = 0

    for x, y in area:
        for dx, dy in CORNER_DIRECTIONS:
            if (x + dx, y) not in area and (x, y + dy) not in area:
                corners += 1
            elif (
                (x + dx, y) in area
                and (x, y + dy) in area
                and (x + dx, y + dy) not in area
            ):
                corners += 1

    return corners


def find_perimeter(area):

    perimeter = 0
    for x, y in area:
        for dx, dy in DIRECTIONS:
            if (
                (x + dx, y) not in area
                or (x, y + dy) not in area
                or (x + dx, y + dy) not in area
            ):
                perimeter += 1

    return perimeter


def find_area(data, i, j):

    queue = [(i, j)]
    visited = set()
    n_rows, n_cols = len(data), len(data[0])

    while queue:

        x, y = queue.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in DIRECTIONS:
            if (
                0 <= x + dx < n_rows
                and 0 <= y + dy < n_cols
                and (x + dx, y + dy) not in visited
                and data[x][y] == data[x + dx][y + dy]
            ):
                queue.append((x + dx, y + dy))

    return visited


def solve(input_file, cost_func):

    data = load(input_file)
    n_rows = len(data)
    n_cols = len(data[0])
    visited = set()

    result = 0

    for i in range(n_rows):
        for j in range(n_cols):
            if ((i, j)) not in visited:
                area = find_area(data, i, j)
                result += cost_func(area) * len(area)
                visited.update(area)

    return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, find_perimeter))
    print("Part 2 solution:", solve(args.input_file, find_corners))


if __name__ == "__main__":
    main()
