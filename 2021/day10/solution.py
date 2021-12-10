#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
import typing as t
from argparse import ArgumentParser
from collections import deque
from dataclasses import dataclass


verbose = False


MATCH = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}
SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

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
    score = 0
    for line in read_file(filename):
        score += score_invalid(line)
    print("Score:", score)


def score_invalid(line):
    stack = deque()
    for character in line:
        if character in MATCH.keys():
            if stack.pop() != MATCH[character]:
                if verbose:
                    print("INVALID:", line)
                return SCORES[character]
        else:
            stack.append(character)
    if verbose:
        print("VALID:", line)
    return 0


def part2(filename):
    pass


def read_file(filename) -> t.Iterator[str]:
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


if __name__ == "__main__":
    sys.exit(main())
