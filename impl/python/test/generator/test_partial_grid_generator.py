from sudoku.validity import check_solution, grid_match_clues
from sudoku.generator.full_grid_generator import FullGridGenerator
from sudoku.generator.partial_grid_generator import PartialGridGenerator
from sudoku.multisolver.multisolver import multisolve

from sudoku.solver.backtracking import solve

import numpy as np

def test_partial_grid_generator():
    # given
    size = 3
    seed = 101  # seed used for the full grid generator
    full_grid_generator = FullGridGenerator(size)
    multisolver = multisolve

    # when
    partial_grid_generator = PartialGridGenerator(full_grid_generator, multisolver)
    grid = partial_grid_generator.generate(seed)

    # then
    solution = solve(grid)
    full_grid_solution = full_grid_generator.generate(seed)
    assert check_solution(solution)
    assert grid_match_clues(solution, full_grid_solution)


def test_partial_grid_generator_several():
    grids = []
    for seed in [0, 1, 101, 105]:  # seed used for the full grid generator
        # given
        size = 3
        full_grid_generator = FullGridGenerator(size)
        multisolver = multisolve

        # when
        partial_grid_generator = PartialGridGenerator(full_grid_generator, multisolver)
        grid = partial_grid_generator.generate(seed)
        grids.append(grid)

        # then
        solution = solve(grid)
        full_grid_solution = full_grid_generator.generate(seed)
        assert check_solution(solution)
        assert grid_match_clues(solution, full_grid_solution)

    for i in range(len(grids)):
        for j in range(i):
            assert (
                grids[i] != grids[j]
            ).any()  # TODO there should be a better way of making sur of uniqueness


def test_partial_grid_generator_check_reproducibility():
    grids = []
    for _ in range(5):  # seed used for the full grid generator
        # given
        seed = 101
        size = 3
        full_grid_generator = FullGridGenerator(size)
        multisolver = multisolve

        # when
        partial_grid_generator = PartialGridGenerator(full_grid_generator, multisolver)
        grid = partial_grid_generator.generate(seed)
        grids.append(grid)

        # then
        solution = solve(grid)
        full_grid_solution = full_grid_generator.generate(seed)
        assert check_solution(solution)
        assert grid_match_clues(solution, full_grid_solution)

    for i in range(len(grids)):
        assert (
            grids[0] == grids[i]
        ).all()  # TODO there should be a better way to check all equals
