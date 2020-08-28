import pytest
from sudoku.solver import Solver, is_valid_solution
from sudoku.loader import load_from_text_file 

def test_valid():
    sudoku = load_from_text_file("../DATA/validSolution.txt")
    assert(is_valid_solution(sudoku))
    s = Solver()
    s.max_solution = 5
    solutions = s.solve(sudoku)
    assert(len(solutions) == 1)
    for solution in solutions:
        assert(is_valid_solution(solution))

def test_empty():
    sudoku = load_from_text_file("../DATA/empty.txt")
    s = Solver()
    s.max_solution = 10
    solutions = s.solve(sudoku)
    for solution in solutions:
        assert(is_valid_solution(solution))
    assert(len(solutions) <= s.max_solution)
    assert(len(solutions) >= 1)

def test_easy():
    sudoku = load_from_text_file("../DATA/easy.txt")
    s = Solver()
    s.max_solution = 10
    solutions = s.solve(sudoku)
    for solution in solutions:
        assert(is_valid_solution(solution))
    assert(len(solutions) <= s.max_solution)
    assert(len(solutions) >= 1)

def test_hard():
    sudoku = load_from_text_file("../DATA/hard.txt")
    s = Solver()
    s.max_solution = 10
    solutions = s.solve(sudoku)
    for solution in solutions:
        assert(is_valid_solution(solution))
    assert(len(solutions) <= s.max_solution)
    assert(len(solutions) >= 1)

