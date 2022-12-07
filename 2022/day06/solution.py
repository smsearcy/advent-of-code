#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path

import pytest

verbose = False


def main():
    parser = ArgumentParser()
    parser.add_argument("part", type=int)
    parser.add_argument("filename")
    parser.add_argument("--verbose", "-v", action="store_true")

    global verbose
    args = parser.parse_args()
    filename = Path(args.filename)
    input_data = filename.read_text()
    if args.verbose:
        verbose = True

    if args.part == 1:
        print(part1(input_data))
    elif args.part == 2:
        print(part2(input_data))
    else:
        return f"Invalid 'part' specified: {args.part}"


def part1(input_data):
    for i in range(4, len(input_data) + 1, 1):
        if len(set(input_data[i - 4:i])) < 4:
            continue
        return i


def part2(input_data):
    for i in range(14, len(input_data) + 1, 1):
        if len(set(input_data[i - 14:i])) < 14:
            continue
        return i


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5),
        ('nppdvjthqldpwncqszvftbrmjlhg', 6),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11),
    ]
)
def test_part1(data, expected):
    assert part1(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
        ('bvwbjplbgvbhsrlpgdmjqwftvncz', 23),
        ('nppdvjthqldpwncqszvftbrmjlhg', 23),
        ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29),
        ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26),
    ]
)
def test_part2(data, expected):
    assert part2(data) == expected


if __name__ == "__main__":
    sys.exit(main())
