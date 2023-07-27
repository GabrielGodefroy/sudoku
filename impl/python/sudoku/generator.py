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


def shortSudokuSolve(board):
    """Refactor into a class"""
    size = len(board)
    block = int(size**0.5)
    board = [n for row in board for n in row]
    span = {
        (n, p): {
            (g, n)
            for g in (n > 0)
            * [
                p // size,
                size + p % size,
                2 * size + p % size // block + p // size // block * block,
            ]
        }
        for p in range(size * size)
        for n in range(size + 1)
    }
    empties = [i for i, n in enumerate(board) if n == 0]
    used = set().union(*(span[n, p] for p, n in enumerate(board) if n))
    empty = 0
    while empty >= 0 and empty < len(empties):
        pos = empties[empty]
        used -= span[board[pos], pos]
        board[pos] = next(
            (n for n in range(board[pos] + 1, size + 1) if not span[n, pos] & used), 0
        )
        used |= span[board[pos], pos]
        empty += 1 if board[pos] else -1
        if empty == len(empties):
            solution = [board[r : r + size] for r in range(0, size * size, size)]
            yield solution
            empty -= 1


class PartialGridGenerator:
    """Simple implementation"""

    def __init__(self, full_grid_generator, solver):
        self._full_grid_generator = full_grid_generator
        self._solver = solver
        pass

    def generate(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

        solution = self._full_grid_generator.generate(seed)

        print(f"{solution=}")

        board = solution.copy()
        board.flat[
            np.random.choice(np.arange(board.size), int(20 / 100 * 81), replace=False)
        ] = 0

        while True:
            solved = [
                *islice(shortSudokuSolve(board.tolist()), 2)
            ]  # todo, remove need for tolist
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
