import numpy as np


"""
@file multisolver.py
@brief Module for returning not only 1 solution but all valid solutions
"""


def shortSudokuSolve(board: np.ndarray) -> [np.ndarray]:
    """Refactor into a class"""
    size = len(board)
    block = int(size**0.5)
    board = [n for row in board for n in row]

    def getList(p, size, block):
        return [
            p // size,
            size + p % size,
            2 * size + p % size // block + p // size // block * block,
        ]

    span = {
        (n, p): {(g, n) for g in (n > 0) * getList(p, size, block)}
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
