#include <QtWidgets>

#include <map>
#include <vector>
#include <array>
#include <assert.h>
#include <iostream> // TODO tmp

#include <sudoku/solver.h>

using namespace sudoku ;

/*! \file qt.cpp
 * 	\brief A graphical interface for to the sudoku, built using Qt
 * 
 *  \TODO test and check memory leaks
 * 	\TODO add key event
 */


class SudoGridCell : public QLineEdit
{
    Q_OBJECT

public:
    SudoGridCell(QWidget *parent = nullptr) : QLineEdit(parent)
    {
        setValidator(new QIntValidator(1, 9, this));
        set_in_square(0);
        setMinimumSize(50, 50);

        setFont(QFont("Arial", 16));
        setAlignment(Qt::AlignCenter);
    };
    ~SudoGridCell() {}
    void set_in_square(int square_number)
    {
        assert(square_number >= 0);
        assert(square_number < 9);
        set_color(colors[square_number]);
    }
    int value() const { return text().toInt(); }

protected:
    const static std::array<std::string, 9> colors; // TODO constexpr ?
    void set_color(const std::string &color)
    {
        QPalette palette;
        palette.setColor(QPalette::Base, QColor(color.c_str()));
        setPalette(palette);
    }
};

const std::array<std::string, 9> SudoGridCell::colors = {
    "#A569BD", "#BB8FCE", "#D2B4DE",
    "#85C1E9", "#3498DB", "#AED6F1",
    "#FAD7A0", "#FDEBD0", "#F39C12"};

class SudokuGridWidget : public QWidget
{
    Q_OBJECT

public:
    SudokuGridWidget(QWidget *parent = nullptr) : QWidget(parent)
    {
        QGridLayout* grid_layout = new QGridLayout();
        for (int line = 0; line < 9; ++line)
        {
            for (int col = 0; col < 9; ++col)
            {
                int r = (line / 3) * 3 + (col / 3);

                auto cell = new SudoGridCell(this);
                cell->set_in_square(r);
                
                grid_layout->addWidget(cell, line,col);
            }
        }
        setLayout(grid_layout);
    }
    ~SudokuGridWidget() {}

    // TODO array2d to_array2d() const {}

protected:
};



class QSudoku : public QMainWindow
{
    Q_OBJECT
public:
    QSudoku();
    virtual ~QSudoku(){};

private slots:
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

private:
    //QTextEdit 	*textEdit;
    //QPushButton *quitButton;

    //QString currentFile;

private:
    QAction *loadAction;
    QAction *checkAction;
    QAction *solveAction;

    QPushButton *solvButton;
    QPushButton *checButton;
    QPushButton *loadButton;

    SudokuGridWidget* grid;
};

QSudoku::QSudoku()
{
    this->setWindowTitle("Play a Sudoku (C++/Qt version)");
    this->setGeometry(200, 200, 20, 20);


    QVBoxLayout *v_layout = new QVBoxLayout;
    
    grid = new SudokuGridWidget(this);
    v_layout->addWidget(grid);

    QWidget* container = new QWidget(this);
    v_layout->addWidget(container);

    // TODO refactor
    QHBoxLayout *h_layout = new QHBoxLayout;
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


	//loadAction   = new QAction(tr("&Load"), this);
	//connect(loadAction, &QAction::triggered, this, &QSudoku::load);
    QObject::connect(loadButton, &QPushButton::clicked,this, &QSudoku::load);
    QObject::connect(checButton, &QPushButton::clicked,this, &QSudoku::check);
    QObject::connect(solvButton, &QPushButton::clicked,this, &QSudoku::solve);




}

void QSudoku::load() {
    std::cout << " LOAD TODO " << std::endl;
}


void QSudoku::check() {
    std::cout << " CHECK TODO " << std::endl;
}


void QSudoku::solve() {
    std::cout << " SOLVE TODO " << std::endl;
}

