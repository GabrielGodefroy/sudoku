import numpy as np
from itertools import product

from sudoku.loader import raise_error_if_input_not_valid
from sudoku.grid import SudokuGrid


def respect_clues(clues, solution):
    """ Checks that solution respects all clues 

	Returns:
	  bool: True if solution respects all clues
    """
    for x, y in product(range(9), range(9)):
        if clues[x, y] != 0 and clues[x, y] != solution[x, y]:
            return False
    return True


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


class SolverBacktracking:
    """ Solves a sudoku puzzle using a backtracking algorithm 
    
    Note: 
        This simple (dummy?) implementation relies on SudokuGrid

    See:
        EfficientSolver / EfficientSudokuGrid
    """

    def __init__(self, np_clues):
        """ Creates the solver object 
		
		Args:
			clues: given constraints
		"""
        self.set_clues(np_clues)

    def solve(self):
        self.grid = SudokuGrid(self.np_clues)
        self.solution = None
        self.do_solve()
        return self.solution

    def set_clues(self, np_clues):
        raise_error_if_input_not_valid(np_clues)
        self.np_clues = np_clues.copy()

    def do_solve(self):
        if self.solution is not None:
            return
        for x, y in product(range(9), range(9)):  #
            if self.grid[x, y] == 0:
                for n in range(1, 10):
                    if self.grid.valid(x, y, n):
                        self.grid[x, y] = n
                        self.do_solve()
                        self.grid[x, y] = 0
                return
        self.solution = self.grid.grid.copy()


class SolverAlgoX:
    """  Interface for a function that solves a modified version of the Sudoku 

    Algorithm X (barely) modified from https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html 

    Algorithm X is implemented as a set of functions but interfaced in this class 
    for consistency with the backtracking implementation
    """

    def __init__(self, clues):
        self.clues = clues.copy()

    def solve(self):
        def exact_cover(X, Y):
            X = {j: set() for j in X}
            for i, row in Y.items():
                for j in row:
                    X[j].add(i)
            return X

        def solve(X, Y, solution):
            if not X:
                yield list(solution)
            else:
                c = min(X, key=lambda c: len(X[c]))
                for r in list(X[c]):
                    solution.append(r)
                    cols = select(X, Y, r)
                    for s in solve(X, Y, solution):
                        yield s
                    deselect(X, Y, r, cols)
                    solution.pop()

        def select(X, Y, r):
            cols = []
            for j in Y[r]:
                for i in X[j]:
                    for k in Y[i]:
                        if k != j:
                            X[k].remove(i)
                cols.append(X.pop(j))
            return cols

        def deselect(X, Y, r, cols):
            for j in reversed(Y[r]):
                X[j] = cols.pop()
                for i in X[j]:
                    for k in Y[i]:
                        if k != j:
                            X[k].add(i)

        grid = self.clues
        assert grid.shape == (9, 9)
        R, C = (3, 3)
        N = R * C
        X = (
            [("rc", rc) for rc in product(range(N), range(N))]
            + [("rowN", rn) for rn in product(range(N), range(1, N + 1))]
            + [("colN", cn) for cn in product(range(N), range(1, N + 1))]
            + [("boxN", bn) for bn in product(range(N), range(1, N + 1))]
        )
        Y = dict()
        for r, c, n in product(range(N), range(N), range(1, N + 1)):
            b = (r // R) * R + (c // C)
            Y[(r, c, n)] = [
                ("rc", (r, c)),
                ("rowN", (r, n)),
                ("colN", (c, n)),
                ("boxN", (b, n)),
            ]
        X = exact_cover(X, Y)
        for i, row in enumerate(grid):
            for j, n in enumerate(row):
                if n:
                    select(X, Y, (i, j, n))
        for solution in solve(X, Y, []):
            for (r, c, n) in solution:
                grid[r, c] = n
            return grid

