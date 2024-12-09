import argparse

DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))
WORD = "XMAS"


def load(input_file):
    with open(input_file, "r") as infile:
        return infile.read().splitlines()


def is_cross(data, i, j):

    n_rows, n_chars = len(data), len(data[0])

    if data[i][j] != "A":
        return 0

    if i == 0 or i == n_rows - 1 or j == 0 or j == n_chars - 1:
        return 0

    if not (
        (data[i - 1][j - 1] == "M" and data[i + 1][j + 1] == "S")
        or (data[i - 1][j - 1] == "S" and data[i + 1][j + 1] == "M")
    ):
        return 0

    if not (
        (data[i - 1][j + 1] == "M" and data[i + 1][j - 1] == "S")
        or (data[i - 1][j + 1] == "S" and data[i + 1][j - 1] == "M")
    ):
        return 0

    return 1


def starts_xmas(data, i, j):

    n_rows, n_chars, result = len(data), len(data[0]), 0

    for vert, hor in DIRECTIONS:
        for k, letter in enumerate(WORD):
            if (
                not 0 <= i + vert * k < n_rows
                or not 0 <= j + hor * k < n_chars
                or data[i + vert * k][j + hor * k] != letter
            ):
                break
        else:
            result += 1

    return result


def solve(input_file, solve_func):

    data = load(input_file)

    n_rows = len(data)
    n_chars = len(data[0])
    result = 0

    for i in range(n_rows):
        for j in range(n_chars):
            result += solve_func(data, i, j)

    return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, starts_xmas))
    print("Part 2 solution:", solve(args.input_file, is_cross))


if __name__ == "__main__":
    main()
