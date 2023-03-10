from itertools import product
from sudoku.grid import get_box_number
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


def get_X(dim: int):
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


def get_Y(dim: int) -> dict:
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


def invert_coverage(X: set, Y: dict) -> dict:
    """
    Given a set X, and a dictionary Y key -> list[value] where each value belongs to X:

    Return a dictionnary mapping each element of X to the key link by Y

    >>> result = invert_coverage( X = {1, 2, 3, 4, 5} , Y = { "A": [1, 3, 5], "B": [1, 4] })
    {1: {'B', 'A'}, 2: set(), 3: {'A'}, 4: {'B'}, 5: {'A'}}

    https://en.wikipedia.org/wiki/Exact_cover
    """
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X


def select(X, Y, cell_characteristics: tuple):
    """
    cell_characteristics: contains the row_index, the cell_index and the cell_value
    """
    cols = []
    for j in Y[cell_characteristics]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols


def deselect(X, Y, cell_characteristics: tuple, cols):
    for j in reversed(Y[cell_characteristics]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)


def call_select_on_initial_values(grid: np.ndarray, X, Y):
    """Call the select method for each cell of grid where the value is not 0"""
    for (row_index, col_index), cell_value in np.ndenumerate(grid):
        if cell_value == 0:
            continue
        select(X, Y, (row_index, col_index, cell_value))


def apply_solution(solutions, grid: np.ndarray) -> np.ndarray:
    for (row, col, value) in solutions:
        grid[row, col] = value
    return grid


def solve(grid: np.ndarray) -> np.ndarray:
    N, _N = grid.shape
    assert N == _N
    R = int(N**0.5)

    X = get_X(R)
    Y = get_Y(R)

    X = invert_coverage(X, Y)

    call_select_on_initial_values(grid, X, Y)

    for solutions in solve_with_constraints(X, Y, []):
        return apply_solution(
            solutions, grid
        )  # return to stop on first found grid (yield could also be used)


def solve_with_constraints(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve_with_constraints(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()
