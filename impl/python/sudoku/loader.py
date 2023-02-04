import numpy as np


def load_from_text_file(filepath: str, check_validity=True):
    result = np.loadtxt(filepath, dtype=int)
    if check_validity:
        raise_error_if_input_not_valid(result)
    return result


def load_from_string(text: str, check_validity=True):
    result = np.fromstring(text, dtype=int)
    if check_validity:
        raise_error_if_input_not_valid(result)
    return result


def check_type(sudoku: np.ndarray) -> bool:
    return type(sudoku) == np.ndarray


def check_shape(sudoku: np.ndarray) -> bool:
    return sudoku.shape == (9, 9)


def check_range_value(sudoku: np.ndarray) -> bool:
    return bool((sudoku >= 0).any() and (sudoku <= 9).any())


def check_line(sudoku: np.ndarray, line_index: int) -> bool:
    values = sorted([v for v in sudoku[line_index] if v != 0])
    return len(values) == len(set(values))


def check_column(sudoku: np.ndarray, column_index: int) -> bool:
    values = sorted([v for v in sudoku[:, column_index] if v != 0])
    return len(values) == len(set(values))


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
    return len(values) == len(set(values))


def check_squares(sudoku: np.ndarray) -> bool:
    for x in range(3):
        for y in range(3):
            if check_square(sudoku, x, y) is False:
                return False
    return True


def raise_error_if_input_not_valid(sudoku: np.ndarray) -> None:
    if check_type(sudoku) is False:
        raise TypeError("Sudoku should be given as a numpy.ndarray")

    if check_shape(sudoku) is False:
        raise ValueError("Shape on the sudoku grid should be 9x9")

    if check_range_value(sudoku) is False:
        raise ValueError("Value should be between 0 and 9")

    for functor in [check_squares, check_lines, check_columns]:
        if functor(sudoku) is False:
            raise ValueError("Duplicated value in input")
