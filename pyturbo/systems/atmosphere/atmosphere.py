# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import ambiance
from cosapp.systems import System

from pyturbo.thermo import IdealDryAir


class Atmosphere(System):
    """Standard atmosphere model.

    Inputs
    ------
    gas: Gas, default=IdealDryAir()
        gas model
    altitude[m]: float, default=0.0
        altitude
    mach[]: float, default=0.0
        Mach number
    dtamb[K]: float, default=0.0
        ambient temperature delta to standard atmosphere

    Outputs
    -------
    pamb[Pa]: float
        static ambient pressure
    Pt[Pa]: float
        total pressure
    Tt[K]: float
        total temperature
    """

    def setup(self):
        self.add_inward("gas", IdealDryAir(), desc="gas model")
        self.add_inward("altitude", 0.0, unit="m", desc="altitude")
        self.add_inward("mach", 0.0, unit="", desc="Mach number")
        self.add_inward(
            "dtamb", 0.0, unit="K", desc="ambient temperature delta to standard atmosphere"
        )

        self.add_outward("pamb", 101325.0, unit="Pa", desc="ambient pressure")
        self.add_outward("Pt", 101325.0, unit="Pa", desc="Total pressure")
        self.add_outward("Tt", 288.15, unit="K", desc="Total temperature")

    def compute(self):
        atm = ambiance.Atmosphere(self.altitude)
        pamb = atm.pressure[0]
        tamb = atm.temperature[0] + self.dtamb

        self.pamb = pamb
        self.Tt = self.gas.total_t(tamb, self.mach)
        self.Pt = self.gas.total_p(pamb, tamb, self.Tt)
