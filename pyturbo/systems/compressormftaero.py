import numpy as np
from cosapp.ports import Port
from cosapp.systems import System

from pyturbo.mft.compressor import SimplifiedMftCompressor
from pyturbo.ports import FluidPort
from pyturbo.thermo.ideal_gas import IdealGas


class CompressorAeroMft(System):
    def setup(self):

        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        self.add_inward("pcnr", 90.0)
        self.add_inward("gh", 0.0)
        self.add_inward("cmp_model", SimplifiedMftCompressor())
        self.add_inward("gas", IdealGas(287.058, 1004.0)) # dry air

    def compute(self):
        self.fl_out.Tt = self.gas.t_from_h(self.gas.h(self.fl_in.Tt) + self.cmp_model.ghr(self.gh))
        self.fl_out.pt = self.fl_in.pt * self.cmp_model.pr(self.pcnr, self.gh)
        self.fl_out.W = (
            self.cmp_model.wr(self.pcnr, self.gh) * self.fl_out.pt / np.sqrt(self.fl_out.Tt)
        )
