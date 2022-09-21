from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo import IdealDryAir


class ChannelAero(System):
    """Stator simple channel model.

    Pt_out = Pt_in * (1 - pressure_loss)

    Parameters
    ----------
    FluidLaw: Class, default=IdealDryAir
        class provided the characteristics of gas.

    Inputs
    ------
    fl_in: FluidPort
        inlet fluid

    pressure_loss[-]: float, default=0.01
        pressure loss coefficient

    area_in[m**2]: float, default=1.
        inlet area section
    area_exit[m**2]: float, default=1.
        exit area section

    Outputs
    -------
    fl_out: FluidPort
        gas leaving the inlet

    """

    def setup(self, FluidLaw=IdealDryAir):
        # properties
        self.add_property("gas", FluidLaw())

        # aero
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # geom
        self.add_inward("area_in", 10.0, unit="m**2", desc="inlet aero section")
        self.add_inward("area_exit", 10.0, unit="m**2", desc="exit aero section")

        # inwards
        self.add_inward("pressure_loss", 0.01, unit="", desc="pressure loss coefficient")

        # outwards
        self.add_outward("mach_in", 0.0, unit="", desc="inlet mach")
        self.add_outward("mach_exit", 0.0, unit="", desc="exit mach")

    def compute(self):
        self.fl_out.W = self.fl_in.W
        self.fl_out.Tt = self.fl_in.Tt
        self.fl_out.Pt = self.fl_in.Pt * (1.0 - self.pressure_loss)

        self.mach_in = self.gas.mach(self.fl_in.Pt, self.fl_in.Tt, self.fl_in.W / self.area_in)
        self.mach_exit = self.gas.mach(
            self.fl_out.Pt, self.fl_out.Tt, self.fl_out.W / self.area_exit
        )
