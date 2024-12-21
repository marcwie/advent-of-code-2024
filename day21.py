import argparse
from itertools import product
from collections import Counter


PAD = ["789", "456", "123", ".0A"]
ROBOT_PAD = [".^A", "<v>"]
DIRECTIONS = [(0, -1, "<"), (-1, 0, "^"), (0, 1, ">"), (1, 0, "v")]


def load(input_file):

    with open(input_file, "r") as infile:
        return infile.read().splitlines()


def buttons_coords(pad):
    """The coordinates of each button on either of the two pads."""
    combinations = product(range(len(pad)), range(len(pad[0])))
    return {pad[i][j]: (i, j) for i, j in combinations if pad[i][j] != "."}


def manhattan_distance(point1, point2):
    """Manhattan distance between two points."""
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def is_grouped(sequence):
    """
    Determine whether direction sequences are properly grouped.

    Returns True for sequences such as '>>^^' or 'vv>' and False for '<^<'.
    """
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i - 1] and sequence[i] in sequence[:i]:
            return False
    return True


def move_sequence(pad, start, end):

    if start == end:
        return "A"

    buttons = buttons_coords(pad)
    valid_coords = buttons.values()
    dist = manhattan_distance(buttons[start], buttons[end])

    x, y = buttons[start]
    sequence = ""
    stack = [(x, y, sequence)]
    valid_sequence = []

    while stack:
        for dx, dy, direction in DIRECTIONS:
            if len(sequence + direction) < dist and (x + dx, y + dy) in valid_coords:
                stack.append((x + dx, y + dy, sequence + direction))
            elif (x + dx, y + dy) == buttons[end] and is_grouped(sequence + direction):
                valid_sequence.append(sequence + direction + "A")

        x, y, sequence = stack.pop()

    if len(valid_sequence) == 2:
        return compare(*valid_sequence)

    return valid_sequence[0]


def all_move_sequences(pad):

    buttons = buttons_coords(pad)
    combinations = product(buttons.keys(), buttons.keys())
    sequences = {(p0, p1): move_sequence(pad, p0, p1) for p0, p1 in combinations}

    return sequences


def required_moves(sequence):

    moves = Counter(zip(sequence[:-1], sequence[1:]))
    moves[("A", sequence[0])] += 1

    return moves


def one_run(sequences, moves):

    counter = Counter()
    for move, count in moves.items():
        for next_move, next_count in required_moves(sequences[move]).items():
            counter[next_move] += count * next_count

    return counter


def compare(s1, s2):
    preferences = ["<", "v", "^", ">"]
    return s1 if preferences.index(s1[0]) < preferences.index(s2[0]) else s2


def solve(input_file, n_robots):

    data = load(input_file)
    keypad_sequences = all_move_sequences(PAD)
    robot_sequences = all_move_sequences(ROBOT_PAD)

    result = 0
    for code in data:
        moves = required_moves(code)
        moves = one_run(keypad_sequences, moves)
        for _ in range(n_robots):
            moves = one_run(robot_sequences, moves)

        result += sum(moves.values()) * int(code[:-1])

    return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, n_robots=2))
    print("Part 2 solution:", solve(args.input_file, n_robots=25))


if __name__ == "__main__":
    main()
