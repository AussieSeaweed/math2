from abc import ABC


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    @property
    def endpoints(self):
        return self.u, self.v

    def other(self, vertex):
        if vertex is self.u:
            return self.v
        elif vertex is self.v:
            return self.u
        else:
            raise ValueError('The vertex is not one of the endpoints')


class WeightedMixin(ABC):
    weight = None


class FlowMixin(ABC):
    flow = None
    capacity = None


class WeightedEdge(Edge, WeightedMixin):
    def __init__(self, u, v, weight):
        super().__init__(u, v)

        self.weight = weight


class FlowEdge(Edge, FlowMixin):
    def __init__(self, u, v, flow, capacity):
        super().__init__(u, v)

        self.flow = flow
        self.capacity = capacity


class WeightedFlowEdge(Edge, WeightedMixin, FlowMixin):
    def __init__(self, u, v, weight, flow, capacity):
        super().__init__(u, v)

        self.weight = weight
        self.flow = flow
        self.capacity = capacity
