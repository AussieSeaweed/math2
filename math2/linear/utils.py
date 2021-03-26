from math2.linear.factories import vector
from math2.linear.tensors import Tensor

i = vector((1, 0, 0))
j = vector((0, 1, 0))
k = vector((0, 0, 1))


def norm(t: Tensor, p: float = 2) -> float:
    return sum(s ** p for s in t) ** (1 / p)
