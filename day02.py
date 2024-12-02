def load(input_file):

    with open(input_file, 'r') as infile:
        return [list(map(int, row.split(' '))) for row in infile]


def is_safe(level):
    
    diffs = [level[i+1] - level[i] for i in range(len(level) - 1)]
    return all([-3 <= diff <= -1 for diff in diffs]) or all([1 <= diff <= 3 for diff in diffs])

def is_safe_with_dampener(level):

    if is_safe(level):
        return True
    
    for i in range(len(level)):
        if is_safe(level[:i] + level[i+1:]):
            return True
        
    return False


def solve(input_file, eval_func):
    
    return sum([eval_func(level) for level in load(input_file)])


def main():
    
    assert solve(input_file='inputs/day02/test.txt', eval_func=is_safe) == 2
    print('Part 1 solution:', solve(input_file='inputs/day02/input.txt', eval_func=is_safe))

    assert solve(input_file='inputs/day02/test.txt', eval_func=is_safe_with_dampener) == 4
    print('Part 2 solution:', solve(input_file='inputs/day02/input.txt', eval_func=is_safe_with_dampener))

if __name__ == '__main__':
    main()