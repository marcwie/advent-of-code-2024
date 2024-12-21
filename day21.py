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

    combinations = product(range(len(pad)), range(len(pad[0])))
    return {pad[i][j]: (i, j) for i, j in combinations if pad[i][j] != "."}


def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def is_grouped(sequence):
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i - 1] and sequence[i] in sequence[:i]:
            return False
    return True


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

    moves = Counter(zip(code[:-1], code[1:]))
    moves[("A", code[0])] += 1

    return moves


def one_robot_run(robot_sequences, moves):

    print("getting reuqired moves")
    counter = get_required_moves(moves)

    print("getting robot moves")
    moves = [robot_sequences[move] * count for move, count in counter.items()]

    print("flattening moves")
    moves = "".join(moves)

    return moves


def get_best_robot_moves(robot_sequences):

    for keys, value in robot_sequences.items():
        if keys[0] == keys[1]:
            robot_sequences[keys] = "A"
        else:
            robot_sequences[keys] = value[0]


def get_best_keypad_moves(keypad_sequences, robot_sequences):

    for key, value in keypad_sequences.items():
        if len(value) > 1:
            v1, v2 = value
            p1 = one_robot_run(robot_sequences, one_robot_run(robot_sequences, v1))
            p2 = one_robot_run(robot_sequences, one_robot_run(robot_sequences, v2))
            keypad_sequences[key] = v1 if len(p1) <= len(p2) else v2
        else:
            keypad_sequences[key] = value[0] if value else ""


def solve(input_file, n_robots):

    data = load(input_file)

    keypad_sequences = get_all_move_sequences(PAD)
    robot_sequences = get_all_move_sequences(ROBOT_PAD)

    get_best_robot_moves(robot_sequences)
    get_best_keypad_moves(keypad_sequences, robot_sequences)

    result = 0

    for code in data:

        moves = get_required_moves(code)
        moves = [keypad_sequences[move] for move in moves.keys()]
        moves = "".join(moves)

        for _ in range(n_robots):
            print(code, _, len(moves))
            moves = one_robot_run(robot_sequences, moves)

        result += len(moves) * int(code[:-1])

    return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, n_robots=2))
    # print("Part 2 solution:", solve(args.input_file, n_robots=25))


if __name__ == "__main__":
    main()
