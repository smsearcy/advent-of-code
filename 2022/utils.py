from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def load(cls, value: str) -> Point:
        return Point(*(int(c) for c in value.split(",")))

    @classmethod
    def line(cls, begin: Point, end: Point) -> list[Point]:
        """Create the list of points that make up a line.

        Only cardinal directions are currently supported!

        """
        if begin == end:
            return [begin]
        if begin.y == end.y:
            if begin.x < end.x:
                delta = 1
            else:
                delta = -1
            return [Point(x, begin.y) for x in range(begin.x, end.x + delta, delta)]
        if begin.x == end.x:
            if begin.y < end.y:
                delta = 1
            else:
                delta = -1
            return [Point(begin.x, y) for y in range(begin.y, end.y + delta, delta)]
        return ValueError("Line must be horizontal or vertical.")


@dataclass
class Grid:
    _values: list[list]  # rows of columns

    @property
    def width(self) -> int:
        return len(self._values[0])

    @property
    def height(self):
        return len(self._values)

    def row(self, row) -> list:
        return self._values[row]

    def column(self, column) -> list:
        return [row[column] for row in self._values]

    def find(self, value) -> Point:
        for point in self:
            if self[point] == value:
                return point

    def find_all(self, value) -> Iterator[Point]:
        for point in self:
            if self[point] == value:
                yield point

    def neighbors(self, point: Point, *, diagonal: bool = False) -> Iterator[Point]:
        """Yield the neighbors to a particular point."""
        for delta in (-1, 1):
            if 0 <= point.x + delta < self.width:
                yield Point(point.x + delta, point.y)
            if 0 <= point.y + delta < self.height:
                yield Point(point.x, point.y + delta)

        if diagonal:
            for delta_x in (-1, 1):
                if point.x + delta_x < 0 or point.x + delta_x >= self.width:
                    continue
                for delta_y in (-1, 1):
                    if point.y + delta_y < 0 or point.y + delta_y >= self.height:
                        continue
                    yield Point(point.x + delta_x, point.y + delta_y)

    def __getitem__(self, item: Point):
        try:
            return self._values[item.y][item.x]
        except IndexError:
            raise IndexError(f"Point not in grid: {item}") from None

    def __iter__(self):
        return (Point(x, y) for y in range(self.height) for x in range(self.width))

    def __str__(self):
        output = ["".join(str(val) for val in row) for row in self._values]
        return "\n".join(output)
