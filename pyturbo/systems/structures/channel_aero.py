from cosapp.systems import System

from pyturbo.ports import FluidPort


class ChannelAero(System):
    """Stator simple channel model.

    Pt_out = Pt_in * (1 - pressure_loss)

    Inputs
    ------
    fl_in: FluidPort
        inlet fluid

    pressure_loss[-]: float, default=0.01
        pressure loss coefficient

    Outputs
    -------
    fl_out: FluidPort
        gas leaving the inlet

    """

    def setup(self):
        # aero
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # inwards
        self.add_inward("pressure_loss", 0.01, unit="", desc="pressure loss coefficient")

    def compute(self):
        self.fl_out.W = self.fl_in.W
        self.fl_out.Tt = self.fl_in.Tt
        self.fl_out.Pt = self.fl_in.Pt * (1.0 - self.pressure_loss)
