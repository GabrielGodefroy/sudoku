import pytest
from sudoku.solver import SolverBacktracking, SolverBacktrackingEfficient, SolverAlgoX
from sudoku.solver import is_valid_solution, respect_clues
from sudoku.loader import load_from_text_file 

test_data_with_solution = [
    ("../DATA/empty.txt", SolverAlgoX),
    ("../DATA/easy.txt", SolverAlgoX),
    ("../DATA/hard.txt", SolverAlgoX),
    ("../DATA/validSolution.txt", SolverAlgoX),

    ("../DATA/empty.txt", SolverBacktracking),
    #("../DATA/easy.txt", SolverBacktracking),
    ("../DATA/validSolution.txt", SolverBacktracking),

    ("../DATA/empty.txt", SolverBacktrackingEfficient),
    ("../DATA/validSolution.txt", SolverBacktrackingEfficient),
    ("../DATA/easy.txt", SolverBacktrackingEfficient),
    ("../DATA/hard.txt", SolverBacktrackingEfficient)
]

@pytest.mark.parametrize("clues_file, Solver", test_data_with_solution)
def test_empty(clues_file, Solver):
    sudoku = load_from_text_file(clues_file)
    solver = Solver(sudoku)
    solution = solver.solve()
    assert is_valid_solution(solution)
    assert respect_clues(sudoku, solution)
    assert sudoku is not solution 

