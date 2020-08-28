.. Sudoku documentation master file, created by
   sphinx-quickstart on Thu Aug 27 15:11:08 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Sudoku's documentation!
==================================

A Python module that solve a sudoku puzzle using the backtracking algorithm.

A dummy version of the backtracking algorithm is explained in the following video:
 
 * https://www.youtube.com/watch?v=G_UYXzGuqvM

 However, this dummy implementation tends to be slow. 
 Several heuristics can be used to speed up the resolution.

 I used the two heuristics described here: http://sdz.tdct.org/sdz/le-backtracking-par-l-exemple-resoudre-un-sudoku.html

First, I precompute the possible solutions for each empty (Solver._init_possibility())
Second, I change the traversal order to start with the (Solver._init_order())

.. toctree::
   :maxdepth: 2
   :caption: List of the main files:

   module



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



