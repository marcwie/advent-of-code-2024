import argparse
from itertools import product
from collections import Counter

N_NUMBERS = 2000


def load(input_file):

    with open(input_file, "r") as infile:
        return list(map(int, infile.read().splitlines()))


def next_number(x):
    x = (x ^ (x * 64)) % 16777216
    x = (x ^ (x // 32)) % 16777216
    x = (x ^ (x * 2048)) % 16777216
    return x


def solve(input_file):

    data = load(input_file)

    total_sales = Counter()
    sum_of_numbers = 0

    for number in data:

        # Compute sequence of numbers. Needed for both parts
        numbers = [number]
        for _ in range(N_NUMBERS - 1):
            numbers.append(next_number(numbers[-1]))

        # Part 1
        sum_of_numbers += numbers[-1]

        # Part 2
        sales = Counter()
        numbers = [n % 10 for n in numbers]
        diff = [None] + [numbers[i] - numbers[i - 1] for i in range(1, N_NUMBERS)]

        for i in range(4, N_NUMBERS):
            key = tuple(diff[i - 3 : i + 1])
            sales[key] = sales[key] or numbers[i]

        total_sales += sales

    return sum_of_numbers, total_sales.most_common(1)[0][1]


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    part1, part2 = solve(args.input_file)
    print("Part 1 solution:", part1)
    print("Part 2 solution:", part2)


if __name__ == "__main__":
    main()
