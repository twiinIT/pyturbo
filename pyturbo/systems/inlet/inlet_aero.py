from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo import IdealDryAir


class InletAero(System):
    """
    A simple inlet aerodynamic model.

    It compute drag at throat:

    drag = - W * speed + (ps - pamb) * area

    Parameters
    ----------
    FluidFlow: Class, default is IdealDryAir
        Class provided the characteristics of gas.
        gas.mach: compute mach from total pressure and temperature, mass per area
        gas.static_p: compute static pressure from total pressure and mach
        gas.c: compute speed of sound

    Inputs
    ------
    fl_in: FluidPort
        gas going into the inlet

    pamb[Pa]: float
        ambiant static pressure

    area[m**2]: float
        inlet throat area

    Outputs
    -------
    fl_out: FluidPort
        gas leaving the inlet

    ps[Pa]: float
        static pressure at throat
    mach[-]: float
        fluid mach number at throat
    speed[m/s]: float
        fluid speed at throat in m/s
    drag[N]: float
        drag computed at throat. If drag < 0, aspiration contribute to thrust

    Good practice
    -------------
    1:
        fl_in.pt must remain bigger than pamb
    """

    def setup(self, FluidFlow = IdealDryAir):
        # inputs / outputs
        self.add_input(FluidPort, "fl_in")
        self.add_output(FluidPort, "fl_out")

        # inwards/outwards
        self.add_inward("gas", FluidFlow())
        self.add_inward("pamb", 101325.0, unit="Pa", desc="ambient static pressure")

        self.add_inward("area", 1.0, unit="m**2", desc="throat area")

        self.add_outward("ps", 0.0, unit="pa", desc="static pressure at throat")
        self.add_outward("mach", 0.0, unit="", desc="mach at throat")
        self.add_outward("speed", 0.0, unit="m/s", desc="fluid flow speed at throat")
        self.add_outward("drag", 0.0, unit="N", desc="drag")

    def compute(self):
        self.fl_out.Tt = self.fl_in.Tt
        self.fl_out.pt = self.fl_in.pt
        self.fl_out.W = self.fl_in.W

        pt = self.fl_in.pt
        tt = self.fl_in.Tt
        self.mach = self.gas.mach(pt, tt, self.fl_in.W / self.area)

        self.ps = self.gas.static_p(pt, tt, self.mach)
        self.speed = self.mach * self.gas.c(tt)

        self.drag = self.fl_in.W * self.speed + (self.ps - self.pamb) * self.area
