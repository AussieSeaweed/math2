from math2.linalg.tensors import Matrix, Vector


def zeros(size: int) -> Vector:
    """Constructs a vector of size filled with zeros.

    :param size: The size of the vector.
    :return: The constructed vector.
    """
    return Vector(0 for _ in range(size))


def ones(size: int) -> Vector:
    """Constructs a vector of size filled with ones.

    :param size: The size of the vector.
    :return: The constructed vector.
    """
    return Vector(1 for _ in range(size))


def full(size: int, value: float) -> Vector:
    """Constructs a vector of size filled with the given value.

    :param size: The size of the vector.
    :param value: The fill value.
    :return: The constructed vector.
    """
    return Vector(value for _ in range(size))


def deleted(vec: Vector, index: int) -> Vector:
    """Returns the copied version of the supplied vector that has a value deleted.

    :param vec: The vector to delete.
    :param index: The index of deletion.
    :param value: The value to delete with.
    :return: The deleted vector.
    """
    vec = Vector(vec)
    del vec[index]

    return vec


def inserted(vec: Vector, index: int, value: float) -> Vector:
    """Returns the copied version of the supplied vector that has a value inserted.

    :param vec: The vector to insert.
    :param index: The index of insertion.
    :param value: The value to insert with.
    :return: The inserted vector.
    """
    vec = Vector(vec)
    vec.insert(index, value)

    return vec


def replaced(vec: Vector, index: int, value: float) -> Vector:
    """Returns the copied version of the supplied vector that has a value replaced.

    :param vec: The vector to replace.
    :param index: The index of replacement.
    :param value: The value to replace with.
    :return: The replaced vector.
    """
    vec = Vector(vec)
    vec[index] = value

    return vec


def transposed(mat: Matrix) -> Matrix:
    """Transposes the supplied matrix.

    :param mat: The matrix to transpose.
    :return: The transposed matrix.
    """
    return Matrix((mat[j][i] for j in range(len(mat[i]))) for i in range(len(mat)))
