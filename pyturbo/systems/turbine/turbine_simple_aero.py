# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from math import sqrt

import numpy as np
from cosapp.systems import System
from scipy.optimize import root

from pyturbo.ports import FluidPort, ShaftPort
from pyturbo.thermo.ideal_gas import IdealGas


class TurbineSimpleAero(System):
    """
    A simple aerodynamic gas turbine model.

    It computes the exit gas `fl_out` from inlet gas `fl_in` for a given pressure ratio
    and efficency. The generated power `shaft_out.power` is also computed.
    """

    def setup(self):
        # inputs/outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")
        self.add_output(ShaftPort, "shaft_out")

        # inwards
        self.add_inward("eff_poly", 0.9, desc="polytropic efficiency")
        self.add_inward("er", 5.0, desc="expansion ratio")
        self.add_inward("Ncdes", 150.0, desc="design corrected speed")
        self.add_inward("Ncqdes", 100.0, desc="corrected speed over design value ratio")
        self.add_inward("gas", IdealGas(287.058, 1004.0))

        self.add_inward("area_in", 1.0, unit="m**2", desc="inlet area")
        self.add_inward("mean_radius", 1.0, unit="m", desc="mean radius")
        self.add_inward("stage_count", 1, unit="", desc="stage count")
        # outwards
        self.add_outward("Wc", unit="kg/s", desc="corrected mass flow")
        self.add_outward("Tt_ratio", desc="total temperature ratio")
        self.add_outward("Mach_in", desc="inlet Mach number")
        self.add_outward("psi", desc="aerodynamic loading")
        self.add_outward("sf1", desc="")
        self.add_outward("sf2", desc="")

        # design method
        self.add_design_method("temperature").add_target("fl_in.Tt")
        self.add_design_method("speed").add_unknown("Ncdes", lower_bound=0.0)

    def compute(self):
        # fluid
        self.fl_out.W = self.fl_in.W
        self.fl_out.pt = self.fl_in.pt / self.er
        self.fl_out.Tt = self.gas.t_from_pr(1.0 / self.er, self.fl_in.Tt, self.eff_poly)
        self.Tt_ratio = self.fl_out.Tt / self.fl_in.Tt

        # shaft
        N = self.Ncqdes * self.Ncdes / 100.0 * self.fl_in.Tt**0.5
        self.shaft_out.N = N * 30.0 / np.pi
        dh = self.gas.h(self.fl_in.Tt) - self.gas.h(self.fl_out.Tt)
        self.shaft_out.power = self.fl_in.W * dh

        # inlet Mach number
        def Mach_solver(mach):
            t = self.gas.static_t(self.fl_in.Tt, mach)
            p = self.gas.pr(self.fl_in.Tt, t, 1.0) * self.fl_in.pt
            rho = self.gas.density(p, t)
            vm = self.fl_in.W / (rho * self.area_in)
            return mach - vm / self.gas.c(t)

        self.Mach_in = root(Mach_solver, 0.5).x

        self.sf1 = (
            self.fl_in.W * sqrt(self.fl_in.Tt / 288.15) / (self.fl_in.pt / 101325.0) / self.area_in
        )

        u = self.mean_radius * N
        self.psi = dh / (2.0 * self.stage_count * u**2)

        # outwards
        self.Wc = self.fl_in.W * np.sqrt(self.fl_in.Tt / 288.15) / (self.fl_in.pt / 101325.0)
