import argparse

DIRECTIONS = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}


def load(input_file):

    walls = []
    boxes = []
    movements = ""

    with open(input_file, "r") as infile:

        for i, line in enumerate(infile.read().splitlines()):

            if line and line[0] in DIRECTIONS.keys():
                movements += line
                continue

            for j, char in enumerate(line):
                if char == "#":
                    walls.append((i, j))
                elif char == "O":
                    boxes.append((i, j))
                elif char == "@":
                    robot = (i, j)

    return robot, walls, boxes, movements


def solve(input_file):
    robot, walls, boxes, movements = load(input_file)
    directions = [DIRECTIONS[move] for move in movements]

    x, y = robot
    for dx, dy in directions:

        if (x + dx, y + dy) not in walls and (x + dx, y + dy) not in boxes:
            x, y = x + dx, y + dy

        elif (x + dx, y + dy) in boxes:
            box_line = [(x + dx, y + dy)]

            while (box_line[-1][0] + dx, box_line[-1][1] + dy) in boxes:
                box_line.append((box_line[-1][0] + dx, box_line[-1][1] + dy))

            if (box_line[-1][0] + dx, box_line[-1][1] + dy) not in walls:
                x, y = x + dx, y + dy
                box_indices = [boxes.index(box) for box in box_line]
                for j, (box_x, box_y) in zip(box_indices, box_line):
                    boxes[j] = (box_x + dx, box_y + dy)

    return sum([100 * x + y for x, y in boxes])


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file))


if __name__ == "__main__":
    main()
