#pragma once

#include <array>
#include <string>
#include <iostream>

namespace sudoku
{

    /*! \class Array2D
     *  \brief TODO 
     */
    template <typename ELEM, unsigned int NB_LINE, unsigned int NB_COLUMN>
    class Array2D {
        public :
        Array2D() { values.fill(0); }
        Array2D(const ELEM &v) { values.fill(v); }

        ELEM &operator()(int l, int c)
        {
            return values[l * NB_COLUMN + c];
        }
        ELEM operator()(int l, int c) const
        {
            return values[l * NB_COLUMN + c];
        }

        template <typename T,  unsigned int L, unsigned int C>
        friend std::ostream &operator<<(std::ostream &stream, const Array2D<T, L, C> grid);

        protected:
        std::array<ELEM, NB_LINE * NB_COLUMN> values;

    };

    /*! \class Array2D_9x9 
    *   \brief Stores a 9x9 grid within std::array 
    */
    template <typename ELEM>
    class Array2D_9x9 : public Array2D<ELEM, 9, 9>
    {
    public:
        Array2D_9x9() : Array2D<ELEM,9,9>(){  }
        Array2D_9x9(const ELEM &v) : Array2D<ELEM,9,9>(v){  }

    };

    template <typename T,  unsigned int L, unsigned int C>
    std::ostream &operator<<(std::ostream &stream, const Array2D<T, L, C> grid)
    {
        const char sep = '\t';
        const char eol = '\n';
        for (int l = 0; l < L; ++l)
        {
            for (int c = 0; c < C; ++c)
            {
                stream << grid(l, c) << sep;
            }
            stream << eol;
        }
        return stream;
    }

    typedef Array2D_9x9<unsigned short> Grid9x9;

    /*! \class SudokuGrid
     *   \brief Data structure for storing a sudoku 
     */
    class SudokuGrid : public Grid9x9
    {
    public:
        SudokuGrid() : Grid9x9() {}
        SudokuGrid(const std::string&);
        static SudokuGrid load_from_file(const std::string& filepath);

        bool is_set(int l, int c) const { return operator()(l, c) != 0; }
        void unset(int l, int c) { operator()(l, c) = 0; }

        static unsigned short get_box(int l, int c)
        {
            return (l / 3) * 3 + c / 3;
        }

        static bool is_solution(const SudokuGrid&);
        static bool respect_constraints(const SudokuGrid &clues, const SudokuGrid &solution);

        void copy(const SudokuGrid& rhs) {
            values = rhs.values;
        }
    };
} // namespace sudoku