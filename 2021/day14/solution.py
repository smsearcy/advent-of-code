#!/usr/bin/env python3
"""Day 14: Extended Polymerization

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import itertools
import sys
import typing as t
from argparse import ArgumentParser
from collections import Counter
from dataclasses import dataclass

verbose = False


def main():
    parser = ArgumentParser()
    parser.add_argument("part", type=int)
    parser.add_argument("filename")
    parser.add_argument("--verbose", "-v", action="store_true")

    global verbose
    args = parser.parse_args()
    filename = args.filename
    if args.verbose:
        verbose = True

    if args.part == 1:
        part1(filename)
    elif args.part == 2:
        part2(filename)
    else:
        return f"Invalid 'part' specified: {args.part}"


def part1(filename):
    template, rules = read_file(filename)
    print("Starting template:", "".join(char for char in template))
    print("# of rules:", len(rules))

    for _ in range(10):
        for idx, pair in enumerate(itertools.pairwise("".join(template))):
            template.insert(idx * 2 + 1, rules["".join(pair)])

        if verbose:
            print("".join(c for c in template))

    counts = Counter(template).most_common()
    print("Most common:", counts[0])
    print("Least common:", counts[-1])
    print("Final score:", counts[0][1] - counts[-1][1])


def part2(filename):
    pass


def read_file(filename) -> tuple[list[str], dict[str, str]]:
    rules = {}
    with open(filename, "r") as f:
        template = list(f.readline().rstrip())
        for line in f:
            if not line.rstrip():
                continue
            key, value = line.rstrip().split(" -> ")
            rules[key] = value
    return template, rules


if __name__ == "__main__":
    sys.exit(main())
