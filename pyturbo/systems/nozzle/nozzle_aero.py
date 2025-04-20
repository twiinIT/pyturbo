# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
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
        self.add_inward("area_in", (0.25**2) * np.pi, unit="m**2", desc="inlet aero section")
        self.add_inward("area_exit", (0.15**2) * np.pi, unit="m**2", desc="exit aero section")
        self.add_inward("area", (0.15**2) * np.pi, unit="m**2", desc="choked/exit area")

        # outwards
        self.add_outward("speed", 1.0, unit="m/s", desc="exhaust gas speed")
        self.add_outward("thrust", unit="N")
        self.add_outward("mach", 0.5, unit="", desc="mach at outlet")

        # off design
        self.add_inward("mach_exit", 0.5)
        self.add_unknown("mach_exit")
        self.add_unknown("fl_in.W")
        self.add_equation("mach == mach_exit")
        self.add_equation("fl_in.W == fl_out.W")

        # init
        self.fl_in.W = 100.0

    def compute(self):
        # outputs
        self.fl_out.Pt = self.fl_in.Pt
        self.fl_out.Tt = self.fl_in.Tt

        # Outlet gas flow properties
        ts_exit = self.gas.static_t(self.fl_out.Tt, self.mach_exit, tol=1e-6)

        ps_crit = self.gas.static_p(
            self.fl_out.Pt, self.fl_out.Tt, 1, tol=1e-6
        )  # Static critical pressure is static presure when Mach = 1.0

        ps_exit = max(ps_crit, self.pamb)

        self.mach = self.gas.mach_f_ptpstt(self.fl_in.Pt, ps_exit, self.fl_in.Tt, tol=1e-6)

        self.speed = self.gas.c(ts_exit) * self.mach

        density_exit = self.gas.density(ps_exit, ts_exit)

        self.fl_out.W = density_exit * self.speed * self.area_exit

        self.thrust = self.fl_out.W * self.speed + self.area_exit * (ps_exit - self.pamb)
