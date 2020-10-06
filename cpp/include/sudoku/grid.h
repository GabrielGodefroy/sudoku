#pragma once

#include <array>
#include <string>

namespace sudoku
{

    /*! \class Array2D_9x9 
    * \brief Stores a 9x9 grid within std::array 
    */
    template <typename ELEM>
    class Array2D_9x9
    {
    public:
        Array2D_9x9() { values.fill(0); }
        Array2D_9x9(const ELEM &v) { values.fill(v); } // values.fill(v)

        ELEM &operator()(int l, int c)
        {
            return values[l * 9 + c];
        }
        ELEM operator()(int l, int c) const
        {
            return values[l * 9 + c];
        }
        // TODO std::string to_string()

    protected:
        std::array<ELEM, 9 * 9> values;
    };

    typedef Array2D_9x9<short> Grid9x9;

    /*! \class SudokuGrid
    *   \brief Data structure for storing a sudoku 
    */ 
    class SudokuGrid : public Grid9x9 {
        // is_set(int l, int c)
        // unset(int l, int c)
        // is_valid_clues()
        // is_valid_solution()
    };

} // namespace sudoku