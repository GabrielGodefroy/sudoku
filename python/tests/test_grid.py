import pytest
import numpy as np
from sudoku.grid import SudokuGrid, SudokuGridEfficient
from sudoku.loader import load_from_text_file


data_structures = [SudokuGrid, SudokuGridEfficient]


def test_mytest():
    clues = load_from_text_file("../DATA/easy.txt")
    grid = SudokuGridEfficient(clues)
    grid.heuristic()



@pytest.mark.parametrize("GridStruc", data_structures)
def test_load(GridStruc):
    clues = load_from_text_file("../DATA/easy.txt")
    grid = GridStruc(clues)

    assert grid.valid(0, 0, 1) == False
    assert grid.valid(0, 0, 9) == False

    assert grid.valid(1, 1, 1) == False
    assert grid.valid(1, 1, 3) == True

    assert grid[2, 0] == 8
    assert grid.valid(2, 0, 8) == False
    assert grid.valid(2, 0, 7) == False

    assert grid[0, 2] == 0
    assert grid.valid(0, 2, 9) == False
    assert grid.valid(0, 2, 1) == False
    assert grid.valid(0, 2, 3) == True

    assert grid[2, 2] == 0
    assert grid.valid(2, 2, 9) == False
