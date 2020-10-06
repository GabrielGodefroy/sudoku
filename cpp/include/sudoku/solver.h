#pragma once

#include <sudoku/grid.h>

namespace sudoku
{

    /*! \brief TODO 
    http://mathieuturcotte.ca/textes/sudoku-dancing-links/
    */
    bool solve_algo_X(const Grid9x9 &clues, Grid9x9 &result);

    /*! \return true if the provided grid is a valid sudoku */
    bool check_result(const Grid9x9 &sudoku); //TODO implement

    /*! \return true if the provided grid of clues is valid */
    bool check_clues(const Grid9x9 &sudoku); //TODO implement

} // namespace sudoku