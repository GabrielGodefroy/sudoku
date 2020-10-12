#pragma once

#include <array>
#include <string>
#include <iostream>

/*! \file grid.hpp
 * 	\brief Data structures for storing a Sudoku
 */

namespace sudoku
{

    /*! \class Array2D
     *  \brief Data structure storing an Array2D within a std::array
     */
    template <typename ELEM, std::size_t NB_LINE, std::size_t NB_COLUMN>
    class Array2D {
        public :
        Array2D() { values.fill(0); }
        Array2D(const ELEM &v) { values.fill(v); }

        ELEM &operator()(std::size_t l, std::size_t c)
        {
            return values[l * NB_COLUMN + c];
        }
        ELEM operator()(std::size_t l, std::size_t c) const
        {
            return values[l * NB_COLUMN + c];
        }
        template <typename T,  std::size_t L, std::size_t C>
        friend std::ostream &operator<<(std::ostream &stream, const Array2D<T, L, C> grid);
        protected:
        std::array<ELEM, NB_LINE * NB_COLUMN> values;
    };

    template <typename T,   std::size_t L, std::size_t C>
    std::ostream &operator<<(std::ostream &stream, const Array2D<T, L, C> grid)
    {
        const char sep = ' ';
        const char eol = '\n';
        for (std::size_t l = 0; l < L; ++l)
        {
            for (std::size_t c = 0; c < C; ++c)
            {
                stream << grid(l, c) << sep;
            }
            stream << eol;
        }
        return stream;
    }

    typedef  unsigned short ushort;

    /*! \class Array2D_9x9 
    *   \brief Stores a 9x9 grid
    */
    template <typename ELEM>
    class Array2D_9x9 : public Array2D<ELEM,  9, 9>
    {
    public:
        Array2D_9x9() : Array2D<ELEM, 9,9>(){  }
        Array2D_9x9(const ELEM &v) : Array2D<ELEM,9,9>(v){  }

    };

    typedef Array2D_9x9<ushort> Grid9x9;

    /*! \class SudokuGrid
     *   \brief Data structure for storing a sudoku 
     */
    class SudokuGrid : public Grid9x9
    {
    public:

        SudokuGrid() : Grid9x9(0) {}
        SudokuGrid(const std::string&);

        static SudokuGrid load_from_file(const std::string& filepath);

        bool is_set(ushort l, ushort c) const { return operator()(l, c) != 0; }
        void unset(ushort l, ushort c) { operator()(l, c) = 0; }

        /*! \return the index of the box (0 upper left, to 8 bottom right) */
        static ushort get_box(ushort l, ushort c)
        {
            return (l / 3) * 3 + c / 3;
        }

        static bool is_solution(const SudokuGrid&);
        static bool respect_constraints(const SudokuGrid &clues, const SudokuGrid &solution);

    };
} // namespace sudoku