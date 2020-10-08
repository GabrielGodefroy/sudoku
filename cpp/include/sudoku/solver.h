#pragma once

#include <sudoku/grid.hpp>

namespace sudoku
{

    class AbstractSudokuSolver
    {
    public:
        virtual bool solve(SudokuGrid &clues) = 0;
    };

    class DLX_Solver : public AbstractSudokuSolver
    {

    public:
        DLX_Solver() : head(), headNode(&head){};

        bool solve(SudokuGrid &clues)
        {
            isSolved = false;
            build_sparse_matrix(matrix);
            build_linked_list(matrix);
            transfort_list_to_current_grid(clues);
            search(0, clues);
            if (!isSolved)
                std::cout << "No Solution!" << std::endl;
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

        Node head;
        Node *headNode;
        Node *solution[MAX_K];
        Node *orig_values[MAX_K];

        bool matrix[ROW_NB][COL_NB] = {{0}};
        bool isSolved = false;

        //===============================================================================================================//
        //---------------------------------------------DLX Functions-----------------------------------------------------//
        //===============================================================================================================//

        void cover_column(Node *col);
        void uncover_column(Node *col);
        void search(int k, SudokuGrid &clues);

        //===============================================================================================================//
        //----------------------Functions to turn a Sudoku grid into an Exact Cover problem -----------------------------//
        //===============================================================================================================//

        //--------------------------BUILD THE INITIAL MATRIX CONTAINING ALL POSSIBILITIES--------------------------------//
        void build_sparse_matrix(bool matrix[ROW_NB][COL_NB]);

        //-------------------BUILD A TOROIDAL DOUBLY LINKED LIST OUT OF THE SPARSE MATRIX-------------------------//
        void build_linked_list(bool matrix[ROW_NB][COL_NB]);

        //-------------------COVERS VALUES THAT ARE ALREADY PRESENT IN THE GRID-------------------------//
        void transfort_list_to_current_grid(SudokuGrid &clues);

        //===============================================================================================================//
        //----------------------------------------------- Print Functions -----------------------------------------------//
        //===============================================================================================================//

        void map_solution_to_grid(SudokuGrid &grid);
    };

    /*! \brief TODO 
    http://mathieuturcotte.ca/textes/sudoku-dancing-links/
    https://github.com/KarlHajal/DLX-Sudoku-Solver/blob/master/DLXSudokuSolver.cpp
    */
    bool solve_algo_X(const SudokuGrid &clues, SudokuGrid &result);

} // namespace sudoku