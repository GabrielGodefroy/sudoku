#include <QtWidgets>

#include <map>
#include <vector>
#include <array>
#include <assert.h>
#include <iostream> // TODO tmp

#include <sudoku/solver.h>
#include <sudoku/grid.hpp>

using namespace sudoku;

/*! \file qt.cpp
 * 	\brief A graphical interface for to the sudoku, built using Qt
 * 
 *  \TODO test and check memory leaks
 * 	\TODO add key event
 *  \TODO add tr()
 */

/*! \brief To write and read the values of a sudoku cell */
class SudoGridCell : public QLineEdit
{
    Q_OBJECT
public:
    SudoGridCell(QWidget *parent = nullptr, int square_number = 0);
    ~SudoGridCell();
    int value() const { return text().size() == 0 ? 0 : text().toInt(); }
protected:
    void set_color(const std::string &color);
    void set_in_square(int square_number);
    const static std::array<std::string, 9> colors_per_square; 
};


/*! \brief Organizes 81 sudoku cells */
class SudokuGridWidget : public QWidget
{
    Q_OBJECT
public:
    SudokuGridWidget(QWidget *parent = nullptr);
    ~SudokuGridWidget() {}
    SudokuGrid to_array2d() const;
    void fill_from_array2d(const SudokuGrid &g);
protected:
    Array2D<SudoGridCell *, 9, 9> cells;
};

class QSudoku : public QMainWindow
{
    Q_OBJECT
public:
    QSudoku();
    virtual ~QSudoku(){};

private slots:
    void empty();
    void load();
    void check();
    void solve();

    //private:
    //	typedef void (QNotePad::*slotfunction)();
    //	std::map<char, QNotePad::slotfunction> key_event_to_slot;

protected:
    //	void keyPressEvent(QKeyEvent *event);
    //	void init_central_widget();
    //	void init_menubar();
    //	void init_toolbar();
    //	void init_event();

    static constexpr unsigned int default_statusbar_timeout_ms = 2000;

private:
    QAction *emptyAction;
    QAction *loadAction;
    QAction *checkAction;
    QAction *solveAction;

    QPushButton *emptyButton;
    QPushButton *solvButton;
    QPushButton *checButton;
    QPushButton *loadButton;

    SudokuGridWidget *grid_widget;
};




int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QSudoku window;
    window.show();

    return app.exec();
}




QSudoku::QSudoku()
{
    this->setWindowTitle("Play a Sudoku (C++/Qt version)");
    this->setGeometry(200, 200, 20, 20);

    QVBoxLayout *v_layout = new QVBoxLayout;

    grid_widget = new SudokuGridWidget(this);
    v_layout->addWidget(grid_widget);

    QWidget *container = new QWidget(this);
    v_layout->addWidget(container);

    // TODO refactor
    QHBoxLayout *h_layout = new QHBoxLayout;
    emptyButton = new QPushButton("&Empty", this);
    emptyButton->setFont(QFont("Arial", 16));
    h_layout->addWidget(emptyButton);
    loadButton = new QPushButton("&Load", this);
    loadButton->setFont(QFont("Arial", 16));
    h_layout->addWidget(loadButton);
    checButton = new QPushButton("&Check", this);
    checButton->setFont(QFont("Arial", 16));
    h_layout->addWidget(checButton);
    solvButton = new QPushButton("&Solve", this);
    solvButton->setFont(QFont("Arial", 16));
    h_layout->addWidget(solvButton);

    container->setLayout(h_layout);

    this->setCentralWidget(new QWidget(this));
    this->centralWidget()->setLayout(v_layout);

    this->setStatusBar(new QStatusBar(this));

    QObject::connect(emptyButton, &QPushButton::clicked, this, &QSudoku::empty);
    QObject::connect(loadButton, &QPushButton::clicked, this, &QSudoku::load);
    QObject::connect(checButton, &QPushButton::clicked, this, &QSudoku::check);
    QObject::connect(solvButton, &QPushButton::clicked, this, &QSudoku::solve);
}

void QSudoku::empty()
{
    SudokuGrid g;
    grid_widget->fill_from_array2d(g);
}

void QSudoku::load()
{
    QString filename = QFileDialog::getOpenFileName(this, tr("Open"));

    if (!filename.isEmpty())
    {
        SudokuGrid g = SudokuGrid::load_from_file(filename.toStdString());
        grid_widget->fill_from_array2d(g);
    }
}

void QSudoku::check()
{
    SudokuGrid current_grid = grid_widget->to_array2d();

    if (SudokuGrid::is_solution(current_grid))
    {
        this->statusBar()->showMessage(tr("Well done; this is a valid solution"), default_statusbar_timeout_ms);
    }
    else
    {
        this->statusBar()->showMessage("Oups, you are not there yet!", default_statusbar_timeout_ms);
    }
}

void QSudoku::solve()
{
    const SudokuGrid clues = grid_widget->to_array2d();

    SudokuGrid solution;
    if (solve_algo_X(clues, solution))
    {
        grid_widget->fill_from_array2d(solution);
        this->statusBar()->showMessage("Here is a valid solution!", default_statusbar_timeout_ms);
    }
    else
    {
        this->statusBar()->showMessage("Oups, could not find a solution!", default_statusbar_timeout_ms);
    }
}

SudoGridCell::SudoGridCell(QWidget *parent, int square_number) : QLineEdit(parent)
{
    setValidator(new QIntValidator(1, 9, this));
    set_in_square(square_number);
    setMinimumSize(50, 50);

    setFont(QFont("Arial", 16));
    setAlignment(Qt::AlignCenter);
}
SudoGridCell::~SudoGridCell() {}

void SudoGridCell::set_in_square(int square_number){
    set_color(colors_per_square[square_number]);
}

    void SudoGridCell::set_color(const std::string &color)
{
    QPalette palette;
    palette.setColor(QPalette::Base, QColor(color.c_str()));
    setPalette(palette);
}

const std::array<std::string, 9> SudoGridCell::colors_per_square = {
    "#A569BD", "#BB8FCE", "#D2B4DE",
    "#85C1E9", "#3498DB", "#AED6F1",
    "#FAD7A0", "#FDEBD0", "#F39C12"};








    SudokuGridWidget::SudokuGridWidget(QWidget *parent) : QWidget(parent)
    {
        QGridLayout *grid_layout = new QGridLayout();
        for (int line = 0; line < 9; ++line)
        {
            for (int col = 0; col < 9; ++col)
            {
                int r = (line / 3) * 3 + (col / 3);
                cells(line, col) = new SudoGridCell(this, r);
                grid_layout->addWidget(cells(line, col), line, col);
            }
        }
        setLayout(grid_layout);
    }

    SudokuGrid SudokuGridWidget::to_array2d() const
    {
        SudokuGrid result;
        for (int l = 0; l < 9; l++)
        {
            for (int c = 0; c < 9; c++)
            {
                result(l, c) = cells(l, c)->value();
            }
        }
        return result;
    }

    void SudokuGridWidget::fill_from_array2d(const SudokuGrid &g)
    {
        for (int l = 0; l < 9; l++)
        {
            for (int c = 0; c < 9; c++)
            {
                const int v = g(l, c);
                if (v > 0)
                    cells(l, c)->setText(QString(char('0' + v)));
                else
                    cells(l, c)->setText("");
            }
        }
    }    

#include "qt.moc"

