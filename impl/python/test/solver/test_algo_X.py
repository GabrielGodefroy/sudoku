from sudoku.solver.algo_X import exact_cover, get_X, get_Y
import pytest


def test_exact_cover_full():
    X = {1, 2, 3, 4, 5, 6, 7}
    Y = {
        "A": [1, 4, 7],
        "B": [1, 4],
        "C": [4, 5, 7],
        "D": [3, 5, 6],
        "E": [2, 3, 6, 7],
        "F": [2, 7],
    }
    result = exact_cover(X, Y)
    assert result == {
        1: {"A", "B"},
        2: {"E", "F"},
        3: {"E", "D"},
        4: {"A", "B", "C"},
        5: {"D", "C"},
        6: {"E", "D"},
        7: {"E", "A", "F", "C"},
    }


def test_exact_cover_missing_in_X():
    X = {1, 2, 3, 4}
    Y = {
        "A": [1, 4, 7],
        "B": [1, 4],
        "C": [4, 5, 7],
        "D": [3, 5, 6],
        "E": [2, 3, 6, 7],
        "F": [2, 7],
    }
    with pytest.raises(KeyError):
        exact_cover(X, Y)


def test_exact_cover_missing_in_Y():
    X = {1, 2, 3, 4, 5}
    Y = {"A": [1, 3, 5], "B": [1, 4]}
    result = exact_cover(X, Y)
    assert result == {1: {"B", "A"}, 2: set(), 3: {"A"}, 4: {"B"}, 5: {"A"}}


def test_exact_cover_empty_X():
    X = set()
    Y = {
        "A": [1, 4, 7],
        "B": [1, 4],
        "C": [4, 5, 7],
        "D": [3, 5, 6],
        "E": [2, 3, 6, 7],
        "F": [2, 7],
    }
    with pytest.raises(KeyError):
        exact_cover(X, Y)


def test_exact_cover_empty_Y():
    X = {1, 2, 3, 4, 5, 6, 7}
    Y = {}
    result = exact_cover(X, Y)
    assert result == {
        1: set(),
        2: set(),
        3: set(),
        4: set(),
        5: set(),
        6: set(),
        7: set(),
    }


def test_get_X_1():
    assert get_X(1) == [("rc", (0, 0)), ("rn", (0, 1)), ("cn", (0, 1)), ("bn", (0, 1))]


def test_get_X_2():
    assert get_X(2) == [
        ("rc", (0, 0)),
        ("rc", (0, 1)),
        ("rc", (0, 2)),
        ("rc", (0, 3)),
        ("rc", (1, 0)),
        ("rc", (1, 1)),
        ("rc", (1, 2)),
        ("rc", (1, 3)),
        ("rc", (2, 0)),
        ("rc", (2, 1)),
        ("rc", (2, 2)),
        ("rc", (2, 3)),
        ("rc", (3, 0)),
        ("rc", (3, 1)),
        ("rc", (3, 2)),
        ("rc", (3, 3)),
        ("rn", (0, 1)),
        ("rn", (0, 2)),
        ("rn", (0, 3)),
        ("rn", (0, 4)),
        ("rn", (1, 1)),
        ("rn", (1, 2)),
        ("rn", (1, 3)),
        ("rn", (1, 4)),
        ("rn", (2, 1)),
        ("rn", (2, 2)),
        ("rn", (2, 3)),
        ("rn", (2, 4)),
        ("rn", (3, 1)),
        ("rn", (3, 2)),
        ("rn", (3, 3)),
        ("rn", (3, 4)),
        ("cn", (0, 1)),
        ("cn", (0, 2)),
        ("cn", (0, 3)),
        ("cn", (0, 4)),
        ("cn", (1, 1)),
        ("cn", (1, 2)),
        ("cn", (1, 3)),
        ("cn", (1, 4)),
        ("cn", (2, 1)),
        ("cn", (2, 2)),
        ("cn", (2, 3)),
        ("cn", (2, 4)),
        ("cn", (3, 1)),
        ("cn", (3, 2)),
        ("cn", (3, 3)),
        ("cn", (3, 4)),
        ("bn", (0, 1)),
        ("bn", (0, 2)),
        ("bn", (0, 3)),
        ("bn", (0, 4)),
        ("bn", (1, 1)),
        ("bn", (1, 2)),
        ("bn", (1, 3)),
        ("bn", (1, 4)),
        ("bn", (2, 1)),
        ("bn", (2, 2)),
        ("bn", (2, 3)),
        ("bn", (2, 4)),
        ("bn", (3, 1)),
        ("bn", (3, 2)),
        ("bn", (3, 3)),
        ("bn", (3, 4)),
    ]


def test_get_size_XY():
    # https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/sudoku.paper.html#Sudoku
    # https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/presentationboard.pdf (slide 13 for size 9)
    assert len(get_X(1)) == 1 * 2 * 2
    assert len(get_Y(1)) == 1**3
    assert len(get_X(2)) == 4 * 4 * 4
    assert len(get_Y(2)) == 4**3
    # X are columns
    assert len(get_X(3)) == 4 * 9 * 9 == 324
    # Y are rows
    assert len(get_Y(3)) == 9**3 == 729


def test_get_Y_1():
    assert get_Y(1) == {
        (0, 0, 1): [("rc", (0, 0)), ("rn", (0, 1)), ("cn", (0, 1)), ("bn", (0, 1))]
    }
