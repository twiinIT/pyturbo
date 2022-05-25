# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo.ideal_gas import IdealGas


class InletSimpleAero(System):
    """A simple inlet aerodynamic model.

    The pressure loss is constant. The Mach number is iterated
    to converge the exit mass flow rate on the inlet one.

    The `sizing` design method defines the throat section
    to achieve a given Mach number.
    """

    def setup(self):
        # inputs / outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # inwards/outwards
        self.add_inward("gas", IdealGas(287.058, 1004.0))
        self.add_inward("p_loss", 1.0, unit="", desc="constant pressure loss coefficient")
        self.add_inward("throat_section", 1.0, unit="m**2", desc="throat section")
        self.add_inward("throat_Mach", 0.5, unit="", desc="throat Mach number")

        # solver
        self.add_equation("fl_in.W == fl_out.W").add_unknown("throat_Mach")
        self.add_design_method("sizing").add_target("throat_Mach").add_unknown("throat_section")

    def compute(self):
        self.fl_out.Tt = self.fl_in.Tt
        self.fl_out.pt = self.fl_in.pt * self.p_loss

        t = self.gas.static_t(self.fl_in.Tt, self.throat_Mach)
        pr = self.gas.pr(self.fl_in.Tt, t, 1.0)
        p = self.fl_out.pt * pr
        v = self.throat_Mach * self.gas.c(t)

        self.fl_out.W = self.gas.density(p, t) * v * self.throat_section
