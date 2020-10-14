import pytest
import numpy as np

from sudoku.loader import load_from_text_file

DIM = 9

def test_empty():
    """ Load an empty sudoku """
    result = load_from_text_file("../DATA/empty.txt")
    assert (result == np.zeros((DIM,DIM), dtype=int)).all()

def test_ones():
    result = load_from_text_file("../DATA/ones.txt", check_validity=False)
    """ Load ones only """
    assert (result == np.ones((DIM,DIM), dtype=int)).all() 

def test_diag_ones():
    """ Load identity matrix """
    result = load_from_text_file("../DATA/diag-ones.txt", check_validity=False)
    assert (result == np.diag(np.ones(DIM,dtype=int))).all() 

def test_diag():
    """ Load a diagonal matrix """
    result = load_from_text_file("../DATA/diag.txt")
    assert (result == np.diag([e for e in range(1,DIM+1)])).all() 

def test_number():
    """ 8.5 should throw an error """
    try:
        load_from_text_file("../DATA/invalidNumber.txt")
    except : 
        return 
    assert(False) # should not be reached

def test_number2():
    """ 10 should throw an error """
    try:
        load_from_text_file("../DATA/invalidNumber2.txt")
    except : 
        return 
    assert(False) # should not be reached

def test_size():
    """ Wrong size should throw an error """
    def _test_size(filepath):
        try:
            load_from_text_file(filepath)
        except : 
            return 
        assert(False) # should not be reached

    _test_size("../DATA/invalidSize.txt")
    _test_size("../DATA/invalidSize2.txt")
    _test_size("../DATA/invalidSize3.txt")