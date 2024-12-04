def load(input_file):
    with open(input_file, "r") as infile:
        return infile.read()


def solve(input_file, with_instructions=False):

    data = load(input_file)

    if with_instructions:
        data = "do()" + data
        data = data.split("don't()")
        data = ["".join(entry.split("do()")[1:]) for entry in data]
        data = "".join(data)

    data = data.split("mul(")[1:]
    data = [entry.split(")")[0] for entry in data if ")" in entry]
    data = [entry.split(",") for entry in data if "," in entry]
    data = [entry for entry in data if entry[0].isdigit() and entry[1].isdigit()]
    data = [list(map(int, entry)) for entry in data]
    data = list(map(lambda x: x[0] * x[1], data))

    return sum(data)


def main():

    assert solve(input_file="inputs/day03/test1.txt") == 161
    solution = solve(input_file="inputs/day03/input.txt")
    print("Part 1 solution:", solution)
    assert solution == 167650499

    assert solve(input_file="inputs/day03/test2.txt", with_instructions=True) == 48
    solution = solve(input_file="inputs/day03/input.txt", with_instructions=True)
    print("Part 2 solution:", solution)
    assert solution == 95846796


if __name__ == "__main__":
    main()
