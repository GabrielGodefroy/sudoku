import pytest
import numpy as np

from sudoku.grid import (
    get_neighboorhood_indices,
    get_neighboorhood_values,
    get_candidate_values,
)


def test_neighboorhood_raise():
    with pytest.raises(IndexError):
        get_neighboorhood_indices(-1, 0)
    with pytest.raises(IndexError):
        get_neighboorhood_indices(9, 0)


def test_neighboorhood_0_0():
    assert get_neighboorhood_indices(0, 0) == [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7),
        (0, 8),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 0),
        (7, 0),
        (8, 0),
    ]


def test_neighboorhood_1_0():
    assert get_neighboorhood_indices(1, 0) == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (2, 0),
        (2, 1),
        (2, 2),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 0),
        (7, 0),
        (8, 0),
    ]


def test_neighboorhood_4_4():
    assert get_neighboorhood_indices(4, 4) == [
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 5),
        (4, 6),
        (4, 7),
        (4, 8),
        (5, 3),
        (5, 4),
        (5, 5),
        (6, 4),
        (7, 4),
        (8, 4),
    ]


def test_get_neighboorhood_values_empty_grid():
    array = np.ndarray(shape=(9, 9))
    array.fill(0)
    assert get_neighboorhood_values(1, 1, array) == list()
    assert get_neighboorhood_values(0, 1, array) == list()
    assert get_neighboorhood_values(1, 8, array) == list()
    assert get_neighboorhood_values(8, 8, array) == list()


def test_get_neighboorhood_values_non_empty_grid():
    array = np.ndarray(shape=(9, 9))
    array[0, 0] = 0
    array[1, 1] = 1
    array[2, 2] = 2
    array[0, 8] = 8
    array[8, 0] = 7
    assert sorted(get_neighboorhood_values(0, 0, array)) == [1, 2, 7, 8]
    assert sorted(get_neighboorhood_values(1, 1, array)) == [2]
    assert sorted(get_neighboorhood_values(1, 8, array)) == [1, 8]
    assert sorted(get_neighboorhood_values(8, 1, array)) == [1, 7]


def test_get_candidate_values_on_empty_grid():
    clues = np.ndarray(shape=(9, 9))
    clues.fill(0)
    assert sorted(get_candidate_values(0, 0, clues)) == [i for i in range(1, 10)]
    assert sorted(get_candidate_values(1, 5, clues)) == [i for i in range(1, 10)]
    assert sorted(get_candidate_values(8, 8, clues)) == [i for i in range(1, 10)]


def test_get_candidate_values_on_non_empty_grid():
    array = np.ndarray(shape=(9, 9))
    array[0, 0] = 0
    array[1, 1] = 1
    array[2, 2] = 2
    array[0, 8] = 8
    array[8, 0] = 7
    assert sorted(get_candidate_values(0, 0, array)) == [3, 4, 5, 6, 9]
    assert sorted(get_candidate_values(1, 1, array)) == [1, 3, 4, 5, 6, 7, 8, 9]
    assert sorted(get_candidate_values(1, 8, array)) == [2, 3, 4, 5, 6, 7, 9]
    assert sorted(get_candidate_values(8, 1, array)) == [2, 3, 4, 5, 6, 8, 9]
