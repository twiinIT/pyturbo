from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo.ideal_gas import IdealGas


class CombustorSimpleAero(System):
    """A simple aerodynamic model of a combustor.

    This model takes into account a burner efficiency to compute exit temperature from
    inlet fluid (air) and fuel.
    The Fuel Heating Value is also an input of the model.
    """

    def setup(self, FluidLaw=IdealGas):
        # inputs / outputs
        self.add_input(FluidPort, "fuel_in")
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # inwards / outwards
        self.add_inward("gas", IdealGas(287.058, 1004.0))  # not representing fuel/air mix yet
        self.add_inward("fhv", 46.2e6, unit="J/kg", desc="Fuel Heating Value")
        self.add_inward("eff", 0.99)

    def compute(self):
        # computations
        h_out = self.gas.h(self.fl_in.Tt) + self.fuel_in.W / self.fl_in.W * self.fhv * self.eff

        # output conditions
        self.fl_out.W = self.fl_in.W + self.fuel_in.W
        self.fl_out.pt = self.fl_in.pt
        self.fl_out.Tt = self.gas.t_from_h(h_out)
