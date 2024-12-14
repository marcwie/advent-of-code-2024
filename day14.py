import argparse
from collections import Counter

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))


class Robot:

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self, n, width, height):

        for _ in range(n):

            self.x += self.vx
            self.x %= width

            self.y += self.vy
            self.y %= height

            assert 0 <= self.x <= width - 1
            assert 0 <= self.y <= height - 1

    def quadrant(self, width, heigth):
        if self.x < width / 2 - 1 and self.y < heigth / 2 - 1:
            return 1
        if self.x < width / 2 - 1 and self.y > heigth / 2:
            return 2
        if self.x > width / 2 and self.y < heigth / 2 - 1:
            return 3
        if self.x > width / 2 and self.y > heigth / 2:
            return 4

    def position(self):
        return self.x, self.y


class Space:

    def __init__(self, robots, width, height):

        self.robots = robots
        self.width = width
        self.height = height

    def move(self, n=1):

        for robot in self.robots:
            robot.move(n, width=self.width, height=self.height)

    def positions(self):
        return tuple(coord for robot in self.robots for coord in robot.position())

    def create_image(self):

        positions = [robot.position() for robot in self.robots]
        pos_str = ""

        for y in range(self.height):
            line = ["#" if (x, y) in positions else "." for x in range(self.width)]
            pos_str += "".join(line) + "\n"

        return pos_str

    def robots_form_square(self):

        positions = [robot.position() for robot in self.robots]
        for x, y in positions:
            if all((x + i, y + j) in positions for i, j in DIRECTIONS):
                return True
        return False


def load(input_file):
    with open(input_file, "r") as infile:
        data = infile.read().splitlines()

    robots = []
    for line in data:
        position, velocity = line.split(" ")
        x, y = map(int, position[2:].split(","))
        vx, vy = map(int, velocity[2:].split(","))
        robots.append(Robot(x, y, vx, vy))

    return robots


def part1(input_file, width, height):

    robots = load(input_file)
    space = Space(robots, width=width, height=height)
    space.move(100)

    quadrants = Counter()
    for robot in robots:
        quadrants[robot.quadrant(width, height)] += 1

    result = 1
    for key, value in quadrants.items():
        if key is not None:
            result *= value

    return result


def part2(input_file, width, height):

    robots = load(input_file)
    space = Space(robots, width=width, height=height)
    seen = set()
    positions = space.positions()

    elapsed = 0
    while positions not in seen:

        if space.robots_form_square():
            print(f"Potential tree found after {elapsed}s. Check image to confirm.")
            print(space.create_image())

        seen.add(positions)
        space.move()
        positions = space.positions()
        elapsed += 1


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str)
    parser.add_argument("--width", type=int, default=101, required=False)
    parser.add_argument("--height", type=int, default=103, required=False)
    args = parser.parse_args()

    print("Part 1 solution:", part1(args.input_file, args.width, args.height))
    print("Solving part 2...")
    part2(args.input_file, args.width, args.height)


if __name__ == "__main__":
    main()
