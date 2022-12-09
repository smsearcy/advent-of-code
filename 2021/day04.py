"""Advent of Code 2021: Day 4 - 'Giant Squid Bingo'

"""

from __future__ import annotations

import pprint
import sys
from dataclasses import dataclass, field

BOARD_SIZE = 5


def _blank_board():
    return [
        [False] * BOARD_SIZE,
        [False] * BOARD_SIZE,
        [False] * BOARD_SIZE,
        [False] * BOARD_SIZE,
        [False] * BOARD_SIZE,
    ]


@dataclass
class BingoBoard:
    values: list[list[int]]
    selected: list[list[bool]] = field(default_factory=_blank_board)

    def check_number(self, value: int) -> bool:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.values[row][col] != value:
                    continue
                # found a match
                self.selected[row][col] = True
                return True

        return False

    def check_won(self) -> bool:
        for row in range(BOARD_SIZE):
            if all(self.selected[row]):
                print(f"Winning row: {row}")
                return True
        for col in range(BOARD_SIZE):
            if all(r[col] for r in self.selected):
                print(f"Winning column: {col}")
                return True
        return False

    @property
    def unmarked_numbers(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.selected[row][col]:
                    continue
                yield self.values[row][col]

    @property
    def marked_count(self):
        count = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.selected[row][col]:
                    count += 1
        return count

    def __str__(self):
        output = []
        for row in range(len(self.values)):
            output.append(
                " ".join(
                    f"{val:02}{'*' if sel else ' '}"
                    for val, sel in zip(self.values[row], self.selected[row])
                )
            )
        return "\n".join(output)

    def __repr__(self):
        return pprint.pformat(self.values)


def main():
    filename = sys.argv[1]
    action = sys.argv[2]
    numbers, boards = read_file(filename)

    print(numbers)

    if action == "part1":
        board, last_number = part1(numbers, boards)
        print("Last number:", last_number)
        print("Winning Board:")
        print(board)
        print(f"Score: {sum(board.unmarked_numbers) * last_number}")

    elif action == "part2":
        board, last_number = part2(numbers, boards)
        print("Last number:", last_number)
        print("Winning Board:")
        print(board)
        print(f"Score: {sum(board.unmarked_numbers) * last_number}")

    else:
        return "Invalid action"


def read_file(filename) -> tuple[list[int], list[BingoBoard]]:
    with open(filename, "r") as f:
        called_numbers = [int(v) for v in next(f).split(",")]
        boards = []
        while True:
            try:
                next(f)  # consume the empty line
            except StopIteration:
                break
            lines = []
            for i in range(5):
                lines.append([int(v) for v in next(f).split()])
            boards.append(BingoBoard(values=lines))

    return called_numbers, boards


def part1(numbers: list[int], boards: list[BingoBoard]) -> tuple[BingoBoard, int]:
    """Find the winning board."""

    for number in numbers:
        for idx, board in enumerate(boards, start=1):
            if board.check_number(number):
                if board.check_won():
                    print(f"Board #{idx} won")
                    return board, number


def part2(numbers: list[int], boards: list[BingoBoard]) -> tuple[BingoBoard, int]:
    """Find the losing board."""

    winning_boards = [False] * len(boards)
    for number in numbers:
        for idx, board in enumerate(boards):
            if board.check_number(number) and not winning_boards[idx]:
                if board.check_won():
                    print(f"Board #{idx+1} won")
                    winning_boards[idx] = True
                    if all(winning_boards):
                        return board, number


if __name__ == "__main__":
    sys.exit(main())
