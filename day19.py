import argparse


def load(input_file):

    with open(input_file, "r") as infile:
        data = infile.read().splitlines()

    patterns = data[0].split(", ")
    designs = data[2:]

    return patterns, designs


def can_be_made(design, patterns):

    stack = [design]
    counter = {design: 1}

    while stack:

        stack = sorted(stack, key=len)
        design = stack.pop()

        for pattern in patterns:
            if design.startswith(pattern):
                next_design = design.removeprefix(pattern)
                if next_design in counter.keys():
                    counter[next_design] += counter[design]
                else:
                    stack.append(next_design)
                    counter[next_design] = counter[design]

    return counter.get("", 0)


def solve(input_file, part2=False):

    patterns, designs = load(input_file)
    results = [can_be_made(design, patterns) for design in designs]

    if not part2:
        return sum([result > 0 for result in results])

    return sum(results)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file))
    print("Part 2 solution:", solve(args.input_file, part2=True))


if __name__ == "__main__":
    main()
