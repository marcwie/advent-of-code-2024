import argparse


def parse_line(button, sep="+"):
    x, y = button.split(",")
    x = int(x.split(sep)[1])
    y = int(y.split(sep)[1])
    return x, y


def load(input_file):
    with open(input_file, "r") as infile:
        data = infile.read().splitlines()

    inputs = []

    for i in range(0, len(data) - 1, 4):
        button_A = parse_line(data[i])
        button_B = parse_line(data[i + 1])
        target = parse_line(data[i + 2], sep="=")
        inputs.append((button_A, button_B, target))

    return inputs


def cost(button_A, button_B, target, offset):

    xA, yA = button_A
    xB, yB = button_B
    X = target[0] + offset
    Y = target[1] + offset

    beta = (X * yA - Y * xA) / (yA * xB - yB * xA)
    alpha = (Y - beta * yB) / yA

    if alpha.is_integer() and beta.is_integer():
        return 3 * int(alpha) + int(beta)

    return 0


def solve(input_file, offset):

    data = load(input_file)

    total_cost = 0
    for buttonA, buttonB, target in data:
        total_cost += cost(buttonA, buttonB, target, offset)

    return total_cost


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, offset=0))
    print("Part 2 solution:", solve(args.input_file, offset=10000000000000))


if __name__ == "__main__":
    main()
