# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from math import sqrt

from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo.ideal_gas import IdealGas


class NozzleSimpleAero(System):
    """A simple nozzle aerodynamic model.

    It computes the gross thrust from the inlet flow and ambient static
    pressure assuming a choked throat=exit area (convergent nozzle).
    """

    def setup(self):
        # inputs / outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # inwards/outwards
        self.add_inward("gas", IdealGas(287.058, 1004.0))
        self.add_inward("area", 1.0, unit="m**2", desc="choked/exit area")
        self.add_inward("pamb", 101325.0, unit="Pa", desc="ambient static pressure")
        self.add_outward("thrust", unit="N")

        # solver
        self.add_equation("fl_in.W == fl_out.W")

    def compute(self):
        gamma = self.gas.gamma(self.fl_in.Tt)
        r = self.gas.r

        tr = (self.fl_in.pt / self.pamb) ** ((gamma - 1) / gamma)
        mach_throat = sqrt((tr - 1.0) * (2 / (gamma - 1)))

        if mach_throat > 1:
            mach_throat = 1.0
            tr = (gamma + 1.0) / 2.0

        ts = self.fl_in.Tt / tr
        v = mach_throat * sqrt(gamma * r * ts)
        ps = self.fl_in.pt * tr ** (-gamma / (gamma - 1.0))

        self.fl_out.W = self.gas.density(ps, ts) * v * self.area
        self.fl_out.Tt = self.fl_in.Tt
        self.thrust = self.fl_in.W * v + (ps - self.pamb) * self.area
