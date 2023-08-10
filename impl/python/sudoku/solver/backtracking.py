from sudoku.grid import get_candidate_values
import numpy as np
from itertools import product


def solve(grid: np.ndarray) -> np.ndarray:
    """
    TODO inspired from https://www.youtube.com/watch?v=G_UYXzGuqvM
    """

    solution = None

    def _solve():
        nonlocal solution  # TODO dirty solution - write a class instead?
        if solution is not None:
            return solution

        for i, j in product(range(9), range(9)):
            if grid[i, j] == 0:
                for n in get_candidate_values(i, j, grid):
                    grid[i, j] = n
                    _solve()
                    grid[i, j] = 0
                return
        solution = np.array(grid)

    _solve()

    return solution
