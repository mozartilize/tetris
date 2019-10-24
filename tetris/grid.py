from .helpers import hashing_point


class Point:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y

    def __hash__(self):
        return hashing_point(self.x, self.y)


class TetrisGrid:
    def __init__(self, width, height, locked_points=None):
        self.height = height
        self.width = width

        self.available_points = set()
        self._locked_points = set()
        self._lastest_points = None
        self._init_grid(locked_points or {})

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._grid[index]
        elif isinstance(index, Point):
            return self._grid[index.y][index.x]
        else:
            raise TypeError(
                "%s type of index is not supported" % (type(index))
            )

    def __setitem__(self, point, value):
        if isinstance(point, Point):
            self._grid[point.y][point.x] = value
        else:
            raise TypeError(
                "%s type of point is not supported" % (type(point))
            )

    def _init_grid(self, locked_points):
        self._grid = [None] * self.height
        for y in range(self.height):
            self._grid[y] = [(0, 0, 0)] * self.width
            for x in range(self.width):
                p = Point(x, y)
                color = locked_points.get(p)
                if color is not None:
                    self[p] = color
                    self._locked_points.add(p)
                else:
                    self.available_points.add(p)

    def update(self, input_locked_dict, finnal_lock=False):
        input_locked_points = set(input_locked_dict.keys())
        if finnal_lock:
            self._lastest_points = input_locked_points
        free_points = self._locked_points - input_locked_points
        additional_locked_points = input_locked_points - self._locked_points
        for point in free_points:
            self[point] = (0, 0, 0)
        for point in additional_locked_points:
            self[point] = input_locked_dict[point]
        self.available_points.difference_update(additional_locked_points)
        self.available_points.update(free_points)
        self._locked_points.difference_update(free_points)
        self._locked_points.update(additional_locked_points)

    def check_lost(self):
        return self._lastest_points \
            and any(point.y < 1 for point in self._lastest_points)


class GriddedShape:
    def __init__(self, point, shape):
        self.point = point
        self.shape = shape

    @property
    def positions(self):
        for i, line in enumerate(self.shape.shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    # what are 2 and 4?
                    yield Point(
                        self.point.x + j - 2,
                        self.point.y + i - 4
                    )

    def go_right(self, units):
        self.point.x += units

    def go_left(self, units):
        self.point.x -= units

    def go_down(self, units):
        self.point.y += units

    def go_up(self, units):
        self.point.y -= units

    @property
    def rotation(self):
        return self.shape.rotation

    @property
    def color(self):
        return self.shape.color


def valid_space(shape, grid):
    return not any(
        p not in grid.available_points and p.y > -1 for p in shape.positions
    )


def clear_rows(grid, locked):
    inc = 0
    for y in range(grid.height - 1, -1, -1):
        row = grid[y]
        if (0, 0, 0) not in row:
            inc += 1
            ind = y
            for x in range(grid.width):
                try:
                    del locked[Point(x, y)]
                except KeyError:
                    continue

    if inc > 0:
        for point in sorted(list(locked), key=lambda point: point.y)[::-1]:
            if point.y < ind:
                newpoint = Point(point.x, point.y + inc)
                locked[newpoint] = locked.pop(point)

    return inc
