import pytest
from sudoku.solver import SolverBacktracking, is_valid_solution
from sudoku.loader import load_from_text_file 


def has_one_solution(filepath):
    sudoku = load_from_text_file(filepath)
    s = SolverBacktracking(3)
    solutions = s.solve(sudoku)
    for solution in solutions:
        print(solution)
        assert(is_valid_solution(solution))
    assert(len(list(solutions)) == 1 )

def has_several_solutions(filepath):
    nb_sol = 3
    sudoku = load_from_text_file(filepath)
    s = SolverBacktracking(nb_sol)
    solutions = s.solve(sudoku)
    assert( (solutions[0] == solutions[1]).all() == False)
    assert( (solutions[0] == solutions[2]).all() == False)
    assert( (solutions[1] == solutions[2]).all() == False)
    for solution in solutions:
        assert(is_valid_solution(solution))
    assert(len(list(solutions)) == nb_sol )

def test_valid():
    sudoku = load_from_text_file("../DATA/validSolution.txt")
    assert(is_valid_solution(sudoku))
    s = SolverBacktracking()
    s.max_solution = 5
    solutions = s.solve(sudoku)
    assert(len(solutions) == 1)
    for solution in solutions:
        assert(is_valid_solution(solution))

def test_empty():
    sudoku = load_from_text_file("../DATA/empty.txt")
    s = SolverBacktracking()
    s.max_solution = 10
    solutions = s.solve(sudoku)
    for solution in solutions:
        assert(is_valid_solution(solution))
    assert(len(solutions) <= s.max_solution)
    assert(len(solutions) >= 1)

def test_easy():
    has_several_solutions("../DATA/easy.txt")

def test_hard():
    has_one_solution("../DATA/hard.txt")
