from collections import Counter
import argparse


def load(input_file):
    with open(input_file, "r") as infile:
        inputs = infile.read().splitlines()

    inputs = list(map(int, inputs[0]))
    data = []

    for i, input in enumerate(inputs):
        if i % 2 == 0:
            data += input * [i // 2]
        else:
            data += input * [None]

    return data


def checksum(input):

    result = 0
    for i, id_number in enumerate(input):
        result += i * id_number
    return result


def solve_part1(input_file):

    input = load(input_file)

    n_digits = len([entry for entry in input if entry is not None])

    target = input[:n_digits]
    remain = [entry for entry in input[n_digits:] if entry]

    for i, entry in enumerate(target):
        if entry is None:
            target[i] = remain.pop()

    return checksum(target)


def solve_part2(input_file):

    input = load(input_file)
    right = len(input) - 1
    counter = Counter(input)

    while right > 0:

        if input[right]:

            n = counter[input[right]]
            right -= n - 1

            for j in range(right):
                if input[j : j + n] == [None] * n:
                    input[j : j + n] = [input[right]] * n
                    input[right : right + n] = [None] * n
                    break

        right -= 1

    input = [entry if entry else 0 for entry in input]

    return checksum(input)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve_part1(args.input_file))
    print("Part 2 solution:", solve_part2(args.input_file))


if __name__ == "__main__":
    main()
