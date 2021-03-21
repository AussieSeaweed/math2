from math2.linalg.matrices import Matrix


def singleton(scalar):
    return Matrix(((scalar,),))


def row(vector):
    return Matrix((vector,))


def column(vector):
    return Matrix((scalar,) for scalar in vector)


def transposed(matrix):
    return Matrix(matrix.columns)


i = row((1, 0, 0))
j = row((0, 1, 0))
k = row((0, 0, 1))
