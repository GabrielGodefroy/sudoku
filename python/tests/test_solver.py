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

def test_invalid():
    sudoku = load_from_text_file("../DATA/invalidSolution.txt")
    assert(is_valid_solution(sudoku)==False)
    s = Solver()
    try:
        s.solve(sudoku)
    except : 
        return 
    assert(False) # should not be reached


def test_easy():
    sudoku = load_from_text_file("../DATA/easy.txt")
    s = Solver()
    s.max_solution = 10
    solutions = s.solve(sudoku)
    for solution in solutions:
        assert(is_valid_solution(solution))
    assert(len(solutions) <= s.max_solution)

def test_performance():
    def solve_sudoku(filepath, nb_solution):
        sudoku = load_from_text_file(filepath)
        s = Solver()
        s.max_solution = nb_solution
        solutions = s.solve(sudoku)
        for solution in solutions:
            assert(is_valid_solution(solution))
        assert(len(solutions) <= s.max_solution)

    solve_sudoku("../DATA/easy.txt",5)
    solve_sudoku("../DATA/NearValidSolution.txt",5)