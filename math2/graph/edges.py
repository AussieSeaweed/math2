from abc import ABC
from typing import Generic

from math2.typing import _H, _S


class Edge(Generic[_H]):
    def __init__(self, u: _H, v: _H):
        self.u = u
        self.v = v

    @property
    def endpoints(self) -> tuple[_H, _H]:
        return self.u, self.v

    def other(self, vertex: _H) -> _H:
        if vertex is self.u:
            return self.v
        elif vertex is self.v:
            return self.u
        else:
            raise ValueError('The vertex is not one of the endpoints')


class WeightedMixin(Generic[_S], ABC):
    weight: _S


class FlowMixin(Generic[_S], ABC):
    flow: _S
    capacity: _S


class WeightedEdge(Edge[_H], WeightedMixin[_S]):
    def __init__(self, u: _H, v: _H, weight: _S):
        super().__init__(u, v)

        self.weight = weight


class FlowEdge(Edge[_H], FlowMixin[_S]):
    def __init__(self, u: _H, v: _H, flow: _S, capacity: _S):
        super().__init__(u, v)

        self.flow = flow
        self.capacity = capacity


class WeightedFlowEdge(Edge[_H], WeightedMixin[_S], FlowMixin[_S]):
    def __init__(self, u: _H, v: _H, weight: _S, flow: _S, capacity: _S):
        super().__init__(u, v)

        self.weight = weight
        self.flow = flow
        self.capacity = capacity
