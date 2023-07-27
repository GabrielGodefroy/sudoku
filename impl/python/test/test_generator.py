from sudoku.validity import check_solution
from sudoku.generator import FullGridGenerator, PartialGridGenerator

from sudoku.solver.backtracking import solve

import numpy as np


def test_full_grid_generator_constructor():
    generator = FullGridGenerator(3)
    assert generator._base == 3
    assert generator._side == 9


def test_full_grid_generator_pattern():

    generator = FullGridGenerator(3)
    assert generator._pattern(0, 0) == 0
    assert generator._pattern(0, 1) == 1
    assert generator._pattern(0, 2) == 2
    assert generator._pattern(0, 3) == 3
    assert generator._pattern(0, 8) == 8
    # ...
    assert generator._pattern(1, 0) == 3
    assert generator._pattern(1, 1) == 4
    assert generator._pattern(1, 2) == 5
    assert generator._pattern(1, 5) == 8
    assert generator._pattern(1, 6) == 0
    assert generator._pattern(1, 8) == 2
    # ...
    assert generator._pattern(2, 0) == 6
    assert generator._pattern(2, 2) == 8
    assert generator._pattern(2, 3) == 0
    # ...
    assert generator._pattern(8, 0) == 8
    assert generator._pattern(8, 8) == 7


def test_full_grid_generator_pattern2():

    generator = FullGridGenerator(3)
    lst = [1, 5, 8]
    assert set(generator._shuffle(lst)) == set(lst)


def test_full_grid_generator_generate_from_seed():

    generator = FullGridGenerator(3)
    res = generator.generate(101)
    assert (
        res
        == np.array(
            [
                [3, 9, 7, 8, 6, 5, 1, 4, 2],
                [5, 6, 8, 1, 4, 2, 7, 9, 3],
                [2, 4, 1, 7, 9, 3, 8, 6, 5],
                [7, 2, 9, 6, 3, 8, 4, 5, 1],
                [1, 5, 4, 9, 2, 7, 6, 3, 8],
                [8, 3, 6, 4, 5, 1, 9, 2, 7],
                [6, 7, 3, 5, 8, 4, 2, 1, 9],
                [4, 8, 5, 2, 1, 9, 3, 7, 6],
                [9, 1, 2, 3, 7, 6, 5, 8, 4],
            ]
        )
    ).all()
    assert check_solution(res)


def test_full_grid_generator_generate_several_solution():

    generator = FullGridGenerator(3)
    for seed in range(10):
        res = generator.generate(seed)
        assert check_solution(res)


def test_partial_grid_generator():

    full_grid_generator = FullGridGenerator(3)

    partial_grid_generator = PartialGridGenerator(full_grid_generator, None)
    grid = partial_grid_generator.generate()

    print(f"{grid=}")

    solution = solve(grid)
    assert check_solution(solution)
    # assert grid_match_clues(solution, clues)
