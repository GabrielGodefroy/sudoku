import pytest
from sudoku.solver.solver import SolverKeyError, solve, get_avail_solver_names


def test_solver_dispatch():
    with pytest.raises(
        TypeError
    ):  # dispatch works as excepted but implementation fails later
        solve(None, "backtracking")


def test_solver_dispatch_on_unknown_strategy():
    with pytest.raises(SolverKeyError):
        solve(None, "unkown strategy")


def test_get_avail_solver_names():
    assert get_avail_solver_names() == ["backtracking", "algoX"]
