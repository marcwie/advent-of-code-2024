import argparse
from itertools import product

PAD = ["789", "456", "123", ".0A"]
ROBOT_PAD = [".^A", "<v>"]
DIRECTIONS = [(0, -1, "<"), (-1, 0, "^"), (0, 1, ">"), (1, 0, "v")]


def load(input_file):

    with open(input_file, "r") as infile:
        return infile.read().splitlines()


def buttons_coords(pad):

    combinations = product(range(len(pad)), range(len(pad[0])))
    return {pad[i][j]: (i, j) for i, j in combinations if pad[i][j] != "."}


def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_move_sequence(pad, start, end):

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
            elif (x + dx, y + dy) == buttons[end]:
                valid_sequence.append(sequence + direction + "A")

        x, y, sequence = stack.pop()

    return [s for s in valid_sequence if is_grouped(s)]


def get_all_move_sequences(pad):

    buttons = buttons_coords(pad)
    combinations = product(buttons.keys(), buttons.keys())
    sequences = {(p0, p1): get_move_sequence(pad, p0, p1) for p0, p1 in combinations}

    return sequences


def get_required_moves(code):

    moves = [("A", code[0])]
    for i in range(1, len(code)):
        moves.append((code[i - 1], code[i]))

    return moves


def is_grouped(sequence):
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i - 1] and sequence[i] in sequence[:i]:
            return False
    return True


def flatten_moves(moves):
    return [move for move in product(*moves)]


def filter_unique_sequences(moves):

    sequences = []
    for move in moves:
        if sorted(move) not in sequences:
            sequences.append(sorted(move))
    return sequences


def one_robot_run(robot_sequences, moves):

    next_sequence = []

    for move in moves:
        moves = get_required_moves(move)
        moves = [robot_sequences[move] for move in moves]
        moves = flatten_moves(moves)
        moves = filter_unique_sequences(moves)
        moves = ["".join(move) for move in moves]
        next_sequence.extend(moves)

    return next_sequence


def solve(input_file, n_robots):

    data = load(input_file)

    keypad_sequences = get_all_move_sequences(PAD)
    robot_sequences = get_all_move_sequences(ROBOT_PAD)

    for keys in robot_sequences.keys():
        if keys[0] == keys[1]:
            robot_sequences[keys] = ["A"]

    result = 0

    for code in data:

        moves = get_required_moves(code)
        moves = [keypad_sequences[move] for move in moves]
        moves = ["".join(move) for move in flatten_moves(moves)]

        for _ in range(n_robots):
            moves = one_robot_run(robot_sequences, moves)

        moves = len(sorted(moves, key=len)[0])

        result += moves * int(code[:-1])

    return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, n_robots=2))
    # print("Part 2 solution:", solve(args.input_file, 20, 100))


if __name__ == "__main__":
    main()
