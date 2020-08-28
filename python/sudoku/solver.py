import numpy as np
import itertools

from sudoku.loader import raise_error_if_input_not_valid

""" 
Solver for the sudoku puzzle
"""

# https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
# https://www.youtube.com/watch?v=G_UYXzGuqvM
# https://github.com/JoeKarlsson/python-sudoku-generator-solver/blob/master/sudoku.py

class Solver:
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

        if self.max_solution < 1:
            raise ValueError(
                "Maximum number of solutions to search should be 1 or more"
            )

        self._init_possibility(grid)
        self._init_order(grid)

        self.solutions = []
        self._do_solve(grid)
        #print(self.solutions)
        return self.solutions




    def _init_possibility(self, grid):
        """ Build a dictionnary of possible values for each cell to fill """
        self.possibility = {}
        for x, y in itertools.product(range(9), range(9)):
            if grid[x, y] == 0:

                cur_post = [e for e in range(1, 10)]
                if grid[x, y] == 0:
                    for e in grid[x]:
                        if e in cur_post:
                            cur_post.remove(e)
                    for e in grid[:, y]:
                        if e in cur_post:
                            cur_post.remove(e)
                    x_init = (x // 3)*3
                    y_init = (y // 3)*3
                    assert(len(grid[x_init : x_init + 3, y_init : y_init + 3].flatten())==9)
                    for e in grid[x_init : x_init + 3, y_init : y_init + 3].flatten():
                        if e in cur_post:
                            cur_post.remove(e)
                self.possibility[(x, y)] = cur_post 


    def _init_order(self, grid):
        """ Build a traversing order, from the cells with less possible
        values to the cells with more
        
        Notes:
            This order is not updated while solving the sudoku
        """
        self.order = []
        for x, y in itertools.product(range(9), range(9)):
            if grid[x, y] == 0:
                self.order.append((x, y))
        self.order = sorted(self.order, key=lambda ind: len(self.possibility[ind]))
        #print("possib",self.possibility)
        #print("order ", self.order)

    def _do_solve(self, grid):
        # enough solutions were found
        if self._enough_solution_found():
            return
        for x, y in self.order:  # itertools.product(range(9),range(9)): # 
            if grid[x, y] == 0:
                for n in self.possibility[(x, y)]:  # range(1,10): # 
                    if self.is_possible_value(x, y, n, grid):
                        grid[x, y] = n
                        self._do_solve(grid)
                        grid[x, y] = 0
                return
        self.solutions.append(np.array(grid))

    def is_possible_value(self, x, y, n, sudoku):
        """ Check whether n can possibly be added in the
			partially solved sudoku grid (at x,y position)

		Args:
			x (int): line index
			y (int): column index
			n (int): number of try at x and y coordinate
			grid (np.ndarray): the unsolved sudoku grid

		Returns:
			bool: True if n is not already in a line, column, or subsquare

        TODO

            This is the critical function. Need to be O(1)

python -m cProfile -s tottime  tests/tmp.py
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  5115176   30.355    0.000   30.355    0.000 solver.py:102(is_possible_value)
1110027/1   14.581    0.000   45.251   45.251 solver.py:88(_do_solve)
  1110027    0.245    0.000    0.315    0.000 solver.py:130(_enough_solution_found)
		"""

        for i in range(0, 9):
            if sudoku[i, y] == n:
                return False
        for i in range(0, 9):
            if sudoku[x, i] == n:
                return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if sudoku[x0 + i, y0 + j] == n:
                    return False
        return True

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

