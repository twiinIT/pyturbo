from cosapp.systems import System

from pyturbo.ports import FluidPort
from pyturbo.thermo import IdealDryAir


class InletAero(System):
    """A simple inlet aerodynamic model.

    It compute drag at throat:

    drag = - W * speed + (ps - pamb) * area

    Parameters
    ----------
    FluidFlow: Class, default is IdealDryAir
        Class provided the characteristics of gas.

    Inputs
    ------
    fl_in: FluidPort
        gas going into the inlet

    pamb[Pa]: float, default=101325.0
        ambiant static pressure

    area[m**2]: float, default=1.0
        inlet throat area

    Outputs
    -------
    fl_out: FluidPort
        gas leaving the inlet

    ps[Pa]: float, default=0.0
        static pressure at throat
    mach[-]: float, default=0.0
        fluid mach number at throat
    speed[m/s]: float, default=0.0
        fluid speed at throat in m/s
    drag[N]: float, default=0.0
        drag computed at throat. If drag < 0, aspiration contribute to thrust

    Good practice
    -------------
    1:
        fl_in.Pt must remain bigger than pamb
    """

    def setup(self, FluidFlow=IdealDryAir):
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
        self.fl_out.Pt = self.fl_in.Pt
        self.fl_out.W = self.fl_in.W

        pt = self.fl_in.Pt
        tt = self.fl_in.Tt
        self.mach = self.gas.mach_f_wqa(pt, tt, self.fl_in.W / self.area, tol=1e-6)

        self.ps = self.gas.static_p(pt, tt, self.mach, tol=1e-6)
        self.speed = self.mach * self.gas.c(tt)

        self.drag = self.fl_in.W * self.speed + (self.ps - self.pamb) * self.area
