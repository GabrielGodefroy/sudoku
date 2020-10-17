import numpy as np
import copy

from sudoku.grid import SudokuGridEfficient

class SudokuGenerator:
    def __init__(self):
        pass

    def generate(self,seed=None):
        if seed is not None and type(seed) == int:
            np.random.seed(seed)
        self.grid = SudokuGridEfficient()
        self.solution = None
        self.do_generate()
        return self.solution

    def do_generate(self):
        if self.solution is not None:
            return
        self.grid.heuristic()
        for index in self.grid.remaining:  
            possible_val = self.grid.possible_values(index)
            np.random.shuffle(possible_val)
            for n in possible_val:
                possibilities, grid, remaining, nb_possibilities = self.grid.possibilities.copy(), self.grid.grid.copy(), self.grid.remaining.copy(), self.grid.nb_possibilities.copy()
                self.grid[index] = n
                self.do_generate()
                self.grid.possibilities, self.grid.grid, self.grid.remaining, self.grid.nb_possibilities = possibilities, grid, remaining, nb_possibilities
            return
        self.solution = self.grid.grid.copy()
