# Copyright (C) 2022, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.ports import Port


class FluidPort(Port):

    """A fluid port aggregating basic information

    Variables
    ---------
    W [kg/s] : float
        mass flow
    pt [Pa] : float
        total pressure
    Tt [K] : float
        total temperature
    """

    def setup(self):
        self.add_variable("W", 1.0, unit="kg/s", desc="mass flow rate")
        self.add_variable("pt", 101325.0, unit="Pa", desc="total pressure")
        self.add_variable("Tt", 288.15, unit="K", desc="total temperature")
