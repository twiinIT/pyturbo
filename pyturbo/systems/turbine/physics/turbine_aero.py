# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.ports import FluidPort, ShaftPort
from pyturbo.thermo import IdealDryAir


class TurbineAero(System):
    """A simple aerodynamic gas turbine model.

    It computes the exit gas `fl_out` from inlet gas `fl_in` for a given pressure ratio
    and efficency. The generated power `sh_out.power` is also computed.

    Parameters
    ----------
    FluidLaw: Class, default=IdealDryAir
        Class providing gas characteristics

    Inputs
    ------
    fl_in: FluidPort
        inlet gas

    eff_poly[-]: float, default=0.9
        polytropic efficiency
    er[-]: float, default=5.0
        expansion ratio
    Ncdes[%]: float, default=150.0
        design corrected speed
    Ncqdes[rpm/K**0.5]: float, default=100.0
        corrected speed over design value ratio

    stage_count: int, default=1
        number of stages
    area_in[m**2]: float, default=1.0
        inlet area
    mean_radius[m]: float, default=1.0
        mean radius

    Outputs
    -------
    fl_out: FluidPort
        fluid leaving the compressor
    sh_out: ShaftPort
        shaft

    Wc[kg/s]: float
        corrected mass flow
    Tt_ratio[-]: float
        total temperature ratio
    psi[-]: float
        aerodynamic loading by stage

    Design methods
    --------------
    off design:
        Ncqdes unknown
    """

    def setup(self, FluidLaw=IdealDryAir):
        # properties
        self.add_inward("gas", FluidLaw())

        # inputs/outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")
        self.add_output(ShaftPort, "sh_out")

        # inwards
        self.add_inward("eff_poly", 0.9, unit="", desc="polytropic efficiency")
        self.add_inward("dhqt", 400.0, unit="", desc="enthalpy delta over inlet temperature")
        self.add_inward("Ncdes", 150.0, unit="rpm/K", desc="design corrected speed")
        self.add_inward("Ncqdes", 100.0, unit="", desc="corrected speed over design value ratio")

        self.add_inward("area_in", 1.0, unit="m**2", desc="inlet area")
        self.add_inward("blokage", 4.0, unit="", desc="aero blokage factor")
        self.add_inward("mean_radius", 1.0, unit="m", desc="mean radius")
        self.add_inward("stage_count", 1, unit="", desc="stage count")

        # outwards
        self.add_outward("Wc", unit="kg/s", desc="inlet corrected mass flow")
        self.add_outward("Wcrit", unit="kg/s", desc="critical inlet corrected mass flow")
        self.add_outward("Tt_ratio", 0.6, unit="", desc="total temperature ratio")
        self.add_outward("psi", unit="", desc="aerodynamic loading")

        # off design
        self.add_unknown("Ncqdes", max_rel_step=0.5)
        self.add_unknown("dhqt", max_rel_step=0.8)
        self.add_unknown("fl_in.W")
        self.add_equation("fl_in.W == Wcrit")

        off_design = self.add_design_method("off_design_standalone")
        off_design.add_target("sh_out.N")
        off_design.add_target("sh_out.power")

    def compute(self):
        # fluid
        self.fl_out.W = self.fl_in.W
        dh = self.dhqt * self.fl_in.Tt
        self.fl_out.Tt = self.gas.t_f_h(self.gas.h(self.fl_in.Tt) - dh, tol=1e-6)
        self.fl_out.Pt = (
            self.gas.pr(self.fl_in.Tt, self.fl_out.Tt, 1.0 / self.eff_poly) * self.fl_in.Pt
        )

        # shaft
        N = self.Ncqdes * self.Ncdes / 100.0 * self.fl_in.Tt**0.5
        self.sh_out.N = N * 30.0 / np.pi
        self.sh_out.power = self.fl_in.W * dh

        u = self.mean_radius * N
        self.psi = dh / (2.0 * self.stage_count * u**2)

        # outwards
        self.Wc = self.fl_in.W * np.sqrt(self.fl_in.Tt / 288.15) / (self.fl_in.Pt / 101325.0)

        self.Wcrit = (
            self.gas.wqa_crit(self.fl_in.Pt, self.fl_in.Tt, tol=1e-6) * self.area_in / self.blokage
        )
        self.Tt_ratio = self.fl_out.Tt / self.fl_in.Tt
