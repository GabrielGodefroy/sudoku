from sudoku.solver.backtracking import solve as backtracking_solve
from sudoku.solver.algo_X import solve as algoX_solve

import numpy as np

solver_implementation = {"backtracking": backtracking_solve, "algoX": algoX_solve}


def get_avail_solver_names():
    return list(solver_implementation.keys())


class SolverKeyError(Exception):
    """Exception raised when asking for a missing unimplemented solver."""

    def __init__(self, asked_name: str):
        super().__init__(f"Unknown solver implementation: {asked_name}")


def solve(grid: np.ndarray, solver_name: str = "algoX") -> np.ndarray:

    try:
        impl = solver_implementation[solver_name]
    except KeyError:
        raise SolverKeyError(solver_name)

    return impl(grid)
