import numpy as np
from itertools import product
import copy


class SudokuGrid:
    """ Implements a 9x9 Sudoku grid  
    
    Internally the grid is stored as a np.array
    Values can be added/remove thanks to the [] operator
    
    Checking the validity of an insertion (self.valid) requires to 
    run through every value in the sudoku. 
    This slows down the backtracking a lot!
    """
    def __init__(self, clues):
        print("Construct SudokuGrid")
        self.clues = clues
        self.grid = self.clues.copy()


    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        """ Set the value in the solved grid and update self.on_line, self.on_colm, self.on_reg """
        if value == 0:
            assert self.grid[index] != 0
        else:
            assert self.grid[index] == 0

        self.grid[index] = value

    @staticmethod
    def box(x, y):
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
        if self[x, y] != 0:
            return False
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


class SudokuGridEfficient(SudokuGrid):
    """ Checking for validity is o(1)

        The integrity of the data structure is not maintained when backtracking 
        (i.e., call [x,y]=0) 

        The values need to be deep-copied in the stack of recursive calls

        See SolverBacktrackingEfficient
    """
    def __init__(self, clues):
        """ Calls operator [] to copy the clues, so that the possibility 
            data structure is updated """

        # TODO set up a list of neighbors to speed up things
        neighbors = []
        for r in range(9):
            neighbors.append([]) 
            for c in range(9): 
                neighbors[r].append([]) 
                b = SudokuGrid.box(r, c)
                for r2, c2 in product(range(9), range(9)):
                    b2 = SudokuGrid.box(r2, c2)
                    if (r == r2 or c == c2 or b == b2) and ((r,c)!=(r2,c2)):
                        neighbors[r][c].append([r2,c2])
                neighbors[r][c] = np.array(neighbors[r][c])
                assert neighbors[r][c].shape == (20,2)
        SudokuGridEfficient.neighbors = neighbors
        # end of to refactor part
    
        self.clues = clues
        self.np_values = np.array([i+1 for i in range(9)])
        self.possibilities = np.full((9, 9, 9), True, dtype=bool)
        self.nb_possibilities = np.full((9, 9), 9, dtype=int)
        self.remaining = [(x,y) for x,y in product(range(9),range(9))]
        self.grid = np.zeros((9, 9), dtype=int)

        for x, y in product(range(9), range(9)):
            if self.clues[x, y] != 0:
                self[x, y] = self.clues[x, y]
        self.to_solve()



    def to_solve(self):
        self.remaining.sort(key=lambda ind: self.nb_possibilities[ind])
        return self.remaining
        

    def valid(self, x, y, value):
        """ Checking validity is now o(1) """
        assert value > 0
        return self.possibilities[x, y, value - 1]

    def __setitem__(self, index, value):
        """ Set an (unset) value and update the list of possibilities """
        #assert value != 0
        #assert self.grid[index] == 0
        self.remaining.remove(index)
        self.grid[index] = value

        self.possibilities[index].fill(False)
        self.nb_possibilities[index] = 0
        for r, c in SudokuGridEfficient.neighbors[index[0]][index[1]]:
            if self.possibilities[r, c, value - 1]:
                self.possibilities[r, c, value - 1] = False
                self.nb_possibilities[r,c]-=1

    def tmp_setitem(self, index, value):
        self.remaining.remove(index)
        self.grid[index] = value
        for r, c in SudokuGridEfficient.neighbors[index[0]][index[1]]:
            if self.possibilities[r, c, value - 1]:
                self.possibilities[r, c, value - 1] = False
                self.nb_possibilities[r,c]-=1

    def heuristic(self):
        """ Fills all the cells where only one value can be set """
        remain = self.to_solve()
        while len(remain)>0 and np.sum(self.possibilities[remain[0]]) == 1:
            while len(remain)>0 and np.sum(self.possibilities[remain[0]]) == 1:
                value = np.dot(self.possibilities[remain[0]], self.np_values)
                self.tmp_setitem(remain[0],value)
            remain = self.to_solve() 

