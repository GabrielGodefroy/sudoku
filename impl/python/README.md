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

Launch unit tests:

```
python -m pytest . # why not just pytest?
```

Run coverage:
```
coverage run -m pytest
coverage report -m
```