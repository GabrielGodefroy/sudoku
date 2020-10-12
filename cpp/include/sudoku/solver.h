#pragma once

#include <sudoku/grid.hpp>

/*! \file solver.h
 * 	\brief Sudoku solver
 */

namespace sudoku
{
    /*! \brief Solvess the sudoku with given clues using DLX algorithm.
     *  \return true if a solution was found, false otherwise.
     * 
     *  \see DLX_Solver
     *  
     */
    bool solve_algo_X(const SudokuGrid &clues, SudokuGrid &result);


    class AbstractSudokuSolver
    {
    public:
        virtual bool solve(SudokuGrid &clues) = 0;
    };

    /*! \brief A solver relying on dancing link implementation of algo X 
     * 
     * \see
     *      http://mathieuturcotte.ca/textes/sudoku-dancing-links/
     *      and
     *      https://github.com/KarlHajal/DLX-Sudoku-Solver/blob/master/DLXSudokuSolver.cpp
     *      for explaination of the algorithm used,
     */
    class DLX_Solver : public AbstractSudokuSolver
    {

    public:
        DLX_Solver() : head(), headNode(&head){};

        bool solve(SudokuGrid &partial_solution)
        {
            isSolved = false;
            build_sparse_matrix(matrix);
            build_linked_list(matrix);
            transfort_list_to_current_grid(partial_solution);
            search(0, partial_solution);
            return isSolved;
        }

    protected:
        struct Node
        {

            Node *left = nullptr;
            Node *right = nullptr;
            Node *up = nullptr;
            Node *down = nullptr;
            Node *head = nullptr;

            int size = 0; //used for Column header

            struct ID
            {
                int candidate ;
                int row ;
                int column ;
            } id; //used to identify row in order to map solutions to a sudoku grid
        };

        static constexpr int MAX_K = 1000;
        static constexpr int SIZE = 9;
        static constexpr int SIZE_SQRT = 3;
        static constexpr int SIZE_SQUARED = SIZE * SIZE;

        static constexpr int ROW_NB = SIZE * SIZE * SIZE;
        static constexpr int COL_NB = 4 * SIZE * SIZE;

        Node head ;
        Node *headNode = nullptr;
        Node *solution[MAX_K];
        Node *orig_values[MAX_K];

        bool matrix[ROW_NB][COL_NB] = {{0}};
        bool isSolved = false;

        void cover_column(Node *col);
        void uncover_column(Node *col);
        void search(int k, SudokuGrid &partial_solution);

        void build_sparse_matrix(bool matrix[ROW_NB][COL_NB]);
        void build_linked_list(bool matrix[ROW_NB][COL_NB]);
        void transfort_list_to_current_grid(SudokuGrid &clues);
        void map_solution_to_grid(SudokuGrid &grid);
    };
} 