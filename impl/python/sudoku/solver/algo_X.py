from itertools import product
from sudoku.grid import get_box_number
import numpy as np

"""
Algorithm X modified from https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

Also inspired from https://github.com/ShivanKaul/Sudoku-DLX
"""


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
        box = get_box_number(row, col, dim)
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


def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols


def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)


def call_select_on_initial_values(grid: np.ndarray, X, Y):
    for row_index, row in enumerate(grid):
        for col_index, cur_value in enumerate(row):
            if cur_value != 0:
                select(X, Y, (row_index, col_index, cur_value))


def solve(grid: np.ndarray) -> np.ndarray:
    N, _N = grid.shape
    assert N == _N
    R = int(N**0.5)

    X = get_X(R)
    Y = get_Y(R)

    X = invert_coverage(X, Y)

    call_select_on_initial_values(grid, X, Y)

    for solution in solve_with_constraints(X, Y, []):
        for (r, c, n) in solution:
            grid[r, c] = n
        return grid


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
