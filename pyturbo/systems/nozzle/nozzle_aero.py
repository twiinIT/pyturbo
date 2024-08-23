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
        self.add_inward("gamma", 1.4, unit="", desc="Heat capacity ratio")
        self.add_inward("rho_1", 1.2, unit="kg/m**3", desc="Fluid density at inlet")
        self.add_inward("rho_2", 1.2, unit="kg/m**3", desc="Fluid density at outlet")

        # outwards
        self.add_outward("m2", 0.0, unit="", desc="mach at outlet")
        self.add_outward("mach", 0.0, unit="", desc="mach at outlet")
        self.add_outward("speed", 0.0, unit="m/s", desc="fluid flow speed at outlet")
        self.add_outward("thrust", unit="N")

        # off design
        self.add_equation("fl_in.W == fl_out.W")

        # init
        self.fl_in.W = 100.0

    def compute(self):
        # outputs
        self.fl_out.Pt = self.fl_in.Pt
        self.fl_out.Tt = self.fl_in.Tt

        ps_crit = ((2 / (self.gamma + 1)) ** (self.gamma / (self.gamma - 1))) * self.fl_out.Pt
        ps1 = self.fl_in.Pt - 0.5 * ((self.fl_in.W**2) / (self.rho_1 * (self.area_in**2)))
        ps2 = max(ps_crit, self.pamb)

        ts1 = self.fl_in.Tt + ((1 - self.gamma) / (2 * self.gamma * 287)) * (
            self.fl_in.W / (self.rho_1 * self.area_in)
        )
        ts2 = ts1 * ((self.rho_2 / self.rho_1) ** (1 / (1 - self.gamma)))

        self.speed = np.sqrt(
            (2 / self.rho_2) * ((self.fl_in.W / (2 * self.rho_1 * (self.area_in**2))) + ps1 - ps2)
        )
        self.m2 = self.speed / np.sqrt(self.gamma * 287 * ts2)
        self.mach = self.m2
        self.fl_out.W = self.rho_2 * self.speed * self.area_exit
        self.thrust = self.fl_out.W * self.speed + self.area_exit * (ps2 - self.pamb)