/*

QNotePad::QNotePad() : textEdit(new QTextEdit(this)), quitButton(new QPushButton("&Quit",this)){

	this->setWindowTitle("A notepad showing photo (written in Qt)");
	this->setMinimumSize(200, 200);

	openAction   = new QAction(tr("&Open"), this);
	saveAction   = new QAction(tr("&Save"), this);
	saveAsAction = new QAction(tr("&Save As"), this);
	exitAction   = new QAction(tr("&Exit"), this);
    nextAction   = new QAction(tr("&Next"), this);
    prevAction   = new QAction(tr("&Prev"), this);

	connect(openAction, &QAction::triggered, this, &QNotePad::open);
	connect(saveAction, &QAction::triggered, this, &QNotePad::save);
	connect(saveAsAction, &QAction::triggered, this, &QNotePad::saveAs);
	connect(exitAction, &QAction::triggered, this, &QNotePad::exit);
    connect(nextAction, &QAction::triggered, this, &QNotePad::next);
	connect(prevAction, &QAction::triggered, this, &QNotePad::prev);

	init_event();

	init_central_widget();
	init_menubar();
	init_toolbar();

}

QNotePad::~QNotePad(){
    delete saveAsAction;
    delete openAction;
};
void QNotePad::init_central_widget(){

	QVBoxLayout* layout = new QVBoxLayout;
	layout->addWidget(textEdit);
	layout->addWidget(quitButton);
	
	this->setCentralWidget(new QWidget(this));
    this->centralWidget()->setLayout(layout);
    
	textEdit->viewport()->setAutoFillBackground(false);
	

	next();

}
void QNotePad::init_event(){
	QObject::connect(quitButton, &QPushButton::clicked,this, &QNotePad::exit);

	key_event_to_slot['S']   = &QNotePad::save;
	key_event_to_slot['Q']   = &QNotePad::exit;
	key_event_to_slot['O']   = &QNotePad::open;
    key_event_to_slot['N']   = &QNotePad::next;
    key_event_to_slot['P']   = &QNotePad::prev;
}


void QNotePad::init_menubar() {

       QMenuBar *qmb = new QMenuBar(this);

        QMenu *fileMenu = qmb->addMenu("&Menu");
		fileMenu->addAction(openAction);
        fileMenu->addAction(saveAsAction);
		fileMenu->addAction(saveAction);
        fileMenu = qmb->addMenu("&Exit");

        fileMenu->addAction("Exit", this, &QNotePad::close);

        this->setMenuBar(qmb);
}

void QNotePad::init_toolbar() {
		QToolBar* qtb = this->addToolBar("ToolBar");        
        qtb->addAction(prevAction);
        qtb->addAction(nextAction);
}

void QNotePad::open(){

	QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"), "",
    tr("Text Files (*.txt);;C++ Files (*.cpp *.h)"));

	if (fileName != "") {
    QFile file(fileName);
    if (!file.open(QIODevice::ReadOnly)) {
        QMessageBox::critical(this, tr("Error"), tr("Could not open file"));
        return;
    }
    QTextStream in(&file);
    textEdit->setText(in.readAll());
    file.close();
}

}


void QNotePad::save(){
     QString fileName;
    // If we don't have a filename from before, get one.
    if (currentFile.isEmpty()) {
        fileName = QFileDialog::getSaveFileName(this, "Save");
        currentFile = fileName;
    } else {
        fileName = currentFile;
    }
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QFile::Text)) {
        QMessageBox::warning(this, "Warning", "Cannot save file: " + file.errorString());
        return;
    }
    setWindowTitle(fileName);
    QTextStream out(&file);
    QString text = textEdit->toPlainText();
    out << text;
    file.close();   
}

void QNotePad::saveAs(){
    QString fileName = QFileDialog::getSaveFileName(this, "Save as");
    QFile file(fileName);

    if (!file.open(QFile::WriteOnly | QFile::Text)) {
        QMessageBox::warning(this, "Warning", "Cannot save file: " + file.errorString());
        return;
    }
    currentFile = fileName;
    setWindowTitle(fileName);
    QTextStream out(&file);
    QString text = textEdit->toPlainText();
    out << text;
    file.close();
}

void QNotePad::exit(){
	 QCoreApplication::quit();
}

void QNotePad::next(){
    photo_ind+=1;
    if(photo_ind>=int(list_of_photos.size())) {photo_ind=0;}

    QString stylesheet = stylesheet_template; 
    stylesheet.replace(QRegularExpression("IMGNAME"), list_of_photos[photo_ind]);
    textEdit->setStyleSheet(stylesheet);
}	 

void QNotePad::prev(){
    photo_ind-=1;
    if(photo_ind<0) {photo_ind=list_of_photos.size()-1;}

    QString stylesheet = stylesheet_template; 
    stylesheet.replace(QRegularExpression("IMGNAME"), list_of_photos[photo_ind]);
    textEdit->setStyleSheet(stylesheet);
}

void QNotePad::keyPressEvent(QKeyEvent* e){
	char curchar = char(e->key());
	
	auto it = key_event_to_slot.find(curchar);
	if ( it != key_event_to_slot.end() ) {
		const auto event = it->second;
		(this->*event)();
	}
}
*/

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QSudoku window;
    window.show();

    return app.exec();
}

#include "qt.moc"
