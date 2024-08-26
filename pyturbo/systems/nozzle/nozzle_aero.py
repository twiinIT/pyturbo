# Copyright (C) 2022-2023, twiinIT
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
        self.add_inward("area_in", 0.0625 * np.pi, unit="m**2", desc="inlet aero section")
        self.add_inward("area_exit", 0.0225 * np.pi, unit="m**2", desc="exit aero section")
        self.add_inward("area", 0.0225 * np.pi, unit="m**2", desc="choked/exit area")
        self.add_inward("m2", 0.990, unit="", desc="mach at outlet")
        self.add_inward("mach", 1.0, unit="", desc="mach at throat")

        # outwards
        self.add_outward("m1", 0.3, unit="", desc="mach at inlet")
        self.add_outward("speed", 0.0, unit="m/s", desc="fluid flow speed at outlet")
        self.add_outward("thrust", unit="N")

        # off design
        self.add_equation(
            "area/area_in == (m1/mach) * (((1 + ((0.4/2)*(mach**2))))/(1 + ((0.4/2)*(m1**2))))**(2.4/0.8)"
        )
        self.add_equation(
            "area_exit/area == (mach/m2) * (((1 + ((0.4/2)*(m2**2))))/(1 + ((0.4/2)*(mach**2))))**(2.4/0.8)"
        )

        # init
        self.fl_in.W = 100.0

    def compute(self):
        # outputs
        self.fl_out.Pt = self.fl_in.Pt
        self.fl_out.Tt = self.fl_in.Tt
        self.fl_out.W = self.fl_in.W

        rho1 = 1.2

        ps1 = self.fl_in.Pt - 0.5 * ((self.fl_in.W**2) / (rho1 * (self.area_in**2)))

        self.m1 = self.gas.mach_f_ptpstt(self.fl_in.Pt, ps1, self.fl_in.Tt, tol=1e-6)

        ts2 = self.gas.static_t(self.fl_out.Tt, self.m2, tol=1e-6)

        self.speed = np.sqrt(self.gas.gamma(ts2) * 287 * ts2) * self.m2

        ps2 = self.gas.static_p(self.fl_out.Pt, self.fl_out.Tt, self.m2, tol=1e-6)

        self.thrust = self.fl_out.W * self.speed + self.area_exit * (ps2 - self.pamb)
