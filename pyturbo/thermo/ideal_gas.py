# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from scipy.optimize import root, toms748


class IdealGas:
    """A simple model to compute thermodynamic properties for a generic gas.

    Limitations:
        - r constant
        - cp constant

    Parameters
    ----------
    r[J/kg/K]: float
        specific gas constant
    cp[J/kg/K]: float
        mass heat capacity
    """

    def __init__(self, r: float, cp: float):
        self._r = r
        self._cp = cp
        self._gamma = cp / (cp - r)

    @property
    def r(self):
        """Get the specific gas constant r.

        Outputs
        -------
        r[J/kg/K]: float
            specific gas constant
        """
        return self._r

    def cp(self, t):
        """Get the constant mass heat capacity cp.

        Outputs
        -------
        cp[J/kg/K]: float
            constant mass heat capacity
        """
        return self._cp

    def h(self, t):
        """Compute the enthalpy from the temperature.

        Inputs
        ----------
        t[K]: float
            temperature

        Outputs
        -------
        h[J/kg]: float
            Enthalpy
        """
        return self._cp * t

    def gamma(self, t):
        """Get the constant heat capacity ratio gamma.

        Outputs
        -------
        gamma[-]: float
            constant heat capacity ratio
        """
        return self._gamma

    def phi(self, t):
        return self._cp * np.log(t)

    def pr(self, t1, t2, eff_poly):
        """Compute the pressure ratio.

        Inputs
        ----------
        t1[K]: float
            temperature
        t2[K]: float
            temperature
        eff_poly[-]: float
            polytropic efficiency

        Outputs
        -------
        pr[-]: float
            pressure ratio
        """
        return np.exp(np.log(t2 / t1) * eff_poly * self._cp / self._r)

    def t_from_pr(self, pr, t1, eff_poly):
        """Compute the temperature raise due to polytropic compression.

        Inputs
        ----------
        pr[-]: float
            pressure ratio
        t1[K]: float
            temperature
        eff_poly[-]: float
            polytropic efficiency

        Outputs
        -------
        t[K]: float
            temperature
        """
        return t1 * np.power(pr, self._r / (self._cp * eff_poly))

    def eff_poly(self, p1, t1, p2, t2):
        """Compute the polytropic efficiency from pressures and temperatures.

        Inputs
        ----------
        p1[Pa]: float
            pressure
        t1[K]: float
            temperature
        p2[Pa]: float
            pressure
        t2[K]: float
            temperature

        Outputs
        -------
        eff_poly[-]: float
            polytropic efficiency
        """
        return self._r * np.log(p2 / p1) / (self.phi(t2) - self.phi(t1))

    def t_from_h(self, h):
        """Compute temperature from enthalpy.

        Inputs
        ----------
        h[J/kg]: float
            enthalpy

        Outputs
        -------
        t[K]: float
            temperature
        """
        return h / self._cp

    def static_t(self, tt, mach):
        """Compute static temperature from total temperature and mach.

        Inputs
        ----------
        tt[K]: float
            total temperature
        mach[-]: float
            mach number

        Outputs
        -------
        ts[K]: float
            static temperature
        """
        return tt / (1.0 + 0.5 * (self._gamma - 1.0) * mach**2)

    def total_t(self, ts, mach):
        """Compute total temperature from static temperature and mach.

        Inputs
        ----------
        ts[K]: float
            static temperature
        mach[-]: float
            mach number

        Outputs
        -------
        tt[K]: float
            total temperature
        """
        return ts * (1.0 + 0.5 * (self._gamma - 1.0) * mach**2)

    def static_p(self, pt, tt, mach):
        """Compute static pressure from total pressure, total temperature and mach.

        Inputs
        ----------
        pt[Pa]: float
            total pressure
        tt[K]: float
            total temperature
        mach[-]: float
            mach number

        Outputs
        -------
        ps[Pa]: float
            static pressure
        """
        ts = self.static_t(tt, mach)
        ps = pt * self.pr(tt, ts, 1.0)
        return ps

    def static_p_from_rhoV(self, pt, tt, rhoV, subsonic=True):
        """Compute static pressure from total pressure, total temperature and rho*V.

        Inputs
        ----------
        pt[Pa]: float
            total pressure
        tt[K]: float
            total temperature
        rhoV[kg/s/m**2]: float
            density times velocity
        subsonic: bool, default=True
            is the flow subsonic

        Outputs
        -------
        ps[Pa]: float
            static pressure
        """
        mach = self.mach(pt, tt, rhoV, subsonic)
        return self.static_p(pt, tt, mach)

    def total_p(self, ps, ts, tt):
        """Compute total pressure from static pressure, static temperature and total temperature.

        Inputs
        ----------
        ps[Pa]: float
            static pressure
        ts[K]: float
            static temperature
        tt[K]: float
            total temperature

        Outputs
        -------
        pt[Pa]: float
            total pressure
        """
        return ps * self.pr(ts, tt, 1.0)

    def mach(self, pt: float, tt: float, q: float, subsonic: bool = True) -> float:
        """Compute the mach number.

        Inputs
        ----------
        pt[Pa]: float
            total pressure
        tt[K]: float
            total temperature
        rho*V[kg/s/m**2]: float
            density times velocity
        subsonic: bool, default=True
            is the flow subsonic

        Outputs
        -------
        mach[-]: float
            mach number
        """

        def f(mach):
            ts = self.static_t(tt, mach)
            ps = pt * self.pr(tt, ts, 1.0)
            return mach * self.c(ts) - q / self.density(ps, ts)

        try:
            if subsonic:
                m = toms748(f, 0.0, 1.0)
            else:
                m = toms748(f, 1.0, 10.0)
        except ValueError:
            m = 1.0

        return m

    def mach_ptpstt(self, pt: float, ps: float, tt: float) -> float:
        """Compute the mach number from total pressure, static pressure and total temperature.

        Inputs
        ----------
        pt[Pa]: float
            total pressure
        ps[Pa]: float
            static temperature
        tt[K]: float
            total temperature

        Outputs
        -------
        mach[-]: float
            mach number
        """

        def f(mach):
            ts = self.static_t(tt, mach)
            ps_it = pt * self.pr(tt, ts, 1.0)
            return ps - ps_it

        return root(f, 0.5).x[0]

    def density(self, p, t):
        """Compute the gas density.

        Inputs
        ----------
        p[Pa]: float
            pressure
        t[K]: float
            temperature

        Outputs
        -------
        rho[kg/m**3]: float
            gas density
        """
        return p / (self._r * t)

    def c(self, t):
        """Compute the speed of sound.

        Inputs
        ----------
        t[K]: float
            temperature

        Outputs
        -------
        c[m/s]: float
            speed of sound
        """
        return np.sqrt(self._gamma * self._r * t)

    def Wqa_crit(self, pt, tt):
        t = self.static_t(tt, 1.0)
        p = pt * self.pr(tt, t, 1.0)
        rho = self.density(p, t)
        c = self.c(t)

        return rho * c


class IdealDryAir(IdealGas):
    """A simple model to compute thermodynamic properties for dry air.

    Limitations:
    - r constant, set to 287.058 J/kg/K
    - cp constant, set to 1004.0 J/kg/K
    - gamma is calculated from cp, yielding 1.4.
    """

    def __init__(self):
        super().__init__(r=287.058, cp=1004.0)
