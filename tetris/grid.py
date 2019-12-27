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
        self._latest_points = None
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

    def update_to_new_locked_points(self, input_locked_dict):
        self._latest_points = self._update_to_locked_points(input_locked_dict)

    def update_to_locked_points(self, input_locked_dict):
        self._update_to_locked_points(input_locked_dict)

    def _update_to_locked_points(self, input_locked_dict):
        input_locked_points = set(input_locked_dict.keys())
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
        return input_locked_points

    def check_lost(self):
        return self._latest_points \
            and any(point.y < 1 for point in self._latest_points)


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
    ind = {}
    pre_y = None
    mark_y = None
    for y in range(grid.height - 1, -1, -1):
        if (0, 0, 0) not in grid[y]:
            if pre_y and pre_y == y + 1:
                ind[mark_y] += 1
            else:
                mark_y = y
                ind[mark_y] = 1
            pre_y = y
            for x in range(grid.width):
                try:
                    del locked[Point(x, y)]
                except KeyError:
                    continue

    if sum(ind.values()) > 0:
        for point in sorted(list(locked), key=lambda point: point.y)[::-1]:
            steps = sum(map(
                lambda x: x[1],
                filter(lambda x: x[0] > point.y, ind.items())
            ))
            if steps != 0:
                newpoint = Point(point.x, point.y + steps)
                locked[newpoint] = locked.pop(point)
        # if locked:
        #     squeeze_locked(locked, grid.height)
    return sum(ind.values())


def squeeze_locked(locked, grid_height):
    ys = set(map(lambda p: p.y, locked.keys()))
    try:
        yys = set(range(min(ys), grid_height))
        max_blank_y = max(yys - ys)
    except ValueError:
        return
    max_y = max(ys)
    new_locked_y = set()
    while True:
        for point in [point for point in locked.keys() if point.y == max_y]:
            newpoint = Point(point.x, max_blank_y)
            locked[newpoint] = locked.pop(point)
        new_locked_y.add(max_blank_y)
        ys = set(map(lambda p: p.y, locked.keys())) - new_locked_y
        try:
            yys = set(range(min(ys), grid_height)) - new_locked_y
        except ValueError:
            break
        max_blank_y = max(yys - ys)
        max_y = max(ys)
