import numpy as np

from cosapp.systems import System

from pyturbo.ports import FluidPort, ShaftPort
from pyturbo.thermo.ideal_gas import IdealGas


class CompressorSimpleAero(System):
    """
    Compressor aero
    fl_out is computed from fl_in and shaft_in.
    """
    def setup(self):
        # inputs/outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")
        self.add_input(ShaftPort, "shaft_in")

        # inwards
        self.add_inward("eff_poly", 0.9, desc='polytropic efficiency')
        self.add_inward("gas", IdealGas(287.058, 1004.0)) # dry air

        # outwards
        self.add_outward('Wc', unit='kg/s',desc='corrected mass flow')
        self.add_outward('Nc', unit='rpm', desc='corrected shaft speed')
        self.add_outward('pt_ratio', desc='total pressure ratio')
        self.add_outward('Tt_ratio', desc='total temperature ratio')


    def compute(self):
        # enthalpy conservation
        h = self.gas.h(self.fl_in.Tt) + self.shaft_in.power/self.fl_in.W
        self.fl_out.Tt = self.gas.t_from_h(h)
        self.Tt_ratio = self.fl_out.Tt / self.fl_in.Tt

        # mass flow conservation
        self.fl_out.W = self.fl_in.W

        # pressure
        self.pt_ratio = self.gas.pr(self.fl_in.Tt, self.fl_out.Tt, self.eff_poly)
        self.fl_out.pt = self.fl_in.pt * self.pt_ratio

        # outwards
        self.Wc = self.fl_in.W * np.sqrt(self.fl_in.Tt/288.15) / (self.fl_in.pt/101325.) 
        self.Nc = self.shaft_in.N / np.sqrt(self.fl_in.Tt/288.15) 