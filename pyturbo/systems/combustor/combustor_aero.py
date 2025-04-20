# Copyright (C) 2022-2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo import IdealDryAir


class CombustorAero(System):
    """A simple aerodynamic model of a combustor.

    This model takes into account a burner efficiency to compute exit temperature from
    inlet fluid (air) and fuel.
    The Fuel Heating Value is also an input of the model.

    Inputs
    ------
    gas: Gas, default=IdealDryAir()
        gas model

    fl_in: FluidPort
        fluid going into the combustor

    fuel_W[kg/s]: float
        fuel consumption
    fvh[J/Kg]: float
        Fuel Heating Value
        default value is 46e6 J/Kg corresponding at fuel comsumption in air
    eff[-]: float
        efficiency of combustion
        default value is 0.99

    Outputs
    -------
    fl_out: FluidPort
        fluid leaving the combustor

    Tcomb[K]: float
        combustion temperature
    """

    def setup(self):
        # properties
        self.add_inward("gas", IdealDryAir())  # not representing fuel/air mix yet

        # inputs / outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # inwards / outwards
        self.add_inward("fuel_W", 1.0, unit="kg/s", desc="fuel flow")
        self.add_inward("fhv", 46.2e6, unit="J/kg", desc="Fuel Heating Value")
        self.add_inward("eff", 0.99, unit="", desc="combustion efficiency")

        self.add_outward("Tcomb", 600.0, unit="K", desc="combustion temperature")

        # design methods
        scaling = self.add_design_method("scaling")
        scaling.add_unknown("fuel_W")
        scaling.add_target("Tcomb")

    def compute(self):
        self.fl_out.Pt = self.fl_in.Pt
        self.fl_out.W = self.fl_in.W + self.fuel_W

        h_out = self.gas.h(self.fl_in.Tt) + self.fuel_W / self.fl_out.W * self.fhv * self.eff
        self.Tcomb = self.gas.t_f_h(h_out, tol=1e-6)
        self.fl_out.Tt = self.Tcomb
