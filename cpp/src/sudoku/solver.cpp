#include "sudoku/solver.h"

#include <vector>
#include <limits>

namespace sudoku
{
    void DLX_Solver::cover_column(Node *col)
    {
        col->left->right = col->right;
        col->right->left = col->left;
        for (Node *node = col->down; node != col; node = node->down)
        {
            for (Node *temp = node->right; temp != node; temp = temp->right)
            {
                temp->down->up = temp->up;
                temp->up->down = temp->down;
                temp->head->size--;
            }
        }
    }

    void DLX_Solver::uncover_column(Node *col)
    {
        for (Node *node = col->up; node != col; node = node->up)
        {
            for (Node *temp = node->left; temp != node; temp = temp->left)
            {
                temp->head->size++;
                temp->down->up = temp;
                temp->up->down = temp;
            }
        }
        col->left->right = col;
        col->right->left = col;
    }

    void DLX_Solver::search(int k, SudokuGrid &clues)
    {

        if (isSolved)
            return;

        if (headNode->right == headNode)
        {
            map_solution_to_grid(clues);
            isSolved = true;
            return;
        }

        //Choose Column Object Deterministically: Choose the column with the smallest Size
        Node *Col = headNode->right;
        for (Node *temp = Col->right; temp != headNode; temp = temp->right)
            if (temp->size < Col->size)
                Col = temp;

        cover_column(Col);

        for (Node *temp = Col->down; temp != Col; temp = temp->down)
        {
            solution[k] = temp;
            for (Node *node = temp->right; node != temp; node = node->right)
            {
                cover_column(node->head);
            }

            search(k + 1, clues);

            temp = solution[k];
            solution[k] = nullptr;
            Col = temp->head;
            for (Node *node = temp->left; node != temp; node = node->left)
            {
                uncover_column(node->head);
            }
        }

        uncover_column(Col);
    }

    void DLX_Solver::build_linked_list(bool matrix[ROW_NB][COL_NB])
    {

        Node *header = new Node;
        header->left = header;
        header->right = header;
        header->down = header;
        header->up = header;
        header->size = -1;
        header->head = header;
        Node *temp = header;

        //Create all Column Nodes
        for (int i = 0; i < COL_NB; i++)
        {
            Node *newNode = new Node;
            newNode->size = 0;
            newNode->up = newNode;
            newNode->down = newNode;
            newNode->head = newNode;
            newNode->right = header;
            newNode->left = temp;
            temp->right = newNode;
            temp = newNode;
        }

    DLX_Solver::Node::ID id = {0, 1, 1};
        //Add a Node for each 1 present in the sparse matrix and update Column Nodes accordingly
        for (int i = 0; i < ROW_NB; i++)
        {
            Node *top = header->right;
            Node *prev = nullptr;

            if (i != 0 && i % SIZE_SQUARED == 0)
            {
                id.candidate -= SIZE - 1;
                id.row++;
                id.column -= SIZE - 1;
            }
            else if (i != 0 && i % SIZE == 0)
            {
                id.candidate -= SIZE - 1;
                id.column++;
            }
            else
            {
                id.candidate++;
            }

            for (int j = 0; j < COL_NB; j++, top = top->right)
            {
                if (matrix[i][j])
                {
                    Node *newNode = new Node;
                    newNode->id.candidate = id.candidate;
                    newNode->id.row = id.row;
                    newNode->id.column = id.column;
                    if (prev == nullptr)
                    {
                        prev = newNode;
                        prev->right = newNode;
                    }
                    newNode->left = prev;
                    newNode->right = prev->right;
                    newNode->right->left = newNode;
                    prev->right = newNode;
                    newNode->head = top;
                    newNode->down = top;
                    newNode->up = top->up;
                    top->up->down = newNode;
                    top->size++;
                    top->up = newNode;
                    if (top->down == top)
                        top->down = newNode;
                    prev = newNode;
                }
            }
        }

        headNode = header;
    }

    void DLX_Solver::build_sparse_matrix(bool matrix[ROW_NB][COL_NB])
    {

        //Constraint 1: There can only be one value in any given cell
        int j = 0, counter = 0;
        for (int i = 0; i < ROW_NB; i++)
        { //iterate over all rows
            matrix[i][j] = 1;
            counter++;
            if (counter >= SIZE)
            {
                j++;
                counter = 0;
            }
        }

        //Constraint 2: There can only be one instance of a number in any given row
        int x = 0;
        counter = 1;
        for (j = SIZE_SQUARED; j < 2 * SIZE_SQUARED; j++)
        {
            for (int i = x; i < counter * SIZE_SQUARED; i += SIZE)
                matrix[i][j] = 1;

            if ((j + 1) % SIZE == 0)
            {
                x = counter * SIZE_SQUARED;
                counter++;
            }
            else
                x++;
        }

        //Constraint 3: There can only be one instance of a number in any given column
        j = 2 * SIZE_SQUARED;
        for (int i = 0; i < ROW_NB; i++)
        {
            matrix[i][j] = 1;
            j++;
            if (j >= 3 * SIZE_SQUARED)
                j = 2 * SIZE_SQUARED;
        }

        //Constraint 4: There can only be one instance of a number in any given region
        x = 0;
        for (j = 3 * SIZE_SQUARED; j < COL_NB; j++)
        {

            for (int l = 0; l < SIZE_SQRT; l++)
            {
                for (int k = 0; k < SIZE_SQRT; k++)
                    matrix[x + l * SIZE + k * SIZE_SQUARED][j] = 1;
            }

            int temp = j + 1 - 3 * SIZE_SQUARED;

            if (temp % (int)(SIZE_SQRT * SIZE) == 0)
                x += (SIZE_SQRT - 1) * SIZE_SQUARED + (SIZE_SQRT - 1) * SIZE + 1;
            else if (temp % SIZE == 0)
                x += SIZE * (SIZE_SQRT - 1) + 1;
            else
                x++;
        }
    }

    void DLX_Solver::transfort_list_to_current_grid(SudokuGrid &clues)
    {
        int index = 0;
        for (int i = 0; i < SIZE; i++)
            for (int j = 0; j < SIZE; j++)
                if (clues(i, j) > 0)
                {
                    Node *Col = nullptr;
                    Node *temp = nullptr;
                    for (Col = headNode->right; Col != headNode; Col = Col->right)
                    {
                        for (temp = Col->down; temp != Col; temp = temp->down)
                            if (temp->id.candidate == clues(i, j) && (temp->id.row - 1) == i && (temp->id.column - 1) == j)
                            {
                                cover_column(Col);
                                orig_values[index] = temp;
                                index++;
                                for (Node *node = temp->right; node != temp; node = node->right)
                                {
                                    cover_column(node->head);
                                }
                            }
                    }
                }
    }

    void DLX_Solver::map_solution_to_grid(SudokuGrid &grid)
        {

            for (int i = 0; solution[i] != nullptr; i++)
            {
                grid(solution[i]->id.row - 1, solution[i]->id.column - 1) = solution[i]->id.candidate;
            }
            for (int i = 0; orig_values[i] != nullptr; i++)
            {
                grid(orig_values[i]->id.row - 1, orig_values[i]->id.column - 1) = orig_values[i]->id.candidate;
            }
        }

    bool solve_algo_X(const SudokuGrid &clues, SudokuGrid &result)
    {
        DLX_Solver solver;
        result.copy(clues); // todo
        bool is_solved = solver.solve(result);
        return is_solved;
    }

} // namespace sudoku