from cosapp.systems import System

from pyturbo.systems import CombustorSimpleAero, CompressorSimpleAero, TurbineSimpleAero


class GasGeneratorSimpleAero(System):
    """A simple gas generator aerodynamic model.

    This model includes a compressor, a combustor and a turbine. The power transmission
    between the turbine and the compressor is direct without and intermediate shaft model.
    """

    def setup(self):
        # children
        self.add_child(CompressorSimpleAero("compressor"), pulling=["fl_in"])
        self.add_child(CombustorSimpleAero("combustor"), pulling=["fuel_in"])
        self.add_child(TurbineSimpleAero("turbine"), pulling=["fl_out"])

        # connection
        self.connect(self.turbine.shaft_out, self.compressor.shaft_in)
        self.connect(self.compressor.fl_out, self.combustor.fl_in)
        self.connect(self.combustor.fl_out, self.turbine.fl_in)

        # outwards
        self.add_outward("pr", 1.0, desc="pressure ratio")
        self.add_outward("opr", 1.0, desc="overall pressure ratio")

        # init
        self.compressor.shaft_in.power = 10e6

    def compute(self):
        self.pr = self.fl_out.pt / self.fl_in.pt
        self.opr = self.compressor.fl_out.pt / self.fl_in.pt
