# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.ports.fluidport import FluidPort
from pyturbo.thermo.ideal_gas import IdealDryAir


class Atmosphere(System):
    """Atmosphere

    Provide fluid port characteristics from altitude, mach speed and
    delta ISA temperature.
    """

    def setup(self):
        self.add_inward("gas", IdealDryAir())

        self.add_property("t0", 288.15)
        self.add_property("p0", 101325.0)

        # inward/outward
        self.add_inward("altitude", 10000, unit="m", desc="altitude in m")
        self.add_inward("mach", 0.8, unit="", desc="mach speed")
        self.add_inward("dtamb", 0.0, unit="K", desc="ambient temperature delta")
        self.add_outward("ps", 1.0, unit="pa", desc="static pressure")
        self.add_outward("ts", 1.0, unit="K", desc="static temperature")

        # inputs/outputs
        self.add_output(FluidPort, "fl_out")

        # off design
        self.add_inward("W", 1.0, unit="kg/s", desc="air mass flow")
        self.add_unknown("W", max_rel_step=0.5)

    def compute(self):
        h = self.altitude

        self.ts = self.t0 * (1.0 - 0.000022558 * self.altitude) + self.dtamb
        self.ps = self.p0 * (1 - 0.0065 * h / (self.t0 - 15.0)) ** 5.2561

        self.fl_out.W = self.W
        self.fl_out.Tt = self.gas.total_t(self.ts, self.mach)
        self.fl_out.pt = self.gas.total_p(self.ps, self.ts, self.fl_out.Tt)
