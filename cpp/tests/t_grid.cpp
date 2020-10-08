#include "catch.hpp"

#include <sudoku/grid.hpp>

using namespace sudoku;

TEST_CASE("Check the initialization of the Grid", "[grid9x9]")
{
    Grid9x9 g;
    REQUIRE(g(0, 0) == 0);
    REQUIRE(g(8, 0) == 0);
    REQUIRE(g(0, 8) == 0);
    REQUIRE(g(8, 8) == 0);
}

TEST_CASE("Check the initialization of the grid with given value", "[grid9x9]")
{
    const short v = 5;
    Grid9x9 g = Grid9x9(5);
    REQUIRE(g(0, 0) == v);
    REQUIRE(g(8, 0) == v);
    REQUIRE(g(0, 8) == v);
    REQUIRE(g(8, 8) == v);

}

TEST_CASE("Check the setter / getter", "[grid9x9]")
{
    Grid9x9 g;

    g(1, 1) = 1;
    g(3, 4) = 8;
    g(4, 2) = 6;
    g(8, 8) = 3;

    //std::cout << g << std::flush;

    REQUIRE(g(0, 0) == 0);
    REQUIRE(g(1, 1) == 1);
    REQUIRE(g(3, 4) == 8);
    REQUIRE(g(4, 2) == 6);
    REQUIRE(g(8, 8) == 3);
}

TEST_CASE("Check for boolean", "[grid9x9]")
{
    Array2D_9x9<bool> g_bool;

    REQUIRE(g_bool(0, 0) == false);
    REQUIRE(g_bool(2, 3) == false);

    g_bool(1, 2) = true;
    REQUIRE(g_bool(1, 2) == true);
    REQUIRE(g_bool(2, 1) == false);

    g_bool(2, 1) = true;
    REQUIRE(g_bool(2, 1) == true);
}


