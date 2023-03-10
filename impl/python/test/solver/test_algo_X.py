from sudoku.solver.algo_X import invert_coverage, get_X, get_Y, solve
import pytest
import numpy as np
from sudoku.validity import check_solution, grid_match_clues


def test_invert_coverage_full():
    X = {1, 2, 3, 4, 5, 6, 7}
    Y = {
        "A": [1, 4, 7],
        "B": [1, 4],
        "C": [4, 5, 7],
        "D": [3, 5, 6],
        "E": [2, 3, 6, 7],
        "F": [2, 7],
    }
    result = invert_coverage(X, Y)
    assert result == {
        1: {"A", "B"},
        2: {"E", "F"},
        3: {"E", "D"},
        4: {"A", "B", "C"},
        5: {"D", "C"},
        6: {"E", "D"},
        7: {"E", "A", "F", "C"},
    }


def test_invert_coverage_missing_in_X():
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
        invert_coverage(X, Y)


def test_invert_coverage_missing_in_Y():
    X = {1, 2, 3, 4, 5}
    Y = {"A": [1, 3, 5], "B": [1, 4]}
    result = invert_coverage(X, Y)
    assert result == {1: {"B", "A"}, 2: set(), 3: {"A"}, 4: {"B"}, 5: {"A"}}


def test_invert_coverage_empty_X():
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
        invert_coverage(X, Y)


def test_invert_coverage_empty_Y():
    X = {1, 2, 3, 4, 5, 6, 7}
    Y = {}
    result = invert_coverage(X, Y)
    assert result == {
        1: set(),
        2: set(),
        3: set(),
        4: set(),
        5: set(),
        6: set(),
        7: set(),
    }


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


def test_get_X_1():
    assert get_X(1) == [("rc", (0, 0)), ("rn", (0, 1)), ("cn", (0, 1)), ("bn", (0, 1))]


def test_get_Y_1():
    assert get_Y(1) == {
        (0, 0, 1): [("rc", (0, 0)), ("rn", (0, 1)), ("cn", (0, 1)), ("bn", (0, 1))]
    }


