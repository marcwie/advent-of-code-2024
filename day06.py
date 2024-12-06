DIRECTIONS = {">": (0, 1, "v"), "v": (1, 0, "<"), "<": (0, -1, "^"), "^": (-1, 0, ">")}


def load(input_file):
    with open(input_file, "r") as infile:
        return infile.read().splitlines()


def setup(data):

    obstacles = set()
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == "#":
                obstacles.add((i, j))
            elif char in DIRECTIONS.keys():
                y, x = i, j
                direction = DIRECTIONS[char]

    return obstacles, x, y, direction


def is_loop(obstacles, x, y, direction, n_rows, n_cols):

    visited = set()

    while 0 <= y < n_rows and 0 <= x < n_cols:

        if (y, x, direction) in visited:
            return 1

        visited.add((y, x, direction))
        if (y + direction[0], x + direction[1]) not in obstacles:
            y += direction[0]
            x += direction[1]
        else:
            direction = DIRECTIONS[direction[2]]

    return 0


def part2(obstacles, x, y, direction, n_cols, n_rows):

    result = 0

    for i in range(n_rows):
        for j in range(n_cols):
            if (i, j) not in obstacles:
                adapted_obstacles = obstacles | set([(i, j)])
                result += is_loop(adapted_obstacles, x, y, direction, n_rows, n_cols)

    return result


def part1(obstacles, x, y, direction, n_cols, n_rows):

    visited = set()

    while 0 <= y < n_rows and 0 <= x < n_cols:
        visited.add((y, x))
        if (y + direction[0], x + direction[1]) not in obstacles:
            y += direction[0]
            x += direction[1]
        else:
            direction = DIRECTIONS[direction[2]]

    return len(visited)


def solve(input_file, solve_func):

    data = load(input_file)
    obstacles, x, y, direction = setup(data)

    n_rows = len(data)
    n_cols = len(data[0])

    return solve_func(obstacles, x, y, direction, n_cols, n_rows)


def main():

    assert solve("inputs/day06/test.txt", part1) == 41
    solution = solve("inputs/day06/input.txt", part1)
    print("Part 1 solution:", solution)
    assert solution == 4964

    assert solve("inputs/day06/test.txt", part2) == 6
    solution = solve("inputs/day06/input.txt", part2)
    print("Part 2 solution:", solution)
    assert solution == 1740


if __name__ == "__main__":
    main()
