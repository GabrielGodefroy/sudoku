#define CATCH_CONFIG_MAIN // This tells Catch to provide a main() - only do this in one cpp file
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
