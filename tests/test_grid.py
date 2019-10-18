from tetris.tetris import clear_rows
from tetris.grid import Point, TetrisGrid

locked_points = {
    Point(0, 4): (1, 1, 1),
    Point(1, 4): (1, 1, 1),
    Point(2, 4): (1, 1, 1),
    Point(3, 4): (1, 1, 1),
    # Point(0, 3): (1, 1, 1),
    Point(1, 3): (1, 1, 1),
    Point(2, 3): (1, 1, 1),
    Point(3, 3): (1, 1, 1),
    Point(3, 2): (1, 1, 1),
}

grid = TetrisGrid(4, 5, locked_points)


if __name__ == '__main__':
    print(clear_rows(grid, locked_points))
