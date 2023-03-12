from itertools import product
from sudoku.grid import get_box_number
from sudoku.solver.algo_X_impl.algo_X_impl import (
    select,
    invert_coverage,
    recursive_exact_coverage,
)
import numpy as np

"""
Algorithm X modified from https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

Also inspired from https://github.com/ShivanKaul/Sudoku-DLX
"""


class CellIndex:
    def __init__(self, row_ind: int, col_ind: int):
        self.row_ind = row_ind
        self.col_ind = col_ind


class ValuedCell:
    def __init__(self, row_ind: int, col_ind: int, value: int):
        self.index = CellIndex(row_ind, col_ind)
        self.value = value


def build_list_of_constraints(dim: int):
    N = dim * dim
    """Represent the columns of the sparse matrix constraints"""
    return (
        # position constraint: only 1 number can occupy a cell
        # cell index range from (0,0) to (N-1,N-1)
        [("rc", rc) for rc in product(range(N), range(N))]
        # row constraint: row indices ranges from 0 to N-1,
        #                 number ranges from 0 to N
        + [("rn", rn) for rn in product(range(N), range(1, N + 1))]
        # column constraint
        + [("cn", cn) for cn in product(range(N), range(1, N + 1))]
        # region constraint
        + [("bn", bn) for bn in product(range(N), range(1, N + 1))]
    )


def build_map_of_constraint_per_cell(dim: int) -> dict:
    """Represent the rows of the sparse matrix constraints"""
    N = dim * dim
    Y = dict()
    for row, col, num in product(range(N), range(N), range(1, N + 1)):
        # r: row, c: column, n: number
        # for row and column, indices start at 0
        # number range from 1 to 9
        box = get_box_number(row, col, dim)  # TODO use CellIndex
        Y[(row, col, num)] = [
            ("rc", (row, col)),
            ("rn", (row, num)),
            ("cn", (col, num)),
            ("bn", (box, num)),
        ]
    return Y


def call_select_on_initial_values(
    grid: np.ndarray, candidate_per_constraint, constraint_map_per_cell
):
    """Call the select method for each cell of grid where the value is not 0"""
    for (row_index, col_index), cell_value in np.ndenumerate(grid):
        if cell_value == 0:
            continue
        select(
            candidate_per_constraint,
            constraint_map_per_cell,
            (row_index, col_index, cell_value),
        )


def apply_solution(solutions, grid: np.ndarray) -> np.ndarray:
    for (row, col, value) in solutions:
        grid[row, col] = value
    return grid


def solve(grid: np.ndarray) -> np.ndarray:
    N, _N = grid.shape
    assert N == _N
    R = int(N**0.5)

    list_of_constraints = build_list_of_constraints(R)
    constraint_map_per_cell = build_map_of_constraint_per_cell(R)

    candidate_per_constraint = invert_coverage(
        list_of_constraints, constraint_map_per_cell
    )

    call_select_on_initial_values(
        grid, candidate_per_constraint, constraint_map_per_cell
    )

    for solutions in recursive_exact_coverage(
        candidate_per_constraint, constraint_map_per_cell, []
    ):
        return apply_solution(
            solutions, grid
        )  # return to stop on first found grid (yield could also be used)
