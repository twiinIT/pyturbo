import numpy as np


class IdealGas:

    def __init__(self, r: float, cp: float):
        self._r = r
        self._cp = cp
        self._gamma = cp / (cp - r)

    def r(self, t):
        return self._r

    def cp(self, t):
        return self._cp

    def h(self, t):
        return self._cp * t
    
    def gamma(self, t):
        return self._gamma

    def phi(self, t):
        return self._cp * np.log(t)

    def pr(self, t1, t2, eff_poly):
        return np.exp(np.log(t2 / t1) * eff_poly * self._cp / self._r)

    def eff_poly(self, p1, t1, p2, t2):
        return self._r * np.log(p2 / p1) / (self.phi(t2) - self.phi(t1))

    def t_from_h(self, h):
        return h / self._cp
