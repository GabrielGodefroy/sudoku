import numpy as np
from itertools import product


class SudokuGrid:
    """ Implements a 9x9 Sudoku grid  
    
    Internally the grid is stored as a np.array
    Values can be added/remove thanks to the [] operator
    
    Checking the validity of an insertion (self.valid) requires to 
    run through every value in the sudoku. This slows down 
    the backtracking quite a lot
    """

    def __init__(self, clues):
        self.clues = clues
        self.grid = self.clues.copy()
        # np.zeros((9, 9), dtype=int)
        # for x, y in product(range(9), range(9)):
        #    if self.clues[x, y] != 0:
        #        self[x, y] = self.clues[x, y]

    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        """ Set the value in the solved grid and update self.on_line, self.on_colm, self.on_reg """
        if value == 0:
            assert self.grid[index] != 0
        else:
            assert self.grid[index] == 0

        self.grid[index] = value

    def box(self, x, y):
        """ Get the index of the box (from 0 to 9) """
        return x // 3 * 3 + y // 3

    def valid(self, x, y, value):
        """ Check whether n can possibly be added in the
            partially solved sudoku grid (at x,y position)

        Args:
            x (int): line index
            y (int): column index
            value (int): number of try at x and y coordinate

        Returns:
            bool: True if n is not already in a line, column, or box
        
        Note:
            This is a critical function, and should more efficient 
        """
        r = self.box(x, y)
        for x_other, y_other in product(range(9), range(9)):
            r_other = self.box(x_other, y_other)
            if (x == x_other or y == y_other or r == r_other) and value == self[
                x_other, y_other
            ]:
                return False
        return True

    def to_np(self):
        """ Convert back the sudoku into a np.array """
        result = np.zeros((9, 9), dtype=int)
        for x, y in product(range(9), range(9)):
            result[x, y] = self[x, y]
        return result
