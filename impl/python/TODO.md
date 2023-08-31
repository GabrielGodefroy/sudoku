
#  Implement a simple sudoku solver in python (step1: up-and-running)

- [x] Implement a first solver
- [x] Implement a first application to solve a sudoku
- [x] Add a Continuous Integration step to help preparing pull-request
  - [x] [github actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)
  - [x] [page for python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
  - [x] [python with conda](https://autobencoder.com/2020-08-24-conda-actions/)
- [x] Add a pre-commit step
  - [x] Use black/flake8
  - [x] Use pytest for unittest
  - [x] add a tag to run pytest only on fast test when pre-commit
- [X] Implement a first grid generator
- [X] Use vscode and [devcontainer](https://www.youtube.com/watch?v=FvUpjdWnibo)

# Algorithmic improvements

- [ ] Properly implement multi solver to yield several (all) solutions
- [...] Algorithm X0

# Software engineering improvements

- [ ] Code coverage on CI (https://deusyss.developpez.com/tutoriels/Python/Coverage/)
- [ ] Graphical interface using pyqt
- [ ] Test the cli from an external program that can be shared for the different languages
- [ ] Use matrix in gitlab-ci to run with several python version
- [ ] Restrict python version in conda environment file
- [ ] Add an `install` target to avoid `export PYTHONPATH=~$(pwd):$PYTHONPATH`
- [ ] Improve usage of vscode (refactoring tricks, debugging, ...)
- [ ] Try other programming paradigm/library: FP, structured, ...

## Unit testing in python

- [ ] Proper doc string
- [ ] Try to use doc test
  - [ ] https://docs.python.org/3/library/doctest.html
  - [ ] https://stackoverflow.com/questions/67379623/doctest-multiple-files-from-one-file
- [ ] Try to use hypothesis

# Documentation and exposure

- [ ] Generate documentation page/website, e.g., using [github pages](https://pages.github.com/)
- [ ] Benchmark the different algorithms (solver, generation, ...)
- [ ] Implement more efficient solvers (and benchmark)
