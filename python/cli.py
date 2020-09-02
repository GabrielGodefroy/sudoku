""" 
Main executable

Load the 9x9 sudoku puzzle, check it's validity, solve it,
and display one or several possible solution(s)
"""

import argparse

from sudoku.loader import load_from_text_file
from sudoku.solver import Solver 

def parse_arg():
    """ Create a argparse object, parses the arguments 

    Returns: the parsed arguments
    """

    parser = argparse.ArgumentParser(description='Solve a sudoku puzzle')
    parser.add_argument('-f','--file', required=True, metavar='filepath', type=str, 
        dest='filepath',
        help='Path to the file containing the puzzle to solve')
    parser.add_argument('-n','--nb-solution', dest='max_nb_sol',
        default=1, type=int,
        help='The maximum number of solutions to return')

    args = parser.parse_args()
    return args 

def main():
    args = parse_arg()
    
    
    try:   
        s = Solver()
        s.max_solution = args.max_nb_sol
        sudoku = load_from_text_file(args.filepath)
        solutions = s.solve(sudoku)
        for solution in solutions:
            print('\n'.join([' '.join([str(cell) for cell in row]) for row in solution]),end="\n\n")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()