from sudoku.generator import SudokuGenerator
from sudoku.solver import is_valid_solution
import numpy as np


def test_reproductibility():
    constant_seed = 101
    nb_generations =  50
    solutions = np.full((nb_generations,9,9),0,dtype=int)
    for x in range(nb_generations):
        generator = SudokuGenerator()
        solution = generator.generate(constant_seed)
        assert is_valid_solution(solution)
        solutions[x] = solution
    solutions = np.unique(solutions,axis=0)
    assert solutions.shape[0] == 1

def test_diversity():
    np.random.seed(101)
    nb_generations =  50
    solutions = np.full((nb_generations,9,9),0,dtype=int)
    for x in range(nb_generations):
        generator = SudokuGenerator()
        solution = generator.generate()
        assert is_valid_solution(solution)
        solutions[x] = solution
    solutions = np.unique(solutions,axis=0)
    # the likelihood of getting the same sudoku twice is VERy low 
    assert solutions.shape[0] == nb_generations 