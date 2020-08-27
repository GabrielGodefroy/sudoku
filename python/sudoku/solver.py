import numpy as np 

# https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
# https://www.youtube.com/watch?v=G_UYXzGuqvM
# https://github.com/JoeKarlsson/python-sudoku-generator-solver/blob/master/sudoku.py




class Solver:

	def __init__(self):
		self.max_solution = 1
		self.solutions = []

	def solve(self,grid):
		raise_error_if_input_not_valid(grid)
		self.solutions = []
		self._do_solve(grid)
		return self.solutions


	def _do_solve(self, grid):
		# enough solutions were found
		if(len(self.solutions)>=self.max_solution):
			return

		for x in range(9):
			for y in range(9):
				if grid[x,y] == 0:
					for n in range(1,10):
						if self.is_possible_value(x,y, n, grid):
							grid[x,y] = n
							self._do_solve(grid)
							grid[x,y] = 0
					return
		#print(np.array(grid),'\n')
		self.solutions.append(np.array(grid))
		#print("solutions", self.solutions, len(self.solutions))

	def is_possible_value(self, x, y, n, sudoku):
		''' Check whether n can possibly be added in the
			partially solved sudoku grid (at x,y position)

		Args:
			x (int): line index
			y (int): column index
			n (int): number of try at x and y coordinate
			grid (np.ndarray): the unsolved sudoku grid

		Returns:
			bool: True if n is not already in a line, column, or subsquare
		'''

		for i in range(0,9):
			if sudoku[i,y] == n : 
				return False
		for i in range(0,9):
			if sudoku[x,i] == n : 
				return False
		x0 = (x//3)*3
		y0 = (y//3)*3
		for i in range(0,3):
			for j in range(0,3):
				if sudoku[x0+i,y0+j] == n:
					return False
		return True


def solve(grid):

	def is_possible_value(x, y, n, sudoku):
		for i in range(0,9):
			if sudoku[i,y] == n : 
				return False
		for i in range(0,9):
			if sudoku[x,i] == n : 
				return False
		x0 = (x//3)*3
		y0 = (y//3)*3
		for i in range(0,3):
			for j in range(0,3):
				if sudoku[x0+i,y0+j] == n:
					return False
		return True


	for y in range(9):
		for x in range(9):
			if grid[y,x] == 0:
				for n in range(1,10):
					if is_possible_value(y,x,n, grid):
						grid[y,x] = n
						solve(grid)
						grid[y,x] = 0
				return
	print(np.array(grid),'\n')



def raise_error_if_input_not_valid(sudoku):
	""" Check that a grid is a 9x9 sudoku respects the sudoku constraints

	Args:
	  grid (np.ndarray): a 9x9 array
	"""

	if(type(sudoku) != np.ndarray):
		raise TypeError("Sudoku should be given as a numpy.ndarray")
	
	if(sudoku.shape != (9,9)):
		raise ValueError("Sudoku should be 9x9")

	if((sudoku < 0).any() or (sudoku > 9).any() ):
		raise ValueError("Value should be between 0 and 9")

	def raise_error_if_subset_not_valid(subset, text):
		""" Check that a subset (line, column or subsquare) 
		does not contains any duplicated values (except 0). """

		subset = sorted(subset)

		for ind in range(len(subset)-1):
			if (subset[ind]==subset[ind+1] and subset[ind] != 0):
				raise ValueError("Problem in input grid at {}".format(text))


	for line_ind in range(9):
		subset = sudoku[line_ind]
		raise_error_if_subset_not_valid(subset, "line {}".format(line_ind) )
	for column_ind in range(9):
		subset = sudoku[:,column_ind]
		raise_error_if_subset_not_valid(subset, "row {}".format(column_ind))
	for x_init in [0,3,6]:
		for y_init in [0,3,6]:
			subset = sudoku[x_init:x_init+3,y_init:y_init+3].flatten()
			raise_error_if_subset_not_valid(subset, "square ({},{})".format(x_init, y_init))




def is_valid_solution(sudoku):
	''' Check that a grid is a 9x9 sudoku solutions

	Args:
	  grid (np.ndarray): a 9x9 array

	Returns:
	  bool: True if the grid is a valid sudoku results

	Notes:
	  Check that each line, column and sub-square contains 
	  all number of 1 to 9
	'''

	elem = [e for e in range(1,10)]	
	# Check for lines
	for line_ind in range(9):
		if(sorted(sudoku[line_ind]) != elem):
			return False
	# Check for columns
	for column_ind in range(9):
		if(sorted(sudoku[:,column_ind])!=elem):
			return False
	# Check for sub-square
	for x_init in [0,3,6]:
		for y_init in [0,3,6]:
			if(sorted(sudoku[x_init:x_init+3,y_init:y_init+3].flatten())!=elem):
				return False

	return True