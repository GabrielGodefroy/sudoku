#include "catch.hpp"

#include <sudoku/grid.hpp>
#include <sudoku/solver.h>

using namespace sudoku;

static bool respect_constraints(const SudokuGrid &clues, const SudokuGrid &solution)
{
    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++)
        {
            if (clues.is_set(i, j) && clues(i, j) != solution(i, j))
            {
                std::cout << i << " " << j << " " << clues(i, j) << " " << solution(i, j) << std::endl;
                return false;
            }
        }
    }
    return true;
}

TEST_CASE("Test the solver on an empty sudoku", "[solver9x9]")
{
    SudokuGrid empty_grid;
    SudokuGrid solution;
    bool has_solution = solve_algo_X(empty_grid, solution);
    REQUIRE(has_solution == true);
    REQUIRE(SudokuGrid::is_solution(solution) == true);
    REQUIRE(respect_constraints(empty_grid, solution));
}

TEST_CASE("Test the solver on an easy sudoku", "[solver9x9]")
{
    SudokuGrid easy_grid = SudokuGrid::load_from_file("../../DATA/easy.txt");
    SudokuGrid solution;
    bool has_solution = solve_algo_X(easy_grid, solution);
    REQUIRE(has_solution == true);
    REQUIRE(SudokuGrid::is_solution(solution) == true);
    REQUIRE(respect_constraints(easy_grid, solution) == true);
}

TEST_CASE("Test the solver on an hard to backtrack sudoku", "[solver9x9]")
{
    SudokuGrid hard_grid = SudokuGrid::load_from_file("../../DATA/hard.txt");
    SudokuGrid solution;
    bool has_solution = solve_algo_X(hard_grid, solution);
    REQUIRE(has_solution == true);
    std::cout << hard_grid << std::endl;
    std::cout << solution << std::endl;
    REQUIRE(SudokuGrid::is_solution(solution) == true);
    REQUIRE(respect_constraints(hard_grid, solution) == true);
}

TEST_CASE("Test the function that check a solution sudoku on a partial solution", "[solver9x9]")
{
    SudokuGrid hard_grid = SudokuGrid::load_from_file("../../DATA/hard.txt");
    REQUIRE(SudokuGrid::is_solution(hard_grid) == false);
}

TEST_CASE("Test the function that check a solution sudoku", "[solver9x9]")
{
    SudokuGrid solved_grid = SudokuGrid::load_from_file("../../DATA/hard.solved.txt");
    REQUIRE(SudokuGrid::is_solution(solved_grid) == true);
}
