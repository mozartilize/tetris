import pytest

from tetris.grid import Point, TetrisGrid, clear_rows


locked_points0 = {
    Point(0, 11): (1, 1, 1),
    Point(1, 11): (1, 1, 1),
    Point(2, 11): (1, 1, 1),
    Point(3, 11): (1, 1, 1),
    Point(4, 11): (1, 1, 1),
    Point(0, 10): (1, 1, 1),
    # Point(1, 10): (1, 1, 1),
    Point(2, 10): (1, 1, 1),
    Point(3, 10): (1, 1, 1),
    Point(4, 10): (1, 1, 1),
    Point(0, 9): (1, 1, 1),
    Point(1, 9): (1, 1, 1),
    Point(2, 9): (1, 1, 1),
    Point(3, 9): (1, 1, 1),
    Point(4, 9): (1, 1, 1),
}

locked_points1 = {
    Point(0, 11): (1, 1, 1),
    Point(1, 11): (1, 1, 1),
    Point(2, 11): (1, 1, 1),
    Point(3, 11): (1, 1, 1),
    Point(4, 11): (1, 1, 1),
    Point(0, 10): (1, 1, 1),
    # Point(1, 10): (1, 1, 1),
    Point(2, 10): (1, 1, 1),
    Point(3, 10): (1, 1, 1),
    Point(4, 10): (1, 1, 1),
    Point(0, 9): (1, 1, 1),
    Point(1, 9): (1, 1, 1),
    Point(2, 9): (1, 1, 1),
    Point(3, 9): (1, 1, 1),
    Point(4, 9): (1, 1, 1),
    Point(0, 8): (1, 1, 1),
    Point(1, 8): (1, 1, 1),
    Point(2, 8): (1, 1, 1),
    Point(3, 8): (1, 1, 1),
    Point(4, 8): (1, 1, 1),
    Point(0, 7): (1, 1, 1),
}

locked_points2 = {
    Point(0, 11): (1, 1, 1),
    Point(1, 11): (1, 1, 1),
    Point(2, 11): (1, 1, 1),
    Point(3, 11): (1, 1, 1),
    Point(4, 11): (1, 1, 1),
    Point(0, 10): (1, 1, 1),
    Point(1, 10): (1, 1, 1),
    Point(2, 10): (1, 1, 1),
    Point(3, 10): (1, 1, 1),
    Point(4, 10): (1, 1, 1),
    Point(0, 9): (1, 1, 1),
    Point(1, 9): (1, 1, 1),
    Point(2, 9): (1, 1, 1),
    Point(3, 9): (1, 1, 1),
    Point(4, 9): (1, 1, 1),
    Point(0, 8): (1, 1, 1),
    Point(1, 8): (1, 1, 1),
    # Point(2, 8): (1, 1, 1),
    # Point(3, 8): (1, 1, 1),
    Point(4, 8): (1, 1, 1),
    Point(0, 7): (1, 1, 1),
}


@pytest.mark.parametrize('locked,grid,points', [
    [
        locked_points0, TetrisGrid(5, 12, locked_points0), [
            Point(0, 11),
            Point(2, 11),
            Point(3, 11),
            Point(4, 11),
        ]
    ],
    [
        locked_points1, TetrisGrid(5, 12, locked_points1), [
            Point(0, 11),
            Point(2, 11),
            Point(3, 11),
            Point(4, 11),
            Point(0, 10),
        ]
    ],
    [
        locked_points2, TetrisGrid(5, 12, locked_points2), [
            Point(0, 11),
            Point(1, 11),
            Point(4, 11),
            Point(0, 10),
        ]
    ],
])
def test_grid(locked, grid, points):
    clear_rows(grid, locked)
    print(locked)
    for p in points:
        assert p in locked
    assert len(points) == len(locked)
