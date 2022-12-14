#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./day##.py [--verbose]

"""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from typing import NamedTuple

import pytest

verbose = False


class ValidPacket(Exception):
    pass


class InvalidPacket(Exception):
    pass


class Packets(NamedTuple):
    left: list
    right: list

    @property
    def valid(self) -> bool:
        try:
            validate(self.left, self.right)
        except ValidPacket:
            return True
        except InvalidPacket:
            return False
        return True


@dataclass
class Packet:
    values: list

    def __lt__(self, other: Packet):
        try:
            validate(self.values, other.values)
        except ValidPacket:
            return True
        except InvalidPacket:
            return False
        return True


def validate(left: list, right: list):
    if verbose:
        print(f"Comparing {left} to {right}")
    for left_value, right_value in zip_longest(left, right):
        match (left_value, right_value):
            case (int() as a, int() as b):
                if a < b:
                    raise ValidPacket()
                if a > b:
                    raise InvalidPacket()
            case (list() as a, list() as b):
                validate(a, b)
            case (_, None):
                # right side cannot run out first
                raise InvalidPacket(f"Right ran list out first: {left}, {right}")
            case (None, _):
                raise ValidPacket()
            case (int() as a, list() as b):
                validate([a], b)
            case (list() as a, int() as b):
                validate(a, [b])
    return


def main():
    parser = ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")

    global verbose
    args = parser.parse_args()
    if args.verbose:
        verbose = True

    # the download script doesn't add the leading 0
    day = int(Path(__file__).stem.removeprefix("day"))
    input_file = Path(f"day{day}-input.txt")
    print(f"Reading input from {input_file}")
    puzzle_input = input_file.read_text()
    print(f"Day #{day} part 1 solution:", part1(puzzle_input))
    print(f"Day #{day} part 2 solution:", part2(puzzle_input))


def part1(puzzle_input: str):
    valid_packets = []
    for index, packet in enumerate(parse_input(puzzle_input), start=1):
        if packet.valid:
            valid_packets.append(index)

    if verbose:
        print("Valid indexes:", valid_packets)

    return sum(valid_packets)


def part2(puzzle_input: str):
    data = puzzle_input.splitlines()
    packets = [Packet(json.loads(line)) for line in data if line]
    if verbose:
        print("# of packets loaded:", len(packets))

    markers = [Packet([[2]]), Packet([[6]])]
    packets += markers

    packets = sorted(packets)
    first_packet_index = packets.index(markers[0]) + 1
    second_packet_index = packets.index(markers[1]) + 1

    return first_packet_index * second_packet_index


def parse_input(puzzle_input: str) -> Iterator[Packets]:
    data = puzzle_input.splitlines()
    for idx in range(0, len(data), 3):
        yield Packets(json.loads(data[idx]), json.loads(data[idx + 1]))


SAMPLE = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".lstrip(
    "\n"
)


@pytest.mark.parametrize(
    ("func", "input_", "expected"),
    [
        (part1, SAMPLE, 13),
        (part2, SAMPLE, 140),
    ],
)
def test_solutions(func, input_, expected):
    global verbose
    verbose = True
    assert func(input_) == expected


if __name__ == "__main__":
    sys.exit(main())
