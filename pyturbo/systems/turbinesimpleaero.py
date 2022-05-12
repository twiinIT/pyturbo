import numpy as np
from cosapp.systems import System

from pyturbo.ports import FluidPort, ShaftPort
from pyturbo.thermo.ideal_gas import IdealGas


class TurbineSimpleAero(System):
    """
    A simple aerodynamic gas turbine model.

    It computes the exit gas `fl_out` from inlet gas `fl_in` for a given pressure ratio and efficency.
    The generated power `shaft_out.power` is also computed.
    """

    def setup(self):
        # inputs/outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")
        self.add_output(ShaftPort, "shaft_out")

        # inwards
        self.add_inward("eff_poly", 0.9, desc="polytropic efficiency")
        self.add_inward("pr", 5.0, desc="pressure ratio")
        self.add_inward("gas", IdealGas(287.058, 1004.0))

        # outwards
        self.add_outward("Wc", unit="kg/s", desc="corrected mass flow")
        self.add_outward("Tt_ratio", desc="total temperature ratio")

    def compute(self):
        # fluid
        self.fl_out.W = self.fl_in.W
        self.fl_out.pt = self.fl_in.pt / self.pr
        self.fl_out.Tt = self.gas.t_from_pr(self.pr, self.fl_in.Tt, self.eff_poly)
        self.Tt_ratio = self.fl_out.Tt / self.fl_in.Tt

        # shaft power
        self.shaft_out.power = self.fl_in.W * (
            self.gas.h(self.fl_in.Tt) - self.gas.h(self.fl_out.Tt)
        )

        # outwards
        self.Wc = self.fl_in.W * np.sqrt(self.fl_in.Tt / 288.15) / (self.fl_in.pt / 101325.0)
