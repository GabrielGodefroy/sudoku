from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QLineEdit, QFileDialog
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt
import sys

def main():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200,200,20,20)

    win.setWindowTitle("Sudoku") 
   
    main_layout = QGridLayout()
    win.setCentralWidget(QWidget(win))
    win.centralWidget().setLayout(main_layout)

    q1 = QWidget(win.centralWidget())
    q2 = QWidget(win.centralWidget())
    main_layout.addWidget(q1, 0, 0)
    main_layout.addWidget(q2, 1, 0)
    

    grid_layout = QGridLayout()
    grid_layout.setSpacing(10)
    q1.setLayout(grid_layout)


    grid_layout2 = QGridLayout()
    grid_layout2.setSpacing(10)
    q2.setLayout(grid_layout2)

    # https://htmlcolorcodes.com/fr/
    colors = ["#A569BD", "#BB8FCE",  "#D2B4DE", 
            "#85C1E9","#3498DB","#AED6F1",
            "#FAD7A0","#FDEBD0","#F39C12"
            ]

    for x in range(9):
        for y in range(9):
            button = QLineEdit(win) 
            button.setValidator(QIntValidator(1,9))
            button.setFixedHeight(50)
            button.setFixedWidth(50)
            button.setFont(QFont('Arial', 16))
            button.setAlignment(Qt.AlignCenter)  
            color = colors[(x//3)*3+(y//3)]
            button.setStyleSheet("background:{};".format(color));
  
            #button.setReadOnly(True)
            grid_layout.addWidget(button, x, y)

    load_button = QPushButton(q2)
    load_button.setText("Load")
    solv_button = QPushButton(q2)
    solv_button.setText("Solve")
    gnrt_button = QPushButton(q2)
    gnrt_button.setText("Generate")
    
    

    help_button = QPushButton(q2)
    help_button.setText("Help")
    chec_button = QPushButton(q2)
    chec_button.setText("Check")

    load_button.setFixedHeight(50)
    solv_button.setFixedHeight(50)
    gnrt_button.setFixedHeight(50)
    help_button.setFixedHeight(50)
    chec_button.setFixedHeight(50)
    
    load_button.setFont(QFont('Arial', 16))
    solv_button.setFont(QFont('Arial', 16))
    gnrt_button.setFont(QFont('Arial', 16))
    help_button.setFont(QFont('Arial', 16))
    chec_button.setFont(QFont('Arial', 16))

    grid_layout2.addWidget(load_button, 10, 0)
    grid_layout2.addWidget(solv_button, 10, 1)
    grid_layout2.addWidget(gnrt_button, 10, 2)
    grid_layout2.addWidget(help_button, 10, 3)
    grid_layout2.addWidget(chec_button, 10, 4)

    def print_todo(text):
        print(text)

    def load_puzzle_from_text(arg=win):
        filename = QFileDialog.getOpenFileName(win, 'Open File')
        if filename[0]:
            f = open(filename[0],'r')
            with f:
                data = f.read()
                print(data)
                #self.textedit.setText(openFileDialog)

    load_button.clicked.connect(load_puzzle_from_text) 

    win.setFixedSize(win.sizeHint())
    win.setFixedSize(win.size())
    win.show()
    sys.exit(app.exec_())

main()  # make sure to call the function