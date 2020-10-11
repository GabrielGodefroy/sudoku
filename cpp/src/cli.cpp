#include <cstdlib>
#include <iostream>
#include <algorithm>

#include <sudoku/grid.hpp>
#include <sudoku/solver.h>

using namespace sudoku;

/*! \file cli.cpp
 * 	\brief A command line interface for the sudoku
 */

class Parser
{
public:
    Parser(int argc_, char **argv_) : argc(argc_), begin_argv(argv_), end_argv(argv_ + argc_) {}
    virtual ~Parser() {}

    /*! \brief helps parsing the arguments
    *   \return the parameters follow the string \param option
    *  \see https://stackoverflow.com/questions/865668/how-to-parse-command-line-arguments-in-c
    */
    char *get_option_if_exist(const std::string &option) const
    {
        char **itr = std::find(begin_argv, end_argv, option);
        if (itr != end_argv && ++itr != end_argv)
            return *itr;
        else
            return nullptr;
    }

    /*! \brief helps parsing the arguments
    *   \return true if the string \param option is in the list of argument 
    *   \see https://stackoverflow.com/questions/865668/how-to-parse-command-line-arguments-in-c
    */
    bool is_option(const std::string &option) const
    {
        return std::find(begin_argv, end_argv, option) != end_argv;
    }

protected:
    const int argc;
    char **begin_argv;
    char **end_argv;
};

class ParseAndAct : public Parser
{
public:
    ParseAndAct(int argc_, char **argv_) : Parser(argc_, argv_), filename(get_option_if_exist("-f")) {}

    bool do_act() const
    {
        if (do_help())
        {
            return help();
        }
        else if (do_solve_and_check())
        {
            std::cout << "solve and check" << std::endl;
            return solve_and_check();
        }
        else if (do_solve())
        {
            std::cout << "solve" << std::endl;
            return solve();
        }
        else
        {
            std::cout << "Could not determine what to do..." << std::endl;
            return false;
        }
    }
private:
    const char *filename;

public:
    bool help() const
    {
        std::cout << "\n Sudoku solver (C++/command line version)\n\n"
                     "   -h --help:      displays this help\n"
                     "   -f <file_path>: to display this help\n"
                     "   --check:        to perform validity check on the solution.\n"
                     "                                   (Author: Gabriel Godefroy)"
                  << std::endl;
        return true;
    }
    
    bool solve_and_check() const
    {
        SudokuGrid clues = SudokuGrid::load_from_file(filename);
        SudokuGrid result;
        if (solve(clues, result))
        {
            if (SudokuGrid::is_solution(result) && SudokuGrid::respect_constraints(clues, result))
            {
                std::cout << "Solution was successfully checked" << std::endl;
                return true;
            }
            return false;
        }
    }

    bool solve() const
    {
        SudokuGrid clues = SudokuGrid::load_from_file(filename);
        SudokuGrid result;
        return solve(clues, result);
    }

    bool solve(SudokuGrid &clues, SudokuGrid &result) const
    {
        // TODO exception in load?
        bool has_solution = solve_algo_X(clues, result);

        if (!has_solution)
        {
            std::cout << "Could not find a solution for \t" << clues << std::endl;
            return false;
        }

        std::cout << result << std::endl;
        return true;
    }

    bool do_help() const
    {
        return argc == 1 || is_option("-h") || is_option("--help");
    }
    bool do_solve_and_check() const
    {
        return is_option("--check");
    }
    bool do_solve() const
    {
        return filename != nullptr;
    }
};

/*! \brief Command line interface to call solve_algo_X
 * 
 *  Clues are provided as text file.
 *  Run ./cli --help for user help
 */
int main(int argc, char *argv[])
{

    ParseAndAct parser(argc, argv);
    if (parser.do_act())
    {
        return EXIT_SUCCESS;
    }
    else
    {
        return EXIT_FAILURE;
    }
}
