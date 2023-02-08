from sudoku.solver.backtracking import solve as backtracking_solve

import numpy as np

solver_implementation = {
    "backtracking": backtracking_solve,
    # TODO
}


class SolverKeyError(Exception):
    """Exception raised when asking for a missing unimplemented solver."""

    def __init__(self, asked_name: str):
        super().__init__(f"Unknown solver implementation: {asked_name}")


def solve(grid: np.ndarray, solver_name: str = "backtracking"):

    try:
        impl = solver_implementation[solver_name]
    except KeyError:
        raise SolverKeyError(solver_name)

    return impl(grid)
