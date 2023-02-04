import numpy as np


def test_check_line():
    from sudoku.validity import check_line, check_lines

    grid = np.ndarray(shape=(9, 9))
    grid.fill(0)
    grid[0] = [i for i in range(1, 10)]
    grid[1] = [i if i != 1 else 0 for i in range(1, 10)]
    grid[2] = [i if i != 1 else 2 for i in range(1, 10)]
    assert check_line(grid, 0) is True
    assert check_line(grid, 1) is False
    assert check_line(grid, 2) is False
    assert check_lines(grid) is False


def test_check_column():
    from sudoku.validity import check_column, check_columns

    grid = np.ndarray(shape=(9, 9))
    grid.fill(0)
    grid[:, 0] = [i for i in range(1, 10)]
    grid[:, 1] = [i if i != 1 else 0 for i in range(1, 10)]
    grid[:, 2] = [i if i != 1 else 2 for i in range(1, 10)]
    assert check_column(grid, 0) is True
    assert check_column(grid, 1) is False
    assert check_column(grid, 2) is False
    assert check_columns(grid) is False


def test_check_square():
    from sudoku.validity import check_square, check_squares

    grid = np.ndarray(shape=(9, 9))
    grid.fill(0)
    grid[0][0] = 1
    grid[0][1] = 2
    grid[0][2] = 3
    grid[1][0] = 4
    grid[1][1] = 5
    grid[1][2] = 6
    grid[2][0] = 7
    grid[2][1] = 8
    grid[2][2] = 9
    assert check_square(grid, 0, 0) is True
    assert check_square(grid, 1, 0) is False
    assert check_squares(grid) is False
    


def test_valid_grid():
    from sudoku.validity import check_solution

    grid = np.array(
        [
            [9, 4, 3, 1, 7, 2, 8, 6, 5],
            [7, 6, 5, 8, 9, 3, 2, 4, 1],
            [8, 1, 2, 6, 4, 5, 7, 9, 3],
            [5, 9, 6, 4, 8, 1, 3, 2, 7],
            [1, 2, 8, 7, 3, 9, 6, 5, 4],
            [4, 3, 7, 5, 2, 6, 1, 8, 9],
            [2, 7, 9, 3, 5, 8, 4, 1, 6],
            [6, 5, 4, 2, 1, 7, 9, 3, 8],
            [3, 8, 1, 9, 6, 4, 5, 7, 2],
        ]
    )
    assert check_solution(grid)

def test_invalid_grid():
    from sudoku.validity import check_solution

    grid = np.array(
        [
            [4, 4, 3, 1, 7, 2, 8, 6, 5],
            [7, 6, 5, 8, 9, 3, 2, 4, 1],
            [8, 1, 2, 6, 4, 5, 7, 9, 3],
            [5, 9, 6, 4, 8, 1, 3, 2, 7],
            [1, 2, 8, 7, 3, 9, 6, 5, 4],
            [4, 3, 7, 5, 2, 6, 1, 8, 9],
            [2, 7, 9, 3, 5, 8, 4, 1, 6],
            [6, 5, 4, 2, 1, 7, 9, 3, 8],
            [3, 8, 1, 9, 6, 4, 5, 7, 2],
        ]
    )
    assert check_solution(grid) is False
