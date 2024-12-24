import argparse
from itertools import combinations


def load(input_file):

    with open(input_file, "r") as infile:
        return [x.split("-") for x in infile.read().splitlines()]


def neighbors(edges):

    nbs = {}
    for x0, x1 in edges:
        if x0 not in nbs.keys():
            nbs[x0] = set()
        nbs[x0].add(x1)

        if x1 not in nbs.keys():
            nbs[x1] = set()
        nbs[x1].add(x0)

    return nbs


def bronkerbosch(R, P, X, nbs):

    if not P and not X:
        return [R]

    cliques = []
    for vertex in list(P):
        cliques += bronkerbosch(R | {vertex}, P & nbs[vertex], X & nbs[vertex], nbs)
        P.remove(vertex)
        X.add(vertex)

    return cliques


def part1(input_file):

    edges = load(input_file)
    nbs = neighbors(edges)

    groups = []

    for source, targets in nbs.items():
        for x0, x1 in combinations(targets, 2):
            if [x0, x1] in edges or [x1, x0] in edges:
                groups.append([source, x0, x1])

    groups = [g for g in groups if "t" in [g[0][0], g[1][0], g[2][0]]]
    return len(groups) // 3


def part2(input_file):

    edges = load(input_file)
    nbs = neighbors(edges)

    cliques = bronkerbosch(set(), set(nbs.keys()), set(), nbs)

    largest_clique = sorted(cliques, key=len)[-1]
    largest_clique = sorted(list(largest_clique))

    return ",".join(largest_clique)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    args = parser.parse_args()

    print("Part 1 solution:", part1(args.input_file))
    print("Part 2 solution:", part2(args.input_file))


if __name__ == "__main__":
    main()
