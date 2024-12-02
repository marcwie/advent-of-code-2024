def load(input_file):

    with open(input_file, "r") as infile:
        return [list(map(int, row.split(" "))) for row in infile]


def is_safe(level):

    diffs = [level[i + 1] - level[i] for i in range(len(level) - 1)]
    valid_desc = all([-3 <= diff <= -1 for diff in diffs])
    valid_asc = all([1 <= diff <= 3 for diff in diffs])
    return valid_desc or valid_asc


def is_safe_with_dampener(level):

    if is_safe(level):
        return True

    for i in range(len(level)):
        if is_safe(level[:i] + level[i + 1 :]):
            return True

    return False


def solve(input_file, eval_func):

    return sum([eval_func(level) for level in load(input_file)])


def main():

    test = solve(input_file="inputs/day02/test.txt", eval_func=is_safe)
    assert test == 2

    result = solve(input_file="inputs/day02/input.txt", eval_func=is_safe)
    print("Part 1 solution:", result)
    assert result == 383

    test = solve(input_file="inputs/day02/test.txt", eval_func=is_safe_with_dampener)
    assert test == 4

    result = solve(input_file="inputs/day02/input.txt", eval_func=is_safe_with_dampener)
    print("Part 2 solution:", result)
    assert result == 436


if __name__ == "__main__":
    main()
