import argparse


def load(input_file):

    with open(input_file, "r") as infile:
        data = infile.read().splitlines()

    register = [int(entry.split(": ")[1]) for entry in data[:3]]
    program = list(map(int, data[-1][8:].split(",")))

    return program, register


def part2(input_file):

    program, (_, B, C) = load(input_file)

    stack = [(0, 0)]
    while stack:

        # Sort the stack so that the lowest value of A is evaluated first
        stack = sorted(stack, key=lambda x: -x[0])
        A, depth = stack.pop()

        # If the stack went as deep as the length of the program,
        # we are certain to have found a solution
        if depth == len(program):
            return A

        # Since the program divides by 8 and keeps only the integer part, we reverse this process
        # through multiplying by 8 and then testing all 8 numbers that incrementally start from
        # there, as those would in turn again all give the same integer when divided by 8.
        # In addition, we exclude 0 and start our iteration from a smallest value of 1.
        for i in range(0 if A else 1, 8):
            next_a = A * 8 + i
            output = run(program, next_a, B, C)

            # If the first digit of the outputs matches the target at inverse depth
            # we have found another candidate
            if output[0] == program[-depth - 1]:
                stack.append((next_a, depth + 1))

    return 0


def part1(input_file):
    program, register = load(input_file)
    output = run(program, *register)
    return ",".join(map(str, output))


def run(program, A, B, C):

    pointer = 0
    output = []

    while pointer < len(program):
        opcode, operand = program[pointer : pointer + 2]
        combo_operand = [0, 1, 2, 3, A, B, C][operand]
        pointer += 2
        if opcode == 0:
            A //= 2**combo_operand
        elif opcode == 1:
            B ^= operand
        elif opcode == 2:
            B = combo_operand % 8
        elif opcode == 3:
            pointer = pointer if not A else operand
        elif opcode == 4:
            B ^= C
        elif opcode == 5:
            output.append(combo_operand % 8)
        elif opcode == 6:
            B = A // 2**combo_operand
        elif opcode == 7:
            C = A // 2**combo_operand

    return output


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", part1(args.input_file))
    print("Part 2 solution:", part2(args.input_file))


if __name__ == "__main__":
    main()
