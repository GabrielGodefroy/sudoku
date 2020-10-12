from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QWidget,
    QLineEdit,
    QFileDialog,
    QStatusBar,
)
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt

import sys
import numpy as np

from sudoku.loader import load_from_text_file
from sudoku.solver import SolverBacktracking, is_valid_solution # TODO SolverAlgoX, 

""" Graphical interface using PyQt """

class QSudokuGui(QMainWindow):
    """ Graphical interface using PyQt """

    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowTitle("Sudoku (Python3/PyQt version)")
        self.setGeometry(200, 200, 20, 20)

        self.setStatusBar(QStatusBar(self))
        self.statusBar().setFont(QFont("Arial", 16))
        self.statusBar().showMessage(" " * 10 + "Welcome to the sudoku interface", 2000)

        self.setCentralWidget(QSudokuGrid(self))

        self.setFixedSize(self.sizeHint())
        self.setFixedSize(self.size())

class QSudokuGrid(QWidget):
    """ Sudoku grid and button """

    def __init__(self, *args):
        QWidget.__init__(self, *args)
        # https://htmlcolorcodes.com/fr/
        self.colors = (
            "#A569BD",
            "#BB8FCE",
            "#D2B4DE",
            "#85C1E9",
            "#3498DB",
            "#AED6F1",
            "#FAD7A0",
            "#FDEBD0",
            "#F39C12",
        )

        self._create_button()
        self._create_events()

    def _create_button(self):
        """ Creates the sudoku and the push button """
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        self.q1 = QWidget(self)
        self.q2 = QWidget(self)
        main_layout.addWidget(self.q1, 0, 0)
        main_layout.addWidget(self.q2, 1, 0)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        self.q1.setLayout(grid_layout)

        grid_layout2 = QGridLayout()
        grid_layout2.setSpacing(10)
        self.q2.setLayout(grid_layout2)

        def _create_line_edit(x, y):
            lineedit = QLineEdit(self)
            lineedit.setValidator(QIntValidator(1, 9))
            lineedit.setFixedHeight(50)
            lineedit.setFixedWidth(50)
            lineedit.setFont(QFont("Arial", 16))
            lineedit.setAlignment(Qt.AlignCenter)
            color = self.colors[(x // 3) * 3 + (y // 3)]
            lineedit.reg = (x // 3) * 3 + (y // 3) + 1
            lineedit.setStyleSheet(f"background:{color};")
            return lineedit

        self.line_edits = []
        for x in range(9):
            self.line_edits.append([])
            for y in range(9):
                l = _create_line_edit(x, y)
                self.line_edits[-1].append(l)
                # button.setReadOnly(True)
                grid_layout.addWidget(l, x, y)

        self.load_button = self._create_pushbutton("Load")
        self.solv_button = self._create_pushbutton("Solve")
        self.chec_button = self._create_pushbutton("Check")
        self.clea_button = self._create_pushbutton("Clean")

        grid_layout2.addWidget(self.load_button, 10, 0)
        grid_layout2.addWidget(self.solv_button, 10, 1)
        grid_layout2.addWidget(self.clea_button, 10, 2)
        grid_layout2.addWidget(self.chec_button, 10, 4)

    def check_slot(self):
        clues = self.to_np_array()
        if is_valid_solution(clues):
            self.parentWidget().statusBar().showMessage(" " * 10 + "Well done!", 2000)
        else:
            self.parentWidget().statusBar().showMessage(
                " " * 10 + "Something is not quite right...", 2000
            )

    def clean_slot(self):
        for x in range(9):
            for y in range(9):
                v = 1 + (x // 3) * 3 + y // 3
                color = self.colors[v - 1]
                self.line_edits[x][y].setStyleSheet(f"background:{color};")
                self.line_edits[x][y].reg = v

                self.line_edits[x][y].setText("")
                self.line_edits[x][y].setReadOnly(False)

    def solve_slot(self):
        clues = self.to_np_array()
        try:
            solver = SolverBacktracking(clues)
            solution = solver.solve()
            for x in range(9):
                for y in range(9):
                    v = solution[x, y]
                    self.line_edits[x][y].setText(str(v))
        except Exception as e:
            print("Exception while solving the sudoku:\n\t", e)

    def load_puzzle_from_text_slot(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        if filename[0]:
            array = load_from_text_file(filename[0])
            
            for x in range(9):
                for y in range(9):
                    v = array[x,y]
                    if(v>0):
                        self.line_edits[x][y].setText(str(v))
                        self.line_edits[x][y].setReadOnly(True)
                        self.line_edits[x][y].setFont(QFont("Aria;", 18, QFont.Bold))
                    else :
                        self.line_edits[x][y].setText("")
                        self.line_edits[x][y].setReadOnly(False)
                        self.line_edits[x][y].setFont(QFont("Aria;", 16))
            #self.textedit.setText(openFileDialog)

    def to_np_array(self):
        clues = np.ndarray((9, 9), dtype=int)
        for x in range(9):
            for y in range(9):
                r = self.line_edits[x][y].text()
                if r == "" or r == "0":
                    r = 0
                else:
                    r = int(r)
                clues[x, y] = r
        return clues

    def _create_events(self):
        self.load_button.clicked.connect(self.load_puzzle_from_text_slot)
        self.solv_button.clicked.connect(self.solve_slot)
        self.clea_button.clicked.connect(self.clean_slot)
        self.chec_button.clicked.connect(self.check_slot)

    def _create_pushbutton(self, text):
        button = QPushButton(self.q2)
        button.setText(text)
        button.setFixedHeight(50)
        button.setFont(QFont("Arial", 16))
        return button


def main():
    """ Starts the PyQt application """
    app = QApplication(sys.argv)

    win = QSudokuGui()
    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



