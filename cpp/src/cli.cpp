#include <cstdlib>
#include <iostream>
#include <algorithm>

#include <sudoku/grid.hpp>
#include <sudoku/solver.h>

using namespace sudoku;

char *getCmdOption(char **begin, char **end, const std::string &option);
bool cmdOptionExists(char **begin, char **end, const std::string &option);
void display_help();

/*! \brief Command line interface to call solve_algo_X
 * 
 *  Clues are provided as text file.
 *  Run ./cli --help for user help
 */
int main(int argc, char *argv[])
{
    if (argc == 1 || cmdOptionExists(argv, argv + argc, "-h") || cmdOptionExists(argv, argv + argc, "--help"))
    {
        display_help();
        return EXIT_SUCCESS;
    }

    char *filename = getCmdOption(argv, argv + argc, "-f");
    if (!filename){
        std::cout << "Error: could not find the file name" << std::endl;
    }
    else
    {
            // TODO exception in load?
            SudokuGrid clues = SudokuGrid::load_from_file(filename);
            SudokuGrid result;
            bool has_solution = solve_algo_X(clues, result);

            if(!has_solution) {
                std::cout << "Could not find a solution for \t" << clues << std::endl;
                return EXIT_SUCCESS;

            }

            std::cout << result << std::endl;

            bool do_check = cmdOptionExists(argv, argv + argc, "--check");
            if (do_check)
            {

                if (SudokuGrid::is_solution(result) && SudokuGrid::respect_constraints(clues, result))
                {
                    std::cout << "Solution was successfully checked" << std::endl;
                }
                else
                {
                    std::cout << "### Implementation error: the solution is not correct! ###" << std::endl;
                    return EXIT_FAILURE;
                }
            }
        }


    return EXIT_SUCCESS;
}

/*! \brief helps parsing the arguments
*   \return the parameters follow the string \param option
 *  \see https://stackoverflow.com/questions/865668/how-to-parse-command-line-arguments-in-c
 */

char *getCmdOption(char **begin, char **end, const std::string &option)
{
    char **itr = std::find(begin, end, option);
    if (itr != end && ++itr != end) // todo ?
    {
        return *itr;
    }
    return nullptr;
}

/*! \brief helps parsing the arguments
*   \return true if the string \param option is in the list of argument 
 *  \see https://stackoverflow.com/questions/865668/how-to-parse-command-line-arguments-in-c
 */
bool cmdOptionExists(char **begin, char **end, const std::string &option)
{
    return std::find(begin, end, option) != end;
}

void display_help()
{
    std::cout << "\n Sudoku solver (C++/command line version)\n\n"
                 "   -h --help:      displays this help\n"
                 "   -f <file_path>: to display this help\n"
                 "   --check:        to perform validity check on the solution.\n"
                 "                                   (Author: Gabriel Godefroy)"
              << std::endl;
}