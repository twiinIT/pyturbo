# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np


class SimplifiedMftCompressor:
    """Define a simplified MFT compressor."""

    Pstd = 101325.0
    Tstd = 288.15

    def __init__(self):
        self._phi = 1.0
        self._psi = 1.0
        self._utrd = 400.0
        self._inlet_area = 1.0

        self._gls_bb = 0.02
        self._gls_l = 0.05
        self._gls_r = 0.1
        self._vqu_sat = 0.5
        self._gh_vqu_sat = -0.1
        self._vqu_slope = 0.1
        self._kshape = 1.0
        self._exps = 2.0
        self._gh_wr_null = 1.0

        self._gamma = 1.4
        self._r = 287.05
        self._cp = 1004.0

    def wr(self, pcnr, gh):
        vlsl = self.velocity(gh) * self._utrd * pcnr / 100.0
        wr = (
            self._inlet_area
            * (self.Pstd / (self.Tstd * self._r))
            * vlsl
            * (1 - vlsl**2 / (2 * self._cp * self.Tstd)) ** (1 / (self._gamma - 1))
        )

        return wr

    def pr(self, pcnr, gh):
        ghri = self._psi + gh - self.loss(gh)
        tqi = (self._utrd * pcnr / 100) ** 2 * ghri / (2.0 * self._cp * self.Tstd) + 1.0
        return tqi ** (self._gamma / (self._gamma - 1.0))

    def eff_is(self, pcnr, gh):
        ghr = self._psi + gh
        ghri = ghr - self.loss(gh)
        return ghri / ghr

    def offbackbone_loss(self, gh):
        if gh > 0.0:
            return self._gls_r * gh**2
        else:
            return self._gls_l * gh**2

    def loss(self, gh):
        return self._gls_bb + self.offbackbone_loss(gh)

    def velocity(self, gh):
        if gh < self._gh_vqu_sat:
            return self._vqu_sat
        else:
            x = (gh - self._gh_vqu_sat) / (self._gh_wr_null - self._gh_vqu_sat)
            return self._vqu_sat * (
                1.0 - np.log((np.exp(self._kshape) - 1.0) * x**self._exps + 1) / self._kshape
            )

    def ghr(self, gh):
        return self._psi + gh
