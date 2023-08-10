from sudoku.multisolver.multisolver import multisolve
from sudoku.validity import check_solution

import numpy as np

from itertools import islice


def test_multisolver_from_empty_grid():
    # given
    size = 9
    nb_grids = 5
    initial_empty_grids = np.array([[0 for i in range(size)] for j in range(size)])
    # when
    solutions = [*islice(multisolve(initial_empty_grids), nb_grids)]
    # then
    for solution in solutions:
        assert type(solution) is np.ndarray
        assert check_solution(solution)

    for i in range(len(solutions)):
        for j in range(i):
            assert (
                solutions[i] != solutions[j]
            ).any()  # TODO there should be a better way of making sur of uniqueness
