#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./day##.py [-v]

"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import pytest

verbose = False


@dataclass
class Trees:
    # this is a list of rows
    rows: list[list[int]]

    @cached_property
    def size(self) -> int:
        return len(self.rows)

    def is_visible(self, row: int, column: int) -> bool:
        if row == 0 or column == 0 or row == self.size - 1 or column == self.size - 1:
            # outer edge
            return True

        tree_height = self.rows[row][column]
        # check row
        for c in range(0, column):
            if self.rows[row][c] >= tree_height:
                break
        else:
            return True
        for c in range(column + 1, self.size):
            if self.rows[row][c] >= tree_height:
                break
        else:
            return True
        # check column
        for r in range(0, row):
            if self.rows[r][column] >= tree_height:
                break
        else:
            return True
        for r in range(row + 1, self.size):
            if self.rows[r][column] >= tree_height:
                break
        else:
            return True

        return False

    def scenic_score(self, row: int, column: int) -> int:
        up = self._look_up(row, column)
        left = self._look_left(row, column)
        down = self._look_down(row, column)
        right = self._look_right(row, column)
        score = up * down * left * right
        return score

    def _look_up(self, row: int, column: int) -> int:
        score = 0
        tree_height = self.rows[row][column]
        for r in range(row - 1, -1, -1):
            score += 1
            if self.rows[r][column] >= tree_height:
                break
        return score

    def _look_down(self, row: int, column: int) -> int:
        score = 0
        tree_height = self.rows[row][column]
        for r in range(row + 1, self.size, 1):
            score += 1
            if self.rows[r][column] >= tree_height:
                break
        return score

    def _look_left(self, row: int, column: int) -> int:
        score = 0
        tree_height = self.rows[row][column]
        for c in range(column - 1, -1, -1):
            score += 1
            if self.rows[row][c] >= tree_height:
                break
        return score

    def _look_right(self, row: int, column: int) -> int:
        score = 0
        tree_height = self.rows[row][column]
        for c in range(column + 1, self.size, 1):
            score += 1
            if self.rows[row][c] >= tree_height:
                break
        return score


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
    trees = parse_input(puzzle_input)
    visible_count = 0
    for row in range(0, trees.size):
        for col in range(0, trees.size):
            if trees.is_visible(row, col):
                visible_count += 1
    return visible_count


def part2(puzzle_input: str):
    trees = parse_input(puzzle_input)
    scores = []
    for row in range(0, trees.size):
        for col in range(0, trees.size):
            scores.append(trees.scenic_score(row, col))
    return sorted(scores)[-1]


def parse_input(puzzle_input: str) -> Trees:
    rows = []
    for line in puzzle_input.splitlines():
        rows.append([int(t) for t in line])
    trees = Trees(rows)
    if verbose:
        print(trees)
    return trees


SAMPLE = """
30373
25512
65332
33549
35390
""".lstrip(
    "\n"
)


@pytest.mark.parametrize(
    ("func", "input_", "expected"),
    [
        (part1, SAMPLE, 21),
        (part2, SAMPLE, 8),
    ],
)
def test_solutions(func, input_, expected):
    global verbose
    verbose = True
    assert func(input_) == expected


if __name__ == "__main__":
    sys.exit(main())
