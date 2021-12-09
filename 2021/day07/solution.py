#!/usr/bin/env python3
"""Day 7: The Treachery of Whales

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
import typing as t
from argparse import ArgumentParser
from operator import itemgetter
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
    crab_positions = [pos for pos in read_file(filename)]
    print("Starting positions:", crab_positions)
    cost = {}
    for goal in range(min(crab_positions), max(crab_positions) + 1):
        cost[goal] = sum(abs(goal - pos) for pos in crab_positions)

    if verbose:
        print("All costs:", cost)

    print("Most efficient solution:", sorted(cost.items(), key=itemgetter(1))[0])


def part2(filename):
    crab_positions = [pos for pos in read_file(filename)]
    print("Starting positions:", crab_positions)
    cost = {}
    for goal in range(min(crab_positions), max(crab_positions) + 1):
        cost[goal] = sum(abs(goal - pos) * (abs(goal - pos) + 1) / 2  for pos in crab_positions)

    if verbose:
        print("All costs:", cost)

    print("Most efficient solution:", sorted(cost.items(), key=itemgetter(1))[0])


def read_file(filename) -> t.Iterator[int]:
    with open(filename, "r") as f:
        yield from (int(val) for val in f.readline().split(","))


if __name__ == "__main__":
    sys.exit(main())
