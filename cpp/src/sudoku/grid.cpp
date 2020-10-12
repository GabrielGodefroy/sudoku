#include "sudoku/grid.hpp"

#include <vector>
#include <limits>

#include <assert.h>
#include <set>
#include <algorithm>
#include <fstream>
#include <streambuf>

namespace sudoku
{

    SudokuGrid::SudokuGrid(const std::string &representation)
    {
        int index = 0;
        auto &ref_values = values;
        std::for_each(representation.begin(), representation.end(),
                      [&index, &ref_values](const char &c) {
            if (c >= int('0') && c <= int('9'))
            {
                ref_values[index] = c - int('0');
                ++index;
            } });

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

    bool SudokuGrid::respect_constraints(const SudokuGrid &clues, const SudokuGrid &solution)
    {
        for (ushort i = 0; i < 9; i++)
        {
            for (ushort j = 0; j < 9; j++)
            {
                if (clues.is_set(i, j) && clues(i, j) != solution(i, j))
                {
                    return false;
                }
            }
        }
        return true;
    }

    bool SudokuGrid::is_solution(const SudokuGrid &grid)
    {
        typedef std::set<unsigned int> IN_REG;
        std::array<IN_REG, 9 * 3> in_region;

        for (ushort l = 0; l < 9; ++l)
        {
            for (ushort c = 0; c < 9; ++c)
            {
                ushort value = grid(l, c);
                if (value > 0)
                {
                    ushort r = SudokuGrid::get_box(l, c);
                    in_region[l].insert(value);      // lines
                    in_region[c + 9].insert(value);  // columns
                    in_region[r + 18].insert(value); // boxes
                }
            }
        }

        return std::all_of(in_region.begin(), in_region.end(), [](const IN_REG &reg) {
            return reg.size() == 9;
        });
    }

} // namespace sudoku