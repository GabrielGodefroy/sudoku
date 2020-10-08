#include <cstdlib>
#include <iostream>
#include <algorithm>

#include <sudoku/grid.hpp>
#include <sudoku/solver.h>


using namespace sudoku;

// https://stackoverflow.com/questions/865668/how-to-parse-command-line-arguments-in-c

char* getCmdOption(char ** begin, char ** end, const std::string & option)
{
    char ** itr = std::find(begin, end, option);
    if (itr != end && ++itr != end)
    {
        return *itr;
    }
    return nullptr;
}

bool cmdOptionExists(char** begin, char** end, const std::string& option)
{
    return std::find(begin, end, option) != end;
}




int main(int argc, char *argv[])
{

    std::cout << argc << std::endl;

    if(argc == 1 || cmdOptionExists(argv, argv+argc, "-h"))
    {
        std::cout << "here is the help" << std::endl; 
        return EXIT_SUCCESS;
    }

    char* filename = getCmdOption(argv, argv + argc, "-f");
    if (filename)
    {
        SudokuGrid clues = SudokuGrid::load_from_file(filename);
        SudokuGrid result ;
        bool has_solution = solve_algo_X(clues, result);

        if(has_solution) {
            std::cout << result << std::endl;
        } else {
            std::cout << "Could not find a solution for \t" << clues << std::endl;
            return EXIT_SUCCESS;

        }
        //try {
        //} catch {   
        //}
        //auto filename = argv[filename_ind];
        //std::cout << filename << std::endl;
        // Do interesting things
        // ...
    }




    return EXIT_SUCCESS;
}
