#include "sudoku/grid.hpp"

#include <vector>
#include <limits>

#include <assert.h>
#include <set>

#include <fstream>
#include <streambuf>

namespace sudoku
{

    SudokuGrid::SudokuGrid(const std::string &representation)
    {

        int index = 0;

        for (const char &c : representation)
        {
            if (c >= int('0') && c <= int('9'))
            {
                values[index] = c - int('0');
                ++index;
            }
        }
        assert(index == 81); // TODO exception
    }

    SudokuGrid SudokuGrid::load_from_file(const std::string &file_path)
    {
        // todo what if file not found ?
        std::ifstream t(file_path);
        std::string str((std::istreambuf_iterator<char>(t)),
                        std::istreambuf_iterator<char>());
        return SudokuGrid(str);
    }

    bool SudokuGrid::is_solution(const SudokuGrid &grid)
    {
        typedef std::set<unsigned int> IN_REG;
        std::array<IN_REG, 9*3> in_region;

        for (int l = 0; l < 9; ++l)
        {
            for (int c = 0; c < 9; ++c)
            {
                int value = grid(l, c);
                if (value > 0)
                {
                    int r = SudokuGrid::get_box(l, c);
                    in_region[l].insert(value);     // lines
                    in_region[c+9].insert(value);   // columns
                    in_region[r+18].insert(value);  // boxes
                }
            }
        }

        for (const auto& sets : in_region){
            if(sets.size()!=9){
                return false;
            }
        }
        return true;
    }

} // namespace sudoku