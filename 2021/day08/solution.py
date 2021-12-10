#!/usr/bin/env python3
"""Day 8: Seven-Segment Search

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import itertools
import sys
import typing as t
from argparse import ArgumentParser
from dataclasses import dataclass

verbose = False


@dataclass
class Digit:
    segments: str

    @property
    def parts(self) -> set[str]:
        return set(self.segments)


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
    outputs = [output for _pattern, output in read_file(filename)]
    print("Outputs:", outputs)
    count = 0
    for output in itertools.chain(*outputs):
        if len(output) in {2, 3, 4, 7}:
            count += 1

    print("Known outputs:", count)


def part2(filename):
    total = 0
    for patterns, outputs in read_file(filename):
        known = {}
        size_five = []
        size_six = []
        for pattern in patterns:
            if len(pattern) == 2:
                known[1] = pattern
            elif len(pattern) == 3:
                known[7] = pattern
            elif len(pattern) == 4:
                known[4] = pattern
            elif len(pattern) == 7:
                known[8] = pattern
            elif len(pattern) == 5:
                size_five.append(pattern)
            elif len(pattern) == 6:
                size_six.append(pattern)

        # 9 will completely intersect with 4
        for idx in range(len(size_six)):
            if len(set(known[4]).intersection(size_six[idx])) == 4:
                known[9] = size_six.pop(idx)
                break

        # 7 has 3 intersections with 0, but only 2 with 6
        if len(set(known[7]).intersection(size_six[0])) == 3:
            known[0] = size_six[0]
            known[6] = size_six[1]
        else:
            known[0] = size_six[1]
            known[6] = size_six[0]

        # then 3 will complete intersect with 7 (once 9 is gone)
        for idx in range(len(size_five)):
            if len(set(known[7]).intersection(size_five[idx])) == 3:
                known[3] = size_five.pop(idx)
                break

        # 5 will completely intersect with 6
        for idx in range(len(size_five)):
            if len(set(known[6]).intersection(size_five[idx])) == 5:
                known[5] = size_five.pop(idx)
                break

        # that leaves 2
        known[2] = size_five.pop()
        values = {_normalize(val): str(key) for key, val in known.items()}

        if verbose:
            print("Key:", values)

        display = "".join(values[_normalize(digit)] for digit in outputs)
        if verbose:
            print(display)
        total += int(display)

    print("Total:", total)


def _normalize(val: str) -> str:
    return "".join(sorted(val))


def read_file(filename) -> t.Iterator[tuple[list[str], list[str]]]:
    with open(filename, "r") as f:
        for line in f:
            patterns, output = line.split(" | ")
            yield patterns.split(), output.split()


if __name__ == "__main__":
    sys.exit(main())
