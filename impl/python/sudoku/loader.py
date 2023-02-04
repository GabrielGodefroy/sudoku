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


def raise_error_if_input_not_valid(sudoku: np.ndarray):
    if check_type(sudoku) is False:
        raise TypeError("Sudoku should be given as a numpy.ndarray")

    if check_shape(sudoku) is False:
        raise ValueError("Shape on the sudoku grid should be 9x9")

    if check_range_value(sudoku) is False:
        raise ValueError("Value should be between 0 and 9")

    def raise_error_if_subset_not_valid(subset, text):
        subset = sorted(subset)

        for ind in range(len(subset) - 1):
            if subset[ind] == subset[ind + 1] and subset[ind] != 0:
                raise ValueError(f"Problem in input grid at {text}")

    for line_ind in range(9):
        subset = sudoku[line_ind]
        raise_error_if_subset_not_valid(subset, f"line {line_ind}")
    for column_ind in range(9):
        subset = sudoku[:, column_ind]
        raise_error_if_subset_not_valid(subset, f"row {column_ind}")
    for x_init in [0, 3, 6]:
        for y_init in [0, 3, 6]:
            subset = sudoku[x_init : x_init + 3, y_init : y_init + 3].flatten()
            err_msg = f"square ({x_init},{y_init})"
            raise_error_if_subset_not_valid(subset, err_msg)
