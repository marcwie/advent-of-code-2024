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


def expand_map(robot, walls, boxes):

    expanded_walls = [(x, 2 * y + k) for x, y in walls for k in (0, 1)]
    expanded_boxes = [(x, 2 * y + k) for x, y in boxes for k in (0, 1)]
    expanded_robot = (robot[0], 2 * robot[1])

    box_connection = {}
    for i in range(len(boxes)):
        box_connection[2 * i] = 2 * i + 1
        box_connection[2 * i + 1] = 2 * i

    return expanded_robot, expanded_walls, expanded_boxes, box_connection


def move_horizontal(x, y, dy, boxes, walls):

    box_line = [(x, y + dy)]

    while (box_line[-1][0], box_line[-1][1] + dy) in boxes:
        box_line.append((box_line[-1][0], box_line[-1][1] + dy))

    if (box_line[-1][0], box_line[-1][1] + dy) not in walls:
        y = y + dy
        box_indices = [boxes.index(box) for box in box_line]
        for j, (box_x, box_y) in zip(box_indices, box_line):
            boxes[j] = (box_x, box_y + dy)

    return x, y, boxes


def move_vertical(x, y, dx, boxes, box_connection, walls):

    blocking_box = boxes.index((x + dx, y))
    box_line = set((boxes[blocking_box], boxes[box_connection[blocking_box]]))
    n_boxes = 0

    while n_boxes != len(box_line):
        n_boxes = len(box_line)

        added_boxes = set()
        for box in box_line:
            if (box[0] + dx, box[1]) in boxes:
                blocking_box = boxes.index((box[0] + dx, box[1]))
                added_boxes.add(boxes[blocking_box])
                added_boxes.add(boxes[box_connection[blocking_box]])

        box_line |= added_boxes

    for box in box_line:
        if (box[0] + dx, box[1]) in walls:
            return x, y, boxes

    x = x + dx
    box_indices = [boxes.index(box) for box in box_line]
    for j, (box_x, box_y) in zip(box_indices, box_line):
        boxes[j] = (box_x + dx, box_y)

    return x, y, boxes


def solve(input_file, use_expanded_map=False):

    robot, walls, boxes, movements = load(input_file)
    directions = [DIRECTIONS[move] for move in movements]

    if use_expanded_map:
        robot, walls, boxes, box_connection = expand_map(robot, walls, boxes)
    else:
        box_connection = {i: i for i in range(len(boxes))}

    x, y = robot
    for dx, dy in directions:

        if (x + dx, y + dy) not in walls and (x + dx, y + dy) not in boxes:
            x, y = x + dx, y + dy

        elif (x + dx, y + dy) in boxes and dy != 0:
            x, y, boxes = move_horizontal(x, y, dy, boxes, walls)

        elif (x + dx, y + dy) in boxes and dy == 0:
            x, y, boxes = move_vertical(x, y, dx, boxes, box_connection, walls)

    if use_expanded_map:
        boxes = boxes[::2]

    return sum([100 * x + y for x, y in boxes])


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", solve(args.input_file, False))
    print("Part 2 solution:", solve(args.input_file, True))


if __name__ == "__main__":
    main()
