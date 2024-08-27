# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo import IdealDryAir


class NozzleAero(System):
    """A simple nozzle aerodynamic model.

    It computes the gross thrust from the flow and ambient static
    pressure assuming a choked throat=exit area (convergent nozzle).

    thrust = W * speed + (ps - pamb) * area

    Parameters
    ----------
    FluidLaw: Class, default=IdealDryAir
        class provided the characteristics of gas.

    Inputs
    ------
    fl_in: FluidPort
        inlet gas

    pamb[Pa]: float, default=101325.0
        ambiant static pressure

    area[m**2]: float, default=1.0
        nozzle throat area

    Outputs
    -------
    fl_out: FluidPort
        exit gas

    ps[Pa]: float, default=0.0
        static pressure at throat
    mach[-]: float, default=0.0
        fluid mach number at throat
    speed[m/s]: float, default=0.0
        fluid speed at throat
    thrust[N]: float, default=0.0
        thrust in N computed at throat. If drag < 0, aspiration contribute to thrust

    Design methods
    --------------
    off design:
        fluid mass flow imposed by chocked throat

    Good practice
    -------------
    1:
        fl_in.Pt must be bigger than pamb.
    """

    def setup(self, FluidLaw=IdealDryAir):
        # properties
        self.add_inward("gas", FluidLaw())

        # inputs / outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")
        self.add_inward("pamb", 101325.0, unit="Pa", desc="ambient static pressure")

        # geom
        self.add_inward("area_in", 10.0, unit="m**2", desc="inlet aero section")
        self.add_inward("area_exit", 10.0, unit="m**2", desc="exit aero section")
        self.add_inward("area", 1.0, unit="m**2", desc="choked/exit area")

        # outwards
        self.add_outward("ps", 0.0, unit="pa", desc="static pressure at throat")
        self.add_outward("mach", 0.0, unit="", desc="mach at throat")
        self.add_outward("speed", 0.0, unit="m/s", desc="fluid flow speed at throat")
        self.add_outward("thrust", unit="N")

        # off design
        self.add_equation("fl_in.W == fl_out.W")

        # init
        self.fl_in.W = 100.0

    def compute(self):
        # outputs
        self.fl_out.Pt = self.fl_in.Pt
        self.fl_out.Tt = self.fl_in.Tt

        # assumes convergent nozzle (throat at exit)
        self.mach = self.gas.mach_f_ptpstt(
            self.fl_in.Pt, self.pamb, self.fl_in.Tt, tol=1e-6
        )  # How is this function able to limit the outlet at mach = 1 ?

        ts = self.gas.static_t(self.fl_in.Tt, self.mach, tol=1e-6)
        self.ps = self.gas.static_p(self.fl_in.Pt, self.fl_in.Tt, self.mach, tol=1e-6)
        rho = self.gas.density(self.ps, ts)
        self.speed = self.gas.c(ts) * self.mach

        if self.mach > 1.0:
            self.fl_out.W = self.gas.wqa_crit(self.fl_in.Pt, self.fl_in.Tt, tol=1e-6) * self.area
        else:
            self.fl_out.W = rho * self.speed * self.area

        self.thrust = self.fl_out.W * self.speed + (self.ps - self.pamb) * self.area
