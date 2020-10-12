#include "catch.hpp"

#include <sudoku/grid.hpp>

using namespace sudoku;

TEST_CASE("Check for box index", "[sudoku9x9]")
{
    SudokuGrid grid;

    REQUIRE(grid.get_box(0, 0) == 0);
    REQUIRE(grid.get_box(0, 1) == 0);
    REQUIRE(grid.get_box(0, 2) == 0);

    REQUIRE(grid.get_box(1, 0) == 0);
    REQUIRE(grid.get_box(1, 1) == 0);
    REQUIRE(grid.get_box(1, 2) == 0);

    REQUIRE(grid.get_box(2, 0) == 0);
    REQUIRE(grid.get_box(2, 1) == 0);
    REQUIRE(grid.get_box(2, 2) == 0);

    REQUIRE(grid.get_box(0, 3) == 1);
    REQUIRE(grid.get_box(0, 4) == 1);
    REQUIRE(grid.get_box(0, 5) == 1);

    REQUIRE(grid.get_box(1, 3) == 1);
    REQUIRE(grid.get_box(1, 4) == 1);
    REQUIRE(grid.get_box(1, 5) == 1);

    REQUIRE(grid.get_box(3, 0) == 3);
    REQUIRE(grid.get_box(3, 1) == 3);
    REQUIRE(grid.get_box(3, 2) == 3);

    REQUIRE(grid.get_box(3, 3) == 4);
    REQUIRE(grid.get_box(3, 4) == 4);
    REQUIRE(grid.get_box(3, 5) == 4);

    REQUIRE(grid.get_box(7, 8) == 8);
    REQUIRE(grid.get_box(8, 7) == 8);
    REQUIRE(grid.get_box(8, 8) == 8);
}

TEST_CASE("Check read an empty sudoku", "[sudoku9x9]")
{
    SudokuGrid grid(std::string(81, '0'));

    REQUIRE(grid(0, 0) == 0);
    REQUIRE(grid(1, 0) == 0);
    REQUIRE(grid(0, 2) == 0);
    REQUIRE(grid(8, 8) == 0);
}

TEST_CASE("Check read a fake sudoku", "[sudoku9x9]")
{
    SudokuGrid grid(std::string(81, '9'));

    REQUIRE(grid(0, 0) == 9);
    REQUIRE(grid(1, 0) == 9);
    REQUIRE(grid(0, 2) == 9);
    REQUIRE(grid(8, 8) == 9);
}

TEST_CASE("Check read a partially defined sudoku", "[sudoku9x9]")
{
    SudokuGrid grid(
        "1	2	3	4	5	6	7	8	9"
        "5	0	0	0	0	0	0	0	0   "
        "7	0	0	0	000	0	0"
        "3	0	0	0	0	0	0	0	0"
        "4	0	0	0	0	0	0	0	0"
        "9	0	0	0	0	0	0	0	0"
        "8	0	0	0	0	0	0	0	0"
        "2	0	0	0	0	0	0	0	0"
        "600000009");
    REQUIRE(grid(0, 0) == 1);
    REQUIRE(grid(1, 0) == 5);
    REQUIRE(grid(0, 2) == 3);
    REQUIRE(grid(8, 8) == 9);
}


TEST_CASE("Load an empty sudoku from a file", "[sudoku9x9]")
{
    SudokuGrid grid = SudokuGrid::load_from_file("../../DATA/empty.txt");

    REQUIRE(grid(0, 0) == 0);
    REQUIRE(grid(1, 0) == 0);
    REQUIRE(grid(0, 2) == 0);
    REQUIRE(grid(8, 8) == 0);
}

TEST_CASE("Load a partial sudoku from a file", "[sudoku9x9]")
{
    SudokuGrid grid = SudokuGrid::load_from_file("../../DATA/easy.txt");

    REQUIRE(grid(0, 0) == 9);
    REQUIRE(grid(1, 0) == 0);
    REQUIRE(grid(2, 0) == 8);
    REQUIRE(grid(8, 6) == 5);
    REQUIRE(grid(8, 7) == 7);
    REQUIRE(grid(8, 8) == 0);
}
