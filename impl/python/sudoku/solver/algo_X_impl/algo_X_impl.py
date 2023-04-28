"""
Exact cover problem solver implemented using Donald Knuth's algorithm X

 - [Exact cover problem wikipedia page](https://en.wikipedia.org/wiki/Exact_cover)
 - [Knuth's Algorithm X wikipedia page](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X)

Exact cover problem description:

 - Given a set X
 - And given Y, a collection of subsets of X
 - a subcollection S is said to be an exact cover of X
 - if (and only if) each element in X is contained exactly in one subset of S


The wikipedia page for the algorithm X  describe the _dancing link_ (DLX) implementation.

This file uses the implementation described here: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
"""


def exact_coverage(X: set, Y: dict) -> list:
    X = invert_coverage(X, Y)

    for solutions in recursive_exact_coverage(X, Y, []):
        return solutions


def invert_coverage(X: set, Y: dict) -> dict:
    """
    Given a set X, and a dictionary Y key -> list[value] where each value belongs to X:

    Return a dictionnary mapping each element of X to the key link by Y

    >>> result = invert_coverage( X = {1, 2, 3, 4, 5} , Y = { "A": [1, 3, 5], "B": [1, 4] })
    {1: {'B', 'A'}, 2: set(), 3: {'A'}, 4: {'B'}, 5: {'A'}}

    https://en.wikipedia.org/wiki/Exact_cover
    """
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X


def select(X, Y, Ykey):
    subset = []
    for j in Y[Ykey]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        subset.append(X.pop(j))
    return subset


def deselect(X, Y, Ykey, subsets):
    for j in reversed(Y[Ykey]):
        X[j] = subsets.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)


def recursive_exact_coverage(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for candidate in list(X[c]):
            solution.append(candidate)
            cols = select(X, Y, candidate)
            for s in recursive_exact_coverage(X, Y, solution):
                yield s
            deselect(X, Y, candidate, cols)
            solution.pop()
