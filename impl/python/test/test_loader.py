import pytest
import numpy as np

def test_check_type_invalid():
    from sudoku.loader import check_type

    assert check_type(None) is False


def test_check_type_valid():
    from sudoku.loader import check_type

    assert check_type(np.ndarray(shape=(9, 9))) is True


def test_check_shape_valid():
    from sudoku.loader import check_shape

    assert check_shape(np.ndarray(shape=(9, 9))) is True


def test_check_shape_invalid():
    from sudoku.loader import check_shape

    assert check_shape(np.ndarray(shape=(8, 9))) is False
    assert check_shape(np.ndarray(shape=(9, 8))) is False
    assert check_shape(np.ndarray(shape=(8, 8))) is False


def test_check_range_value_invalid():
    from sudoku.loader import check_range_value

    array1 = np.ndarray(shape=(3, 3))
    array1.fill(-1)
    assert check_range_value(array1) is False
    array1.fill(10)
    assert check_range_value(array1) is False


def test_check_range_value_valid():
    from sudoku.loader import check_range_value
    
    array1 = np.ndarray(shape=(3, 3))
    array1.fill(0)
    assert check_range_value(array1) is True
    array1.fill(9)
    assert check_range_value(array1) is True
