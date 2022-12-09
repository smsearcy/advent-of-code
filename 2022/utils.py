from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


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

    def neighbors(self, point: Point, *, diagonal: bool = False) -> Iterator[Point]:
        """Yield the neighbors to a particular point."""
        for delta in (-1, 1):
            if 0 <= point.x + delta < self._width:
                yield Point(point.x + delta, point.y)
            if 0 <= point.y + delta < self._height:
                yield Point(point.x, point.y + delta)

        if diagonal:
            for delta_x in (-1, 1):
                if point.x + delta_x < 0 or point.x + delta_x >= self._width:
                    continue
                for delta_y in (-1, 1):
                    if point.y + delta_y < 0 or point.y + delta_y >= self._height:
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
