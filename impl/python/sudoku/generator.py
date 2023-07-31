import numpy as np
from random import sample
import random
from itertools import islice

"""Modified from https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python"""


class FullGridGenerator:
    def __init__(self, base: int = 3):
        self._base = base
        self._side = self._base**2

    def _pattern(self, row_ind: int, col_ind: int):
        base = self._base
        side = self._side
        return (base * (row_ind % base) + row_ind // base + col_ind) % side

    def _shuffle(self, lst: list):
        """Return the elements of l in a random order"""
        return sample(lst, len(lst))

    def generate(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

        base = self._base

        rangeBase = range(base)
        rows = [
            g * base + r
            for g in self._shuffle(rangeBase)
            for r in self._shuffle(rangeBase)
        ]
        cols = [
            g * base + c
            for g in self._shuffle(rangeBase)
            for c in self._shuffle(rangeBase)
        ]
        rand_1_10 = self._shuffle(range(1, base * base + 1))

        return np.array([[rand_1_10[self._pattern(r, c)] for c in cols] for r in rows])


class PartialGridGenerator:
    """Simple implementation"""

    def __init__(self, full_grid_generator, solver):
        self._full_grid_generator = full_grid_generator
        self._solver = solver

    def generate(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        solution = self._full_grid_generator.generate(seed)

        board = solution.copy()
        board.flat[
            np.random.choice(np.arange(board.size), int(50 / 100 * 81), replace=False)
        ] = 0

        assert type(board) == np.ndarray

        while True:
            solved = [*islice(self._solver(board), 2)]  # todo, remove need for tolist
            if len(solved) == 1:
                break
            diffPos = [
                (r, c)
                for r in range(9)
                for c in range(9)
                if solved[0][r][c] != solved[1][r][c]
            ]
            r, c = random.choice(diffPos)
            board[r, c] = solution[r, c]

        return board
