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


def solve_part2(input_file):

    data = load(input_file)
    obstacles, x, y, direction = setup(data)

    n_rows = len(data)
    n_cols = len(data[0])
    result = 0

    for i in range(n_rows):
        for j in range(n_cols):
            if (i, j) in obstacles:
                continue

            adapted_obstacles = obstacles | set([(i, j)])
            result += is_loop(adapted_obstacles, x, y, direction, n_rows, n_cols)

    return result


def solve_part1(input_file):

    data = load(input_file)
    obstacles, x, y, direction = setup(data)

    n_rows = len(data)
    n_cols = len(data[0])

    visited = set()

    while 0 <= y < n_rows and 0 <= x < n_cols:
        visited.add((y, x))
        if (y + direction[0], x + direction[1]) not in obstacles:
            y += direction[0]
            x += direction[1]
        else:
            direction = DIRECTIONS[direction[2]]

    return len(visited)


def main():

    assert solve_part1(input_file="inputs/day06/test.txt") == 41
    solution = solve_part1(input_file="inputs/day06/input.txt")
    print("Part 1 solution:", solution)
    assert solution == 4964

    assert solve_part2(input_file="inputs/day06/test.txt") == 6
    solution = solve_part2(input_file="inputs/day06/input.txt")
    print("Part 2 solution:", solution)
    assert solution == 1740


if __name__ == "__main__":
    main()
