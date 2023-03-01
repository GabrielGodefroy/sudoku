"""
Algorithm X modified from https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
"""


def exact_cover(X: set, Y: dict) -> dict:
    """

    TODO find a better name

    Given a set X, and a dictionary Y key -> list[value] where each value belongs to X:

    Return a dictionnary mapping each element of X to the key link by Y

    >>> result = exact_cover( X = {1, 2, 3, 4, 5} , Y = { "A": [1, 3, 5], "B": [1, 4] })
    {1: {'B', 'A'}, 2: set(), 3: {'A'}, 4: {'B'}, 5: {'A'}}

    https://en.wikipedia.org/wiki/Exact_cover
    """
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X
