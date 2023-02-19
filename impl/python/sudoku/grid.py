import numpy as np


def get_neighboorhood_values(x: int, y: int, sudoku: np.ndarray) -> list[int]:
    return [
        sudoku[_x][_y]
        for _x, _y in get_neighboorhood_indices(x, y)
        if sudoku[_x][_y] != 0
    ]


def get_candidate_values(x: int, y: int, sudoku: np.ndarray) -> list[int]:
    return [i for i in range(1, 10) if i not in get_neighboorhood_values(x, y, sudoku)]


def get_neighboorhood_indices(x: int, y: int) -> set[tuple]:
    if (x < 0) or (x > 8) or (y < 0) or (y > 8):
        raise IndexError("Coordinate indices should be between 0 and 8")

    result = set()

    for _x in range(9):
        result.add((_x, y))

    for _y in range(9):
        result.add((x, _y))

    x_square_ind = x // 3
    y_square_ind = y // 3

    for _x in range(3 * x_square_ind, 3 * (x_square_ind + 1)):
        for _y in range(3 * y_square_ind, 3 * (y_square_ind + 1)):
            result.add((_x, _y))

    result.remove((x, y))
    return sorted(result)
