from sudoku.solver.algo_X import exact_cover
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
