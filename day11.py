import argparse


def load(input_file):
    with open(input_file, "r") as infile:
        return infile.read().replace("\n", "").split(" ")


def blink(data):

    data_after_blink = {}

    for entry, count in data.items():

        if entry == "0":
            next_val = ["1"]
        elif not len(entry) % 2:
            n_digits = len(entry) // 2
            next_val = [entry[:n_digits], entry[n_digits:].lstrip("0") or "0"]
        else:
            next_val = [str(int(entry) * 2024)]

        for val in next_val:
            data_after_blink[val] = data_after_blink.get(val, 0) + count

    return data_after_blink


def solve(input_file, n_blinks):

    data = load(input_file)
    data = {val: 1 for val in data}

    for _ in range(n_blinks):
        data = blink(data)

    return sum(data.values())


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, 25))
    print("Part 2 solution:", solve(args.input_file, 75))


if __name__ == "__main__":
    main()
