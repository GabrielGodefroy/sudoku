#include "catch.hpp"

#include <sudoku/grid.hpp>
#include <sudoku/solver.h>

using namespace sudoku;

TEST_CASE("Test the solver on an empty sudoku", "[solver9x9]")
{
    SudokuGrid empty_grid;
    SudokuGrid solution;
    bool has_solution = solve_algo_X(empty_grid, solution);
    REQUIRE (has_solution == true);
    REQUIRE (SudokuGrid::is_solution(solution) == true);
}

TEST_CASE("Test the solver on an easy sudoku", "[solver9x9]")
{
    SudokuGrid easy_grid = SudokuGrid::load_from_file("../../DATA/easy.txt");;
    SudokuGrid solution;
    bool has_solution = solve_algo_X(easy_grid, solution);
    REQUIRE (has_solution == true);
    REQUIRE (SudokuGrid::is_solution(solution) == true);
}

TEST_CASE("Test the solver on an hard to backtrack sudoku", "[solver9x9]")
{
    SudokuGrid hard_grid = SudokuGrid::load_from_file("../../DATA/hard.txt");;
    SudokuGrid solution;
    bool has_solution = solve_algo_X(hard_grid, solution);
    REQUIRE (has_solution == true);   
    REQUIRE (SudokuGrid::is_solution(solution) == true);
}

TEST_CASE("Test the function that check a solution sudoku on a partial solution", "[solver9x9]")
{
    SudokuGrid hard_grid = SudokuGrid::load_from_file("../../DATA/hard.txt");
    REQUIRE (SudokuGrid::is_solution(hard_grid) == false);
}

TEST_CASE("Test the function that check a solution sudoku", "[solver9x9]")
{
    SudokuGrid solved_grid = SudokuGrid::load_from_file("../../DATA/hard.solved.txt");;
    REQUIRE (SudokuGrid::is_solution(solved_grid) == true);
}
