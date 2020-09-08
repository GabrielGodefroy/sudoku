import numpy as np
from itertools import product

from sudoku.loader import raise_error_if_input_not_valid

# https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
# https://www.youtube.com/watch?v=G_UYXzGuqvM
# https://github.com/JoeKarlsson/python-sudoku-generator-solver/blob/master/sudoku.py


class SudokuGrid:
    """ Implements a Sudoki grid where regions are not necessarily boxes 
    
    Values can be added/remove thanks to the [] operator

    Checking the validity of an insertion (self.valid) is O(1) thanks to the
    self.on_line, self.on_colm and self.on_reg attributes

    self.grid is used for constructing the solution
    """

    def __init__(self, clues):
        self.clues = clues

        self.on_line = np.full((9, 9), False, dtype=bool)
        self.on_colm = np.full((9, 9), False, dtype=bool)
        self.on_squr = np.full((9, 9), False, dtype=bool)

        self.possible_values = np.full((9, 9, 9), True, dtype=bool) #x,y,value

        self.grid = np.zeros((9, 9), dtype=int)
        for x, y in product(range(9), range(9)):
            if self.clues[x, y] != 0:
                self[x, y] = self.clues[x, y]

    def __getitem__(self, index):
        return self.grid[index]

    def __setitem__(self, index, value):
        """ Set the value in the solved grid and update self.on_line, self.on_colm, self.on_reg """
        if value == 0:
            ind = self.grid[index] - 1
            assert self.grid[index] != 0
        else:
            ind = value - 1
            assert self.grid[index] == 0

        x, y = index
        r = x//3 * 3 + y // 3 
        
        self.on_line[x, ind] = value != 0
        self.on_colm[y, ind] = value != 0
        self.on_squr[r, ind] = value != 0
        self.grid[index] = value

        self.possible_values[x,y,:]   = value != 0
        self.possible_values[:,y,ind] = value != 0
        self.possible_values[x,:,ind] = value != 0

        x0 = 0
        y0 = 0 
        self.possible_values[x0:x0+3,y0:y0+3,ind] = value != 0



        

    def valid(self, x, y, value):
        """ Check whether n can possibly be added in the
            partially solved sudoku grid (at x,y position)

        Args:
            x (int): line index
            y (int): column index
            n (int): number of try at x and y coordinate
            grid (np.ndarray): the unsolved sudoku grid

        Returns:
            bool: True if n is not already in a line, column, or subsquare
        
        Note:
            This is a critical function 
        """
        r = (x // 3) * 3 + (y // 3) 
        return not (
            self.on_line[x, value - 1]
            or self.on_colm[y, value - 1]
            or self.on_squr[r, value - 1]
        )

    def nb_clues(self, x, y):
        r = (x // 3) * 3 + (y // 3) 
        return sum(self.on_line[x]) + sum(self.on_colm[y]) + sum(self.on_squr[r - 1])


class SolverBacktracking:
    """ Solves a sudoku puzzle using a backtracking algorithm
	
	Returns 0, 1 or several solution(s). 
	Raises error if input is not valid.
	"""

    def __init__(self, max_solution=1):
        """ Creates the solver object 
		
		Args:
			max_solution: the maximum of solution to find
		"""
        self.max_solution = max_solution

    def solve(self, grid):
        raise_error_if_input_not_valid(grid)
        self.raise_error_if_max_solution_not_valid()

        self.grid = grid
        self._init_possibility()

        # starting by the values that have more clues tend to speed up the process
        indices_to_search = [
            (x, y) for x, y in product(range(9), range(9)) if self.grid[x, y] == 0
        ]
        self.order = sorted(
            indices_to_search,
            key=lambda ind: sum(self.on_line[ind[0]])
            + sum(self.on_colm[ind[1]])
            + sum(self.on_subs[(ind[0] // 3) * 3 + (ind[1] // 3)]),
            reverse=True,
        )

        self.solutions = []

        self.cur_ind = 0
        self._do_solve()

        return self.solutions

    def _init_possibility(self):
        """ Create 3 matrix storing the values that can has not been assigned
        to a line, a column or a box """

        self.on_line = np.ndarray((9, 9), dtype=bool)
        self.on_line.fill(False)
        self.on_colm = self.on_line.copy()
        self.on_subs = self.on_line.copy()

        for line_ind in range(9):
            for e in self.grid[line_ind]:
                if e > 0:
                    self.on_line[line_ind][e - 1] = True
        for col_ind in range(9):
            for e in self.grid[:, col_ind]:
                if e > 0:
                    self.on_colm[col_ind][e - 1] = True
        for x_ in range(3):
            for y_ in range(3):
                sq_ind = x_ * 3 + y_
                for e in self.grid[x_ * 3 : x_ * 3 + 3, y_ * 3 : y_ * 3 + 3].flatten():
                    if e > 0:
                        self.on_subs[sq_ind][e - 1] = True

    def _do_solve(self):

        if self._enough_solution_found():
            return

        for x, y in self.order[
            self.cur_ind :
        ]:  # itertools.product(range(9),range(9)): #
            if self.grid[x, y] == 0:
                sq_ind = (x // 3) * 3 + (y // 3)
                for n in range(1, 10):
                    if self.is_possible_value(x, y, sq_ind, n):

                        self.cur_ind += 1
                        self.grid[x, y] = n
                        self.on_line[x, n - 1] = self.on_colm[y, n - 1] = self.on_subs[
                            sq_ind, n - 1
                        ] = True

                        self._do_solve()

                        self.cur_ind -= 1
                        self.grid[x, y] = 0
                        self.on_line[x, n - 1] = self.on_colm[y, n - 1] = self.on_subs[
                            sq_ind, n - 1
                        ] = False
                return
        self.solutions.append(np.array(self.grid))

    def is_possible_value(self, x, y, sq_ind, n):
        """ Check whether n can possibly be added in the
			partially solved sudoku grid (at x,y position)

		Args:
			x (int): line index
			y (int): column index
			n (int): number of try at x and y coordinate
			grid (np.ndarray): the unsolved sudoku grid

		Returns:
			bool: True if n is not already in a line, column, or subsquare
        
        Note:
            This is a critical function 
		"""

        return (
            self.on_line[x, n - 1] == False
            and self.on_colm[y, n - 1] == False
            and self.on_subs[sq_ind][n - 1] == False
        )

    def _enough_solution_found(self):
        return len(self.solutions) >= self.max_solution

    def raise_error_if_max_solution_not_valid(self):
        if self.max_solution < 1:
            raise ValueError(
                "Maximum number of solutions to search should be 1 or more"
            )


def is_valid_solution(sudoku):
    """ Check that a grid is a 9x9 sudoku solutions

	Args:
	  grid (np.ndarray): a 9x9 array

	Returns:
	  bool: True if the grid is a valid sudoku results

	Notes:
	  Check that each line, column and sub-square contains 
	  all number of 1 to 9
	"""

    elem = [e for e in range(1, 10)]
    # Check for lines
    for line_ind in range(9):
        if sorted(sudoku[line_ind]) != elem:
            return False
    # Check for columns
    for column_ind in range(9):
        if sorted(sudoku[:, column_ind]) != elem:
            return False
    # Check for sub-square
    for x_init in [0, 3, 6]:
        for y_init in [0, 3, 6]:
            if (
                sorted(sudoku[x_init : x_init + 3, y_init : y_init + 3].flatten())
                != elem
            ):
                return False

    return True

