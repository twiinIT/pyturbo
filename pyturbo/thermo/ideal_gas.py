# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import pythermo
from scipy.optimize import root, toms748


class IdealGas(pythermo.IdealGas):
    """Ideal gas model customized from `pythermo`."""

    def static_p(self, pt: float, tt: float, mach: float, tol: float) -> float:
        """Compute static pressure.

        pt[Pa]: float
            total pressure
        tt[K]: float
            total temperature
        mach[]: float
            Mach number
        tol[]: float
            numerical precision for iterative implementations
        """
        ts = self.static_t(tt, mach, tol)
        ps = pt * self.pr(tt, ts, 1.0)
        return ps

    def c(self, ts: float) -> float:
        """Speed of sound.

        ts[K]: float
            static temperature
        """
        return np.sqrt(self.gamma(ts) * self.r * ts)

    def density(self, ps: float, ts: float) -> float:
        """Density.

        ps[Pa]: float
            static pressure
        ts[K]: float
            static temperature
        """
        return ps / (self.r * ts)

    def wqa_crit(self, pt: float, tt: float, tol: float) -> float:
        """Critical specific mass flow.

        pt[Pa]: float
            total pressure
        tt[K]: float
            total temperature
        tol[]: float
            numerical precision
        """

        ts = self.static_t(tt, 1.0, tol)
        ps = pt * self.pr(tt, ts, 1.0)
        rho = self.density(ps, ts)
        c = self.c(ts)

        return rho * c

    def total_t(self, ts: float, mach: float) -> float:
        """Total temperature.

        ts[K]: float
            static temperature
        mach[]: float
            Mach number
        """
        return ts * (1.0 + 0.5 * (self.gamma(ts) - 1.0) * mach**2)

    def total_p(self, ps: float, ts: float, tt: float) -> float:
        """Total pressure.

        ps[Pa]: float
            static pressure
        tt[K]: float
            total temperature
        ts[K]: float
            static temperature
        """
        return ps * self.pr(ts, tt, 1.0)

    def mach_f_wqa(
        self, pt: float, tt: float, wqa: float, tol: float, subsonic: bool = True
    ) -> float:
        """Mach number.

        pt[Pa]: float
            total pressure
        tt[K]: float
            total temperature
        wqa[kg/s/m**2]: float
            specific mass flow
        tol[]: float
            numerical precision
        subsonic[]: bool
            whether to find the subsonic or supersonic solution
        """

        # TODO : remove when supersonic case will be handled by `pythermo`
        def f(mach):
            ts = self.static_t(tt, mach)
            ps = pt * self.pr(tt, ts, 1.0)
            return mach * self.c(ts) - wqa / self.density(ps, ts)

        try:
            if subsonic:
                m = toms748(f, 0.0, 1.0)
            else:
                m = toms748(f, 1.0, 10.0)
        except ValueError:
            m = 1.0

        return m

    def mach_f_ptpstt(self, pt: float, ps: float, tt: float, tol: float) -> float:
        """Mach number.

        pt[Pa]: float
            total pressure
        ps[Pa]: float
            static pressure
        tt[K]: float
            total temperature
        tol[]: float
            numerical precision
        """

        def f(mach):
            ts = self.static_t(tt, mach, tol)
            ps_it = pt * self.pr(tt, ts, 1.0)
            return ps - ps_it

        return root(f, 0.5).x[0]
