import numpy as np


def load_from_text_file(filepath, check_validity=True):
    """Load a 9x9 np.ndarray as a text file
    
    Args:
        filepath (str): path to the text file
    """
    result = np.loadtxt(filepath, dtype=int)
    if check_validity:
        raise_error_if_input_not_valid(result)
    return result


def raise_error_if_input_not_valid(sudoku):
    """ Check that a grid is a 9x9 sudoku respects the sudoku constraints

    Args:
        grid (np.ndarray): a 9x9 array

    Note:
        This does not check a valid solution exists, only that
        no conflict can be find in a line, column or subsquare
    """

    if type(sudoku) != np.ndarray:
        raise TypeError("Sudoku should be given as a numpy.ndarray")

    if sudoku.shape != (9, 9):
        raise ValueError("Sudoku should be 9x9")

    if (sudoku < 0).any() or (sudoku > 9).any():
        raise ValueError("Value should be between 0 and 9")

    def raise_error_if_subset_not_valid(subset, text):
        """ Check that a subset (line, column or subsquare) 
        does not contains any duplicated values (except 0). """

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
            raise_error_if_subset_not_valid(subset, f"square ({x_init},{y_init})")

