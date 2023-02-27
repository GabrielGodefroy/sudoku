from sudoku.solver.backtracking import solve
from sudoku.validity import check_solution, grid_match_clues

import numpy as np
import pytest


def test_solve_on_empty_grid_1():
    clues = np.ndarray(shape=(9, 9))
    clues.fill(0)
    solution = solve(clues)
    assert check_solution(solution)
    assert grid_match_clues(solution, clues)


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


@pytest.mark.slow
def test_fail_to_solve_as_no_solution_should_return_none():
    clues = np.array(
        [
            [5, 3, 2, 0, 7, 0, 0, 0, 0],
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
    assert solution is None


# TODO too slow
# def test_solve_on_easy_grid_2():
#     clues = np.array(
#         [
#            [9, 0, 0, 1, 0, 0, 0, 0, 5],
#            [0, 0, 5, 0, 9, 0, 2, 0, 1],
#            [8, 0, 0, 0, 4, 0, 0, 0, 0],
#            [0, 0, 0, 0, 8, 0, 0, 0, 0],
#            [0, 0, 0, 7, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 2, 6, 0, 0, 9],
#            [2, 0, 0, 3, 0, 0, 0, 0, 6],
#            [0, 0, 0, 2, 0, 0, 9, 0, 0],
#            [0, 0, 1, 9, 0, 4, 5, 7, 0],
#         ]
#     )
#     solution = solve(clues)
#     assert check_solution(solution)
#     assert grid_match_clues(solution, clues)
