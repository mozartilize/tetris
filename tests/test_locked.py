import pytest

from tetris.grid import squeeze_locked, Point

locked0 = {
    Point(0, 10): 'x',
    Point(1, 10): 'x',
    # Point(2, 10): 'x',
    Point(3, 10): 'x',
    Point(4, 10): 'x',
    Point(0, 7): 'x',
}
locked1 = {
    Point(0, 11): 'x',
    Point(1, 11): 'x',
    Point(2, 11): 'x',
    Point(3, 11): 'x',
    Point(4, 11): 'x',
    Point(0, 10): 'x',
}
locked2 = {
    Point(0, 11): 'x',
    Point(1, 11): 'x',
    Point(2, 11): 'x',
    Point(0, 10): 'x',
}


@pytest.mark.parametrize('locked,points', [
    [
        locked0, [
            Point(0, 11),
            Point(1, 11),
            Point(3, 11),
            Point(4, 11),
            Point(0, 10),
        ]
    ],
    [locked1, locked1.keys()],
    [locked2, locked2.keys()],
])
def test_squeeze_locked(locked, points):
    new_locked = dict(locked)
    squeeze_locked(new_locked, 12)
    for p in points:
        assert p in new_locked
        assert p in new_locked
        assert p in new_locked
        assert p in new_locked
        assert p in new_locked
