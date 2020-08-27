import numpy as np

from sudoku import DIM

def load_from_text_file(filepath):
	"""Load a 9x9 np.ndarray as a text file
	
	Args:
		filepath (str): path to the text file
	"""
	result = np.loadtxt(filepath,dtype=int)

	if result.shape != (DIM,DIM) :
		raise ValueError("Size should be 9x9")
	if ((result < 0).any() or (result > DIM).any() ):
		raise ValueError("Number should be between 0 and 9")
	return result