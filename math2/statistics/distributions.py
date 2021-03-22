from abc import ABC, abstractmethod
from collections.abc import Callable
from math import comb, exp, factorial, gamma, inf, pi, sqrt

from scipy.integrate import quad


class Distribution(Callable, ABC):
    @property
    def standard_deviation(self):
        return sqrt(self.variance)

    @property
    @abstractmethod
    def mean(self):
        pass

    @property
    @abstractmethod
    def variance(self):
        pass

    @abstractmethod
    def cumulative(self, x):
        pass

    @abstractmethod
    def density(self, x):
        pass


class DiscreteDistribution(Distribution, ABC):
    def cumulative(self, x):
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

    def to_poisson(self):
        return PoissonDistribution(self.n * self.p)

    def to_normal(self):
        return NormalDistribution(self.mean, self.standard_deviation)

    def density(self, x):
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

    def density(self, x):
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

    def density(self, x):
        return comb(x - 1, self.k - 1) * self.p ** self.k * self.q ** (x - self.k)


class GeometricDistribution(NegativeBinomialDistribution):
    def __init__(self, p):
        super().__init__(1, p)

    @property
    def mean(self):
        return 1 / self.p

    @property
    def variance(self):
        return (1 - self.p) / self.p ** 2

    def density(self, x):
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

    def density(self, x):
        return exp(-self.lt) * self.lt ** x / factorial(x)


class ContinuousDistribution(Distribution, ABC):
    def cumulative(self, x):
        return quad(self, -inf, x)[0]


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

    def cumulative(self, x):
        if x < self.A:
            return 0
        elif self.B < x:
            return 1
        else:
            return (x - self.A) / (self.B - self.A)

    def density(self, x):
        return 1 / (self.B - self.A) if self.A <= x <= self.B else 0


class NormalDistribution(ContinuousDistribution):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    @property
    def standard_deviation(self):
        return self.sigma

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

    def density(self, x):
        return exp(-(x - self.mu) ** 2 / (2 * self.sigma ** 2)) / (sqrt(2 * pi) * self.sigma)


class StandardNormalDistribution(NormalDistribution):
    def __init__(self):
        super().__init__(0, 1)

    def density(self, x):
        return exp(-x ** 2 / 2) / sqrt(2 * pi)


class GammaDistribution(ContinuousDistribution):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def mean(self):
        return self.a * self.b

    @property
    def variance(self):
        return self.a * self.b ** 2

    def density(self, x):
        return x ** (self.a - 1) * exp(-x / self.b) / (self.b ** self.a * gamma(self.a)) if x > 0 else 0


class ExponentialDistribution(GammaDistribution):
    def __init__(self, b):
        super().__init__(1, b)

    @property
    def standard_deviation(self):
        return self.b

    @property
    def mean(self):
        return self.b

    @property
    def variance(self):
        return self.b ** 2

    def density(self, x):
        return exp(-x / self.b) / self.b if x > 0 else 0


class ChiSquaredDistribution(GammaDistribution):
    def __init__(self, v):
        super().__init__(self.v / 2, 2)

        self.v = v

    @property
    def mean(self):
        return self.v

    @property
    def variance(self):
        return 2 * self.v

    def density(self, x):
        return x ** (self.v / 2 - 1) * exp(-x / 2) / (2 ** (self.v / 2) * gamma(self.v / 2)) if x > 0 else 0


class WeibullDistribution(ContinuousDistribution):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def mean(self):
        return self.a ** (-1 / self.b) * gamma(1 + 1 / self.b)

    @property
    def variance(self):
        return self.a ** (-2 / self.b) * (gamma(1 + 2 / self.b) - gamma(1 + 1 / self.b) ** 2)

    def failure_rate(self, t):
        if t > 0:
            return self.a * self.b * t ** (self.b - 1)
        else:
            raise ValueError(f'{t} not in domain')

    def cumulative(self, x):
        return 1 - exp(-self.a * x ** self.b)

    def density(self, x):
        return self.a * self.b * x ** (self.b - 1) * exp(-self.a * x ** self.b) if x > 0 else 0
