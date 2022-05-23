# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from scipy.optimize import root, toms748


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
        return tt / (1.0 + 0.5 * (self._gamma - 1.0) * mach**2)

    def total_t(self, ts, mach):
        return ts * (1.0 + 0.5 * (self._gamma - 1.0) * mach**2)

    def static_p(self, pt, tt, mach):
        ts = self.static_t(tt, mach)
        ps = pt * self.pr(tt, ts, 1.0)
        return ps

    def static_p_from_rhoV(self, pt, tt, rhoV, subsonic=True):
        mach = self.mach(pt, tt, rhoV, subsonic)
        return self.static_p(pt, tt, mach)

    def total_p(self, ps, ts, tt):
        return ps * self.pr(ts, tt, 1.0)

    def mach(self, pt: float, tt: float, q: float, subsonic: bool = True) -> float:
        def f(mach):
            ts = self.static_t(tt, mach)
            ps = pt * self.pr(tt, ts, 1.0)
            return mach * self.c(ts) - q / self.density(ps, ts)

        if subsonic:
            m = toms748(f, 0.0, 1.0)
        else:
            m = toms748(f, 1.0, 10.0)
        return m

    def mach_ptpstt(self, pt: float, ps: float, tt: float) -> float:
        def f(mach):
            ts = self.static_t(tt, mach)
            ps_it = pt * self.pr(tt, ts, 1.0)
            return ps - ps_it

        return root(f, 0.5).x[0]

    def density(self, p, t):
        return p / (self._r * t)

    def c(self, t):
        return np.sqrt(self._gamma * self._r * t)


class IdealDryAir(IdealGas):
    def __init__(self):
        super().__init__(r=287.058, cp=1004.0)
