import pytest
import numpy as np


def test_check_type_invalid():
    from sudoku.loader import check_type

    assert check_type(None) is False


def test_check_type_valid():
    from sudoku.loader import check_type

    assert check_type(np.ndarray(shape=(9, 9))) is True


def test_check_shape_valid():
    from sudoku.loader import check_shape

    assert check_shape(np.ndarray(shape=(9, 9))) is True


def test_check_shape_invalid():
    from sudoku.loader import check_shape

    assert check_shape(np.ndarray(shape=(8, 9))) is False
    assert check_shape(np.ndarray(shape=(9, 8))) is False
    assert check_shape(np.ndarray(shape=(8, 8))) is False


def test_check_range_value_invalid():
    from sudoku.loader import check_range_value

    grid = np.ndarray(shape=(3, 3))
    grid.fill(-1)
    assert check_range_value(grid) is False
    grid.fill(10)
    assert check_range_value(grid) is False


def test_check_range_value_valid():
    from sudoku.loader import check_range_value

    grid = np.ndarray(shape=(3, 3))
    grid.fill(0)
    assert check_range_value(grid) is True
    grid.fill(9)
    assert check_range_value(grid) is True


def test_check_line():
    from sudoku.loader import check_line, check_lines

    grid = np.ndarray(shape=(9, 9))
    grid.fill(0)
    grid[0][0] = 1
    grid[0][1] = 1
    grid[0][2] = 1
    assert check_line(grid, 0) is False
    assert check_line(grid, 1) is True
    assert check_line(grid, 2) is True
    assert check_line(grid, 8) is True
    assert check_lines(grid) is False


def test_check_column():
    from sudoku.loader import check_column, check_columns

    grid = np.ndarray(shape=(9, 9))
    grid.fill(0)
    grid[1][0] = 1
    grid[3][0] = 1
    assert check_column(grid, 0) is False
    assert check_column(grid, 1) is True
    assert check_column(grid, 2) is True
    assert check_column(grid, 3) is True
    assert check_columns(grid) is False


def test_check_square():
    from sudoku.loader import check_square, check_squares

    grid = np.ndarray(shape=(9, 9))
    grid.fill(0)
    grid[0][0] = 1
    grid[1][1] = 1
    grid[4][4] = 1
    grid[5][5] = 1
    assert check_square(grid, 0, 0) is False
    assert check_square(grid, 1, 0) is True
    assert check_square(grid, 2, 0) is True
    assert check_square(grid, 0, 1) is True
    assert check_square(grid, 1, 1) is False
    assert check_square(grid, 1, 2) is True
    assert check_square(grid, 0, 2) is True
    assert check_square(grid, 2, 1) is True
    assert check_square(grid, 2, 2) is True
    assert check_squares(grid) is False
