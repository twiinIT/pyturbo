# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from pyturbo.thermo.ideal_gas import IdealDryAir, IdealGas


class TestIdealGas:
    gas = IdealGas(r=287.058, cp=1004.0)

    t1 = 100.0
    t2 = 200.0
    p1 = 100000.0
    eff = 0.5
    cp = gas.cp(t1)
    r = gas.r
    pr = gas.pr(t1, t2, eff)

    def test_r(self):
        assert self.r == 287.058

    def test_cp(self):
        assert self.cp == 1004.0

    def test_h(self):
        assert self.gas.h(self.t1) == self.cp * self.t1

    def test_gamma(self):
        assert self.gas.gamma(self.t1) == self.cp / (self.cp - self.r)

    def test_phi(self):
        assert self.gas.phi(self.t1) == self.cp * np.log(self.t1)

    def test_pr(self):
        assert abs(self.pr - (self.t2 / self.t1) ** (self.eff * self.cp / self.r)) < 1e-6

    def test_t_from_pr(self):
        assert self.gas.t_from_pr(self.pr, self.t1, self.eff) == self.t2

    def test_t_from_h(self):
        assert self.gas.t_from_h(self.cp * self.t1) == self.t1

    def test_density(self):
        assert self.gas.density(self.p1, self.t1) == self.p1 / (self.r * self.t1)

    def test_c(self):
        assert self.gas.c(self.t1) == np.sqrt(self.gas.gamma(self.t1) * self.r * self.t1)

    def test_eff_poly(self):
        assert (
            abs(self.gas.eff_poly(self.p1, self.t1, self.p1 * self.pr, self.t2) - self.eff) < 1e-6
        )


class TestDryAir:
    gas = IdealGas(r=287.058, cp=1004.0)
    air = IdealDryAir()

    def test_cp(self):
        assert self.gas.cp(100.0) == self.air.cp(100.0)

    def test_gamma(self):
        assert self.gas.gamma(100.0) == self.air.gamma(100.0)

    def test_r(self):
        assert self.gas.r == self.air.r
