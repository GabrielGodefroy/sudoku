import numpy as np


def check_line(sudoku: np.ndarray, line_index: int) -> bool:
    values = sorted([v for v in sudoku[line_index]])
    return values == [i for i in range(1, 10)]


def check_column(sudoku: np.ndarray, column_index: int) -> bool:
    values = sorted([v for v in sudoku[:, column_index]])
    return values == [i for i in range(1, 10)]


def check_lines(sudoku: np.ndarray) -> bool:
    for ind in range(9):
        if check_line(sudoku, ind) is False:
            return False
    return True


def check_columns(sudoku: np.ndarray) -> bool:
    for ind in range(9):
        if check_column(sudoku, ind) is False:
            return False
    return True


def check_square(sudoku: np.ndarray, sq_x_ind: int, sq_y_ind: int) -> bool:
    values = sorted(
        [
            sudoku[x][y]
            for x in range(3 * sq_x_ind, 3 * sq_x_ind + 3)
            for y in range(3 * sq_y_ind, 3 * sq_y_ind + 3)
            if sudoku[x][y] != 0
        ]
    )
    return values == [i for i in range(1, 10)]


def check_squares(sudoku: np.ndarray) -> bool:
    for x in range(3):
        for y in range(3):
            if check_square(sudoku, x, y) is False:
                return False
    return True


def grid_match_clues(solution: np.ndarray, clues: np.ndarray) -> bool:
    if solution.shape != clues.shape:
        return False

    return bool(np.logical_or(clues == 0, solution == clues).all())


def check_solution(grid: np.ndarray) -> bool:
    for functor in [check_squares, check_lines, check_columns]:
        if functor(grid) is False:
            return False
    return True
