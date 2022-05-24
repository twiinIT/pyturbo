import numpy as np


class IdealGas:
    def __init__(self, r: float, cp: float):
        self._r = r
        self._cp = cp
        self._gamma = cp / (cp - r)

    @property
    def r(self):
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

    def t_from_pr(self, pr, t1, eff_poly):
        return t1 * np.power(pr, self._r / (self._cp * eff_poly))

    def eff_poly(self, p1, t1, p2, t2):
        return self._r * np.log(p2 / p1) / (self.phi(t2) - self.phi(t1))

    def t_from_h(self, h):
        return h / self._cp

    def static_t(self, tt, mach):
        return tt / (1.0 + 0.5 * (self._cp / (self._cp - self._r) - 1.0) * mach**2)

    def total_t(self, ts, mach):
        return ts * (1.0 + 0.5 * (self._cp / (self._cp - self._r) - 1.0) * mach**2)

    def total_p(self, ps, ts, tt):
        return ps * self.pr(ts, tt, 1.0)

    def density(self, p, t):
        return p / (self._r * t)

    def c(self, t):
        return np.sqrt(self._gamma * self._r * t)


class IdealDryAir(IdealGas):
    def __init__(self):
        super().__init__(r=287.058, cp=1004.0)
