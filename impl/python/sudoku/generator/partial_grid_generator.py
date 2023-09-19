import numpy as np
import random
from itertools import islice


class PartialGridGenerator:
    """
    Generate a simple 3x3 sudoku grid that has only one solution.

    (Modified from https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python)
    """

    def __init__(self, full_grid_generator, solver, nb_clues=40):
        self._full_grid_generator = full_grid_generator
        self._solver = solver
        self._nb_clues = nb_clues

        assert (self._nb_clues > 0) and (self._nb_clues <= 9 * 9)

    def generate(self, seed: int = None):
        if seed is not None:
            # TODO see if there is a better practice
            # (maybe dependency injection for number generator)
            random.seed(seed)
            np.random.seed(seed)

        solution = self._full_grid_generator.generate(seed)
        board = self._generate_sparse_grid(solution)

        while True:
            solved = [*islice(self._solver(board), 2)]
            if len(solved) == 1:
                break
            indices_of_different_cells = [
                (row_ind, col_ind)
                for row_ind in range(9)
                for col_ind in range(9)
                if solved[0][row_ind][col_ind] != solved[1][row_ind][col_ind]
            ]
            row_ind, col_ind = random.choice(indices_of_different_cells)
            board[row_ind, col_ind] = solution[row_ind, col_ind]

        return board

    def _generate_sparse_grid(self, initial_solution) -> np.ndarray:
        board = initial_solution.copy()
        board.flat[
            np.random.choice(np.arange(board.size), self._nb_clues, replace=False)
        ] = 0
        assert board.shape == (9, 9)
        assert type(board) == np.ndarray
        return board
