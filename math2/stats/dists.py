from abc import ABC, abstractmethod
from collections.abc import Callable
from math import comb, exp, factorial, inf, pi, sqrt

from scipy.integrate import quad


class Distribution(Callable, ABC):
    @property
    @abstractmethod
    def mean(self):
        pass

    @property
    @abstractmethod
    def variance(self):
        pass

    @abstractmethod
    def cum(self, x):
        pass

    @abstractmethod
    def __call__(self, x):
        pass


class DiscreteDistribution(Distribution, ABC):
    def cum(self, x):
        return sum(self(i) for i in range(x + 1))


class BinomialDistribution(DiscreteDistribution):
    def __init__(self, n, p):
        self.n = n
        self.p = p

    @property
    def q(self):
        return 1 - self.p

    @property
    def mean(self):
        return self.n * self.p

    @property
    def variance(self):
        return self.n * self.p * self.q

    def __call__(self, x):
        return comb(self.n, x) * self.p ** x * self.q ** (self.n - x)


class HypergeometricDistribution(DiscreteDistribution):
    def __init__(self, N, n, k):
        self.N = N
        self.n = n
        self.k = k

    @property
    def mean(self):
        return self.n * self.k / self.N

    @property
    def variance(self):
        return (self.N - self.n) / (self.N - 1) * self.n * self.k / self.N * (1 - self.k / self.N)

    def __call__(self, x):
        return comb(self.n, x) * comb(self.N - self.n, self.k - x) / comb(self.N, self.k)


class NegativeBinomialDistribution(DiscreteDistribution):
    def __init__(self, k, p):
        self.k = k
        self.p = p

    @property
    def q(self):
        return 1 - self.p

    @property
    def mean(self):
        raise NotImplementedError

    @property
    def variance(self):
        raise NotImplementedError

    def __call__(self, x):
        return comb(x - 1, self.k - 1) * self.p ** self.k * self.q ** (x - self.k)


class GeometricDistribution(DiscreteDistribution):
    def __init__(self, p):
        self.p = p

    @property
    def q(self):
        return 1 - self.p

    @property
    def mean(self):
        return 1 / self.p

    @property
    def variance(self):
        return (1 - self.p) / self.p ** 2

    def __call__(self, x):
        return self.p * self.q ** (x - 1)


class PoissonDistribution(DiscreteDistribution):
    def __init__(self, lt):
        self.lt = lt

    @property
    def mean(self):
        return self.lt

    @property
    def variance(self):
        return self.lt

    def __call__(self, x):
        return exp(-self.lt) * self.lt ** x / factorial(x)


class ContinuousDistribution(Distribution, ABC):
    def cum(self, x):
        return quad(self, -inf, x)


class UniformDistribution(ContinuousDistribution):
    def __init__(self, A, B):
        self.A = A
        self.B = B

    @property
    def mean(self):
        return (self.A + self.B) / 2

    @property
    def variance(self):
        return (self.B - self.A) ** 2 / 12

    def __call__(self, x):
        return 1 / (self.B - self.A) if self.A <= x <= self.B else 0


class NormalDistribution(ContinuousDistribution):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    @property
    def mean(self):
        return self.mu

    @property
    def variance(self):
        return self.sigma ** 2

    def standardize(self, x):
        return (x - self.mu) / self.sigma

    def destandardize(self, z):
        return self.sigma * z + self.mu

    def __call__(self, x):
        return exp(-(x - self.mu) ** 2 / (2 * self.sigma ** 2)) / (sqrt(2 * pi) * self.sigma)


class StandardNormalDistribution(ContinuousDistribution):
    @property
    def mean(self):
        return 0

    @property
    def variance(self):
        return 1

    def __call__(self, x):
        return exp(-x ** 2 / 2) / sqrt(2 * pi)
