from collections import Counter

def load(input_file):
    """Load input files into two lists of integers."""
    with open(input_file) as infile:
        data = [line.split('   ') for line in infile]
    
    left, right = zip(*data)
    left = list(map(int, left))
    right = list(map(int, right))

    return left, right


def part1(input_file):
    left, right = load(input_file=input_file)
    
    left.sort()
    right.sort()
    diff = [abs(l - r) for l, r  in zip(left, right)]

    return sum(diff)
    

def part2(input_file):

    left, right = load(input_file=input_file)

    left = Counter(left)
    right = Counter(right)

    result = 0
    for number, count in left.items():
        result += number * count * right[number]

    return result
        

def main():

    assert part1(input_file="inputs/day01/test.txt") == 11
    print('Part 1 solution:', part1(input_file='inputs/day01/input.txt'))

    assert part2(input_file="inputs/day01/test.txt") == 31
    print('Part 2 solution:', part2(input_file='inputs/day01/input.txt'))


if __name__ == '__main__':
    main()