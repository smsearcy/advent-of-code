#!/usr/bin/env python3
"""Template for Advent of Code solution in Python.

Usage: ./solution.py 1|2 FILE

"""

from __future__ import annotations

import enum
import sys
from argparse import ArgumentParser

verbose = False


class Shape(enum.IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


WIN_MAP = {
    Shape.ROCK: Shape.SCISSORS,
    Shape.PAPER: Shape.ROCK,
    Shape.SCISSORS: Shape.PAPER,
}

LOSE_MAP = {loser: winner for winner, loser in WIN_MAP.items()}


OPPONENT_MAP = {
    "A": Shape.ROCK,
    "B": Shape.PAPER,
    "C": Shape.SCISSORS,
}


def score(opponent: Shape, me: Shape) -> int:
    if WIN_MAP[me] == opponent:
        # win (6 pts)
        return 6 + int(me)
    if opponent == me:
        # draw (3 pts)
        return 3 + int(me)
    if WIN_MAP[opponent] == me:
        # lose (0 pts)
        return int(me)
    raise ValueError(f"Unhandled scenario: {opponent=}, {me=}")


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
    my_map = {
        "X": Shape.ROCK,
        "Y": Shape.PAPER,
        "Z": Shape.SCISSORS,
    }
    hands = []
    with open(filename, "r") as f:
        for line in f:
            hands.append((OPPONENT_MAP[line[0]], my_map[line[2]]))

    if verbose:
        print(hands)

    total_score = 0
    for opponent, me in hands:
        total_score += score(opponent, me)

    print("Total score:", total_score)


def part2(filename):
    # X = lose, Y = draw, Z = win
    total_score = 0
    with open(filename, "r") as f:
        for line in f:
            opponent = OPPONENT_MAP[line[0]]
            goal = line[2]
            if goal == "X":
                # lose
                me = WIN_MAP[opponent]
            elif goal == "Z":
                # win
                me = LOSE_MAP[opponent]
            else:
                me = opponent
            total_score += score(opponent, me)

    print("Total score:", total_score)


if __name__ == "__main__":
    sys.exit(main())
