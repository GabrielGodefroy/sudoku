from sudoku.loader import load_from_text_file, raise_error_if_input_not_valid

from sudoku.solver.solver import solve, SolverKeyError

import click

import sys
import numpy as np

from enum import IntEnum


class ExitStatus(IntEnum):
    OK = 0
    NO_SOLUTION_FOUND = 1
    FILE_NOT_FOUND = 2
    INVALID_INPUT = 3
    OTHER = 4


def pretty_print(sudoku: np.ndarray) -> None:
    print(
        "\n".join([" ".join([str(cell) for cell in row]) for row in sudoku]),
        end="\n\n",
    )


@click.command()
@click.option(
    "--filename",
    help="Text file containing the sudoku puzzle to solve",
    default=None,
)
@click.option("--strategy", help="Available strategys are TODO", default=None)
def solve_interface(filename, strategy):
    """
    Command line interface for solving sudoku.

    Usage is:

    >>> python solver.py --filename <filename> [--strategy <strategy>]

    """

    if filename is None:
        print("\nMissing arguments! Use --help.\n" "Aborting...\n")
        sys.exit(ExitStatus.INVALID_INPUT)

    if strategy is None:
        strategy = "backtracking"

    try:
        sudoku = load_from_text_file(filename)
    except FileNotFoundError as e:
        print(e.strerror)
        sys.exit(ExitStatus.FILE_NOT_FOUND)
    except ValueError as e:
        print(f"Input is not valid")
        sys.exit(ExitStatus.INVALID_INPUT)

    try:
        solution = solve(sudoku, strategy)
    except SolverKeyError as e:
        print("Unknown solver strategy")
        sys.exit(ExitStatus.INVALID_INPUT)


    if solution is None:
        print(f"No solution found for hint")
        sys.exit(ExitStatus.NO_SOLUTION_FOUND)

    sys.exit(ExitStatus.OK)


if __name__ == "__main__":
    solve_interface()
