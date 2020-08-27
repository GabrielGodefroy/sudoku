# https://numpy.org/doc/stable/reference/generated/numpy.array.html?highlight=array#numpy.array
import numpy as np 
from solver import Solver, load_from_text_file
# from sudoku import *

# TODO check line column

grid = np.array([[0, 0, 3, 0, 2, 0, 6, 0, 0],
		[9, 0, 0, 3, 0, 5, 0, 0, 1],
		[0, 0, 1, 8, 0, 6, 4, 0, 0],
		[0, 0, 8, 1, 0, 2, 9, 0, 0],
		[7, 0, 0, 0, 0, 0, 0, 0, 8],
		[0, 0, 6, 7, 0, 8, 2, 0, 0],
		[0, 0, 2, 6, 0, 9, 5, 0, 0],
		[8, 0, 0, 2, 0, 3, 0, 0, 9],
		[0, 0, 5, 0, 1, 0, 3, 0, 0]])

grid = np.array([[0, 0, 3, 0, 2, 0, 6, 0, 0],
		[9, 0, 0, 3, 0, 5, 0, 0, 1],
		[0, 0, 1, 8, 0, 6, 4, 0, 0],
		[0, 0, 8, 1, 0, 2, 9, 0, 0],
		[7, 0, 0, 0, 0, 0, 0, 0, 8],
		[0, 0, 6, 7, 0, 8, 2, 0, 0],
		[0, 0, 2, 6, 0, 9, 5, 0, 0],
		[8, 0, 0, 2, 0, 3, 0, 0, 9],
		[0, 0, 0, 0, 0, 0, 0, 0, 0]])



def main():
	# todo
	pass

#print()
#print(is_valid_solution(grid))
s = Solver()
s.solve(grid)
[print(a) for a in s.solution]
#[print(is_valid_solution(a)) for a in s.solution]

#solve(grid)
