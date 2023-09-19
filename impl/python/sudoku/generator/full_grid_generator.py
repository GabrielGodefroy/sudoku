import numpy as np
from random import sample
import random


class FullGridGenerator:
    """
    Generate a complete 3x3 sudoku grid.

    (Modified from https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python)
    """

    def __init__(self, base: int = 3):
        self._base = base
        self._side = self._base**2

    def _pattern(self, row_ind: int, col_ind: int):
        base = self._base
        side = self._side
        return (base * (row_ind % base) + row_ind // base + col_ind) % side

    def _shuffle(self, elements: list):
        """Return the elements of elements in a random order"""
        return sample(elements, len(elements))

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