def test_get_X_2():
    assert get_X(2) == [
        # Position constraints for the 16 cells
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
        # row constraints for the 16 cells
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
        # columns constraints for 16 cells
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
        # block constraints for the 16 cells
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


def test_get_Y_2():
    assert get_Y(2) == {
        # list of constraints for the upper left elements (coord 0,0) for with value 1
        (0, 0, 1): [("rc", (0, 0)), ("rn", (0, 1)), ("cn", (0, 1)), ("bn", (0, 1))],
        # list of constraints for the upper left elements (coord 0,0) for with value 2
        (0, 0, 2): [("rc", (0, 0)), ("rn", (0, 2)), ("cn", (0, 2)), ("bn", (0, 2))],
        (0, 0, 3): [("rc", (0, 0)), ("rn", (0, 3)), ("cn", (0, 3)), ("bn", (0, 3))],
        (0, 0, 4): [("rc", (0, 0)), ("rn", (0, 4)), ("cn", (0, 4)), ("bn", (0, 4))],
        # list of constraints for second element (coord 0,1) for with value 1
        (0, 1, 1): [("rc", (0, 1)), ("rn", (0, 1)), ("cn", (1, 1)), ("bn", (0, 1))],
        (0, 1, 2): [("rc", (0, 1)), ("rn", (0, 2)), ("cn", (1, 2)), ("bn", (0, 2))],
        (0, 1, 3): [("rc", (0, 1)), ("rn", (0, 3)), ("cn", (1, 3)), ("bn", (0, 3))],
        (0, 1, 4): [("rc", (0, 1)), ("rn", (0, 4)), ("cn", (1, 4)), ("bn", (0, 4))],
        (0, 2, 1): [("rc", (0, 2)), ("rn", (0, 1)), ("cn", (2, 1)), ("bn", (1, 1))],
        (0, 2, 2): [("rc", (0, 2)), ("rn", (0, 2)), ("cn", (2, 2)), ("bn", (1, 2))],
        (0, 2, 3): [("rc", (0, 2)), ("rn", (0, 3)), ("cn", (2, 3)), ("bn", (1, 3))],
        (0, 2, 4): [("rc", (0, 2)), ("rn", (0, 4)), ("cn", (2, 4)), ("bn", (1, 4))],
        (0, 3, 1): [("rc", (0, 3)), ("rn", (0, 1)), ("cn", (3, 1)), ("bn", (1, 1))],
        (0, 3, 2): [("rc", (0, 3)), ("rn", (0, 2)), ("cn", (3, 2)), ("bn", (1, 2))],
        (0, 3, 3): [("rc", (0, 3)), ("rn", (0, 3)), ("cn", (3, 3)), ("bn", (1, 3))],
        (0, 3, 4): [("rc", (0, 3)), ("rn", (0, 4)), ("cn", (3, 4)), ("bn", (1, 4))],
        (1, 0, 1): [("rc", (1, 0)), ("rn", (1, 1)), ("cn", (0, 1)), ("bn", (0, 1))],
        (1, 0, 2): [("rc", (1, 0)), ("rn", (1, 2)), ("cn", (0, 2)), ("bn", (0, 2))],
        (1, 0, 3): [("rc", (1, 0)), ("rn", (1, 3)), ("cn", (0, 3)), ("bn", (0, 3))],
        (1, 0, 4): [("rc", (1, 0)), ("rn", (1, 4)), ("cn", (0, 4)), ("bn", (0, 4))],
        (1, 1, 1): [("rc", (1, 1)), ("rn", (1, 1)), ("cn", (1, 1)), ("bn", (0, 1))],
        (1, 1, 2): [("rc", (1, 1)), ("rn", (1, 2)), ("cn", (1, 2)), ("bn", (0, 2))],
        (1, 1, 3): [("rc", (1, 1)), ("rn", (1, 3)), ("cn", (1, 3)), ("bn", (0, 3))],
        (1, 1, 4): [("rc", (1, 1)), ("rn", (1, 4)), ("cn", (1, 4)), ("bn", (0, 4))],
        (1, 2, 1): [("rc", (1, 2)), ("rn", (1, 1)), ("cn", (2, 1)), ("bn", (1, 1))],
        (1, 2, 2): [("rc", (1, 2)), ("rn", (1, 2)), ("cn", (2, 2)), ("bn", (1, 2))],
        (1, 2, 3): [("rc", (1, 2)), ("rn", (1, 3)), ("cn", (2, 3)), ("bn", (1, 3))],
        (1, 2, 4): [("rc", (1, 2)), ("rn", (1, 4)), ("cn", (2, 4)), ("bn", (1, 4))],
        (1, 3, 1): [("rc", (1, 3)), ("rn", (1, 1)), ("cn", (3, 1)), ("bn", (1, 1))],
        (1, 3, 2): [("rc", (1, 3)), ("rn", (1, 2)), ("cn", (3, 2)), ("bn", (1, 2))],
        (1, 3, 3): [("rc", (1, 3)), ("rn", (1, 3)), ("cn", (3, 3)), ("bn", (1, 3))],
        (1, 3, 4): [("rc", (1, 3)), ("rn", (1, 4)), ("cn", (3, 4)), ("bn", (1, 4))],
        (2, 0, 1): [("rc", (2, 0)), ("rn", (2, 1)), ("cn", (0, 1)), ("bn", (2, 1))],
        (2, 0, 2): [("rc", (2, 0)), ("rn", (2, 2)), ("cn", (0, 2)), ("bn", (2, 2))],
        (2, 0, 3): [("rc", (2, 0)), ("rn", (2, 3)), ("cn", (0, 3)), ("bn", (2, 3))],
        (2, 0, 4): [("rc", (2, 0)), ("rn", (2, 4)), ("cn", (0, 4)), ("bn", (2, 4))],
        (2, 1, 1): [("rc", (2, 1)), ("rn", (2, 1)), ("cn", (1, 1)), ("bn", (2, 1))],
        (2, 1, 2): [("rc", (2, 1)), ("rn", (2, 2)), ("cn", (1, 2)), ("bn", (2, 2))],
        (2, 1, 3): [("rc", (2, 1)), ("rn", (2, 3)), ("cn", (1, 3)), ("bn", (2, 3))],
        (2, 1, 4): [("rc", (2, 1)), ("rn", (2, 4)), ("cn", (1, 4)), ("bn", (2, 4))],
        (2, 2, 1): [("rc", (2, 2)), ("rn", (2, 1)), ("cn", (2, 1)), ("bn", (3, 1))],
        (2, 2, 2): [("rc", (2, 2)), ("rn", (2, 2)), ("cn", (2, 2)), ("bn", (3, 2))],
        (2, 2, 3): [("rc", (2, 2)), ("rn", (2, 3)), ("cn", (2, 3)), ("bn", (3, 3))],
        (2, 2, 4): [("rc", (2, 2)), ("rn", (2, 4)), ("cn", (2, 4)), ("bn", (3, 4))],
        (2, 3, 1): [("rc", (2, 3)), ("rn", (2, 1)), ("cn", (3, 1)), ("bn", (3, 1))],
        (2, 3, 2): [("rc", (2, 3)), ("rn", (2, 2)), ("cn", (3, 2)), ("bn", (3, 2))],
        (2, 3, 3): [("rc", (2, 3)), ("rn", (2, 3)), ("cn", (3, 3)), ("bn", (3, 3))],
        (2, 3, 4): [("rc", (2, 3)), ("rn", (2, 4)), ("cn", (3, 4)), ("bn", (3, 4))],
        (3, 0, 1): [("rc", (3, 0)), ("rn", (3, 1)), ("cn", (0, 1)), ("bn", (2, 1))],
        (3, 0, 2): [("rc", (3, 0)), ("rn", (3, 2)), ("cn", (0, 2)), ("bn", (2, 2))],
        (3, 0, 3): [("rc", (3, 0)), ("rn", (3, 3)), ("cn", (0, 3)), ("bn", (2, 3))],
        (3, 0, 4): [("rc", (3, 0)), ("rn", (3, 4)), ("cn", (0, 4)), ("bn", (2, 4))],
        (3, 1, 1): [("rc", (3, 1)), ("rn", (3, 1)), ("cn", (1, 1)), ("bn", (2, 1))],
        (3, 1, 2): [("rc", (3, 1)), ("rn", (3, 2)), ("cn", (1, 2)), ("bn", (2, 2))],
        (3, 1, 3): [("rc", (3, 1)), ("rn", (3, 3)), ("cn", (1, 3)), ("bn", (2, 3))],
        (3, 1, 4): [("rc", (3, 1)), ("rn", (3, 4)), ("cn", (1, 4)), ("bn", (2, 4))],
        (3, 2, 1): [("rc", (3, 2)), ("rn", (3, 1)), ("cn", (2, 1)), ("bn", (3, 1))],
        (3, 2, 2): [("rc", (3, 2)), ("rn", (3, 2)), ("cn", (2, 2)), ("bn", (3, 2))],
        (3, 2, 3): [("rc", (3, 2)), ("rn", (3, 3)), ("cn", (2, 3)), ("bn", (3, 3))],
        (3, 2, 4): [("rc", (3, 2)), ("rn", (3, 4)), ("cn", (2, 4)), ("bn", (3, 4))],
        (3, 3, 1): [("rc", (3, 3)), ("rn", (3, 1)), ("cn", (3, 1)), ("bn", (3, 1))],
        (3, 3, 2): [("rc", (3, 3)), ("rn", (3, 2)), ("cn", (3, 2)), ("bn", (3, 2))],
        (3, 3, 3): [("rc", (3, 3)), ("rn", (3, 3)), ("cn", (3, 3)), ("bn", (3, 3))],
        (3, 3, 4): [("rc", (3, 3)), ("rn", (3, 4)), ("cn", (3, 4)), ("bn", (3, 4))],
    }


def test_solve_X_on_empty_9x9_grid():
    clues = np.ndarray(shape=(9, 9), dtype=int)
    clues.fill(0)
    solution = solve(clues)
    assert check_solution(solution)
    assert grid_match_clues(solution, clues)


def test_solve_X_on_empty_4x4_grid():
    clues = np.ndarray(shape=(4, 4), dtype=int)
    clues.fill(0)
    solution = solve(clues)
    assert solution is not None
    # TODO assert check_solution(solution)
    # TODO assert grid_match_clues(solution, clues)


def test_solve_X_on_impossible_4x4_grid():
    clues = np.ndarray(shape=(4, 4), dtype=int)
    clues.fill(0)
    clues[0, 0] = 1
    clues[0, 1] = 1
    with pytest.raises(KeyError):  # TODO wrap with other exception
        solve(clues)


def test_solve_X_on_impossible_9x9_grid():
    clues = np.ndarray(shape=(9, 9), dtype=int)
    clues.fill(0)
    clues[0, 0] = 1
    clues[0, 1] = 1
    with pytest.raises(KeyError):  # TODO wrap with other exception
        solve(clues)


@pytest.mark.slow
def test_solve_on_easy_grid():
    clues = np.array(
        [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
        ]
    )
    solution = solve(clues)
    assert check_solution(solution)
    assert grid_match_clues(solution, clues)
