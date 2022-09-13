# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.ports import FluidPort, ShaftPort
from pyturbo.thermo import IdealDryAir


class TurbineAero(System):
    """
    A simple aerodynamic gas turbine model.

    It computes the exit gas `fl_out` from inlet gas `fl_in` for a given pressure ratio
    and efficency. The generated power `sh_out.power` is also computed.

    Parameters
    ----------
    FluidLaw: Class, default is IdealDryAir
        Class providing gas characteristics
        gas.h to get enthalpy from temperature
        gas.t_from_h to get temperature from enthapie
        gas.pr to get density from Tt_in, Tt_out, eff_poly
        gas.density to get pressure ratio from p, T
        gas.c to get mach

    Inputs
    ------
    fl_in: FluidPort
        inlet gas

    eff_poly[-]: float
        polytropic efficiency
    er[-]: float
        expansion ratio
    Ncdes[%]: float
        design corrected speed
    Ncqdes[rpm/K**0.5]: float
        corrected speed over design value ratio

    stage_count: int
        number of stages
    area_in[m**2]: float
        inlet area
    mean_radius[m]: float
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
        aerodynamic loading

    Design methods
    --------------
    off design:
        Ncqdes unknown

    """

    def setup(self, FluidLaw=IdealDryAir):
        # properties
        self.add_property("gas", FluidLaw())

        # inputs/outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")
        self.add_output(ShaftPort, "sh_out")

        # inwards
        self.add_inward("eff_poly", 0.9, desc="polytropic efficiency")
        self.add_inward("er", 5.0, unit="", desc="expansion ratio")
        # TODO: fix unit
        self.add_inward("Ncdes", 150.0, unit="rpm/K", desc="design corrected speed")
        self.add_inward("Ncqdes", 100.0, unit="", desc="corrected speed over design value ratio")

        self.add_inward("area_in", 1.0, unit="m**2", desc="inlet area")
        self.add_inward("mean_radius", 1.0, unit="m", desc="mean radius")
        self.add_inward("stage_count", 1, unit="", desc="stage count")

        # outwards
        self.add_outward("Wc", unit="kg/s", desc="corrected mass flow")
        self.add_outward("Tt_ratio", unit="", desc="total temperature ratio")
        self.add_outward("psi", unit="", desc="aerodynamic loading")

        # off design
        self.add_unknown("Ncqdes", max_rel_step=0.5)

        # design method
        self.add_design_method("temperature").add_target("fl_in.Tt")
        self.add_design_method("speed").add_unknown("Ncdes", lower_bound=0.0)

    def compute(self):
        # fluid
        self.fl_out.W = self.fl_in.W
        self.fl_out.Pt = self.fl_in.Pt / self.er
        self.fl_out.Tt = self.gas.t_from_pr(1.0 / self.er, self.fl_in.Tt, 1.0 / self.eff_poly)
        self.Tt_ratio = self.fl_out.Tt / self.fl_in.Tt

        # shaft
        N = self.Ncqdes * self.Ncdes / 100.0 * self.fl_in.Tt**0.5
        self.sh_out.N = N * 30.0 / np.pi
        dh = self.gas.h(self.fl_in.Tt) - self.gas.h(self.fl_out.Tt)
        self.sh_out.power = self.fl_in.W * dh

        # inlet Mach number
        def Mach_solver(mach):
            t = self.gas.static_t(self.fl_in.Tt, mach)
            p = self.gas.pr(self.fl_in.Tt, t, 1.0) * self.fl_in.Pt
            rho = self.gas.density(p, t)
            vm = self.fl_in.W / (rho * self.area_in)
            return mach - vm / self.gas.c(t)

        u = self.mean_radius * N
        self.psi = dh / (2.0 * self.stage_count * u**2)

        # outwards
        self.Wc = self.fl_in.W * np.sqrt(self.fl_in.Tt / 288.15) / (self.fl_in.Pt / 101325.0)
