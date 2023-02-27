# Python


 - __python version__: 3.11
 - __package manager__: `conda`
 - __unit tests__: `pytest`


## User guide

Start conda:

```
conda env create -f environment.yaml
conda activate sudoku
```

Update conda environment (https://stackoverflow.com/questions/42352841/)
```
conda env update --name sudoku --file environment.yml --prune
conda env update --file environment.yml --prune

```

Launch unit tests:

```
python -m pytest . # why not just pytest?
```

Run coverage:
```
coverage run -m pytest
coverage report -m
```

Use flake8:
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=10 --max-line-length=120 --statistics
```
